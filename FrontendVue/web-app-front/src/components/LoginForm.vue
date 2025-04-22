<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const email = ref('');
const password = ref('');
const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const emailError = ref(0);
const passwordError = ref(0);
const router = useRouter();
const loginError = ref('');

const login = async() => {
    emailError.value = 0;
    passwordError.value = 0;

    // Validação do email
    if (!email.value) {
        emailError.value = 1; // Email vazio
    } else if (!emailPattern.test(email.value)) {
        emailError.value = 2; // Email inválido
    }

    // Validação da senha
    if (!password.value) {
        passwordError.value = 1; // Senha vazia
    }

    // Se não houver erros, você pode prosseguir com o login
    if (emailError.value === 0 && passwordError.value === 0) {
        // Aqui você pode adicionar a lógica para o login
        // Por exemplo, chamar uma API para autenticação
        try {
            const response = await axios.post('http://localhost:8000/api/login/', {
                username: email.value,
                password: password.value
            });
            console.log('Resposta da API:', response.data);
            const access = response.data.access;
            const refresh = response.data.refresh;
            localStorage.setItem('access', access);
            localStorage.setItem('refresh', refresh);
            if (response.status === 200) {
                // Redirecionar para a página de dashboard ou outra página
                //router.push('/dashboard'); 
                console.log('Login bem-sucedido!');
            }  
        } catch (error) {
            loginError.value = 'Credenciais inválidas ou erro na conexão.';
            console.error(error);
        }
      } 
  }
</script>




<template>
  <div class="w-full p-5 flex h-full flex-col items-center justify-center">
    <div class="flex mb-20 self-start">
      <img src="../assets/img/hmvdomologo.png" alt="HMV DOMO" class="h-16 " />
    </div>
    <h2 class="text-center text-2xl font-smibold text-gray-900">Iniciar Sessão</h2>
    <form @submit.prevent="login" class="mt-8 space-y-6 w-3/4">
      <div>
        <label for="email" class="block text-md font-regular text-gray-700">Email</label>
        <input 
          v-model="email"
          type="email" 
          name="email"
          id="email"
          :class="emailError === 0 ? 'w-full mt-1 px-4 py-3 text-sm border-b border-extra-soft-orange focus:border-soft-orange focus:outline-hidden' : 'w-full mt-1 px-4 py-3 text-sm border-b border-red-600 focus:border-soft-orange focus:outline-hidden'" 
          placeholder="Insira um email válido" />
        <span v-if="emailError === 1" class="text-red-500 text-sm">O email é obrigatório.</span>
        <span v-if="emailError === 2" class="text-red-500 text-sm">Por favor, insira um email válido.</span>
      </div>
      <div>
        <label for="password" class="block text-md font-regular text-gray-700">Palavra-passe</label>
        <input 
          v-model="password"
          type="password" 
          name="password"
          id="password"
          :class="passwordError === 0 ? 'w-full mt-1 px-4 py-3 text-sm border-b border-extra-soft-orange focus:border-soft-orange focus:outline-hidden' : 'w-full mt-1 px-4 py-3 text-sm border-b border-red-600 focus:border-soft-orange focus:outline-hidden'" 
          placeholder="Insira a sua palavra-passe" />
        <span v-if="passwordError === 1" class="text-red-500 text-sm">A palavra-passe é obrigatória.</span>
      </div>
      <div class="flex flex-col md:flex-row items-center justify-between">
        <label class="flex">
          <input type="checkbox" class="h-5 w-5 text-amber-600 border border-soft-orange rounded focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-soft-orange disabled:border-gray-300 disabled:bg-gray-100 disabled:checked:bg-gray-100" />
          <span class="ml-2 text-sm font-extralight text-gray-700">Lembrar-me</span>
        </label>
        <a href="#" class="text-soft-orange font-extralight text-sm hover:underline sm:ml-4 mt-2 sm:mt-0">Esqueceu-se da palavra-passe?</a>
      </div>
      <button 
        type="submit" 
        class="w-full bg-soft-orange text-black py-3 text-md rounded-md shadow-lg hover:shadow-lg hover:shadow-extra-soft-orange">
        Iniciar Sessão
      </button>
      <span v-if="loginError" class="text-red-500 text-sm">
            {{ loginError }}
      </span>
    </form>
  </div>
</template>


