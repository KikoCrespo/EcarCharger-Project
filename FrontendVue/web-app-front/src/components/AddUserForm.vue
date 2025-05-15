<template>
  <form @submit.prevent="handleSubmit">
    <div class="flex h-auto gap-0 bg-white rounded-md">

      <div class="flex w-full justify-center items-center pb-10 pl-5 mt-5 mb-5 ">
        <div class=" flex-1 w-auto pr-20 mt-5 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
          <div class=" ">
            <h2 class="text-xl font-bold text-gray-900">Adicionar Utilizador</h2>
          </div>
          <div class="grid grid-cols-2 gap-x-6 gap-y-8 sm:col-span-6">
            <div>
              <label for="first-name" class="block text-sm font-medium text-gray-900">Primeiro Nome</label>
              <div class="mt-2">
                <input v-model="form.firstName" type="text" name="first-name" id="first-name" autocomplete="given-name"
                  class="block w-auto border-0 border-b border-extra-soft-orange  bg-transparent text-gray-900 placeholder:text-gray-400 focus:border-soft-orange focus:outline-none focus:ring-0 duration-300 sm:text-sm" />
                <span v-if="formErrors.firstName" class="text-red-500 text-sm">{{ formErrors.firstName }} </span>
              </div>
            </div>

            <div>
              <label for="last-name" class="block text-sm font-medium text-gray-900">Último Nome</label>
              <div class="mt-2">
                <input v-model="form.lastName" type="text" name="last-name" id="last-name" autocomplete="family-name"
                  class="block w-auto border-0 border-b border-extra-soft-orange  bg-transparent text-gray-900 placeholder:text-gray-400 focus:border-soft-orange focus:outline-none focus:ring-0 duration-300 sm:text-sm" />
                <span v-if="formErrors.lastName" class="text-red-500 text-sm"> {{ formErrors.lastName }}
                </span>
              </div>
            </div>
          </div>

          <div class="sm:col-span-3">
            <label for="new-username" class="block text-sm/6 font-medium text-gray-900">Email</label>
            <div class="mt-2 w-1/2">
              <div
                class="flex w-auto items-center border-b border-extra-soft-orange bg-transparent pl-3 focus-within:border-soft-orange focus:outline-none focus:ring-0 duration-300">
                <span class="w-auto border-0 bg-transparent mr-1 text-base text-gray-500 select-none sm:text-sm/6">
                  {{ entidade }}.com/
                </span>
                <input v-model="form.email" type="text" name="new-username" id="new-username"
                  class="block w-auto border-0 bg-transparent text-gray-900 placeholder:text-gray-400 focus:outline-none focus:ring-0 sm:text-sm"
                  placeholder="Utilizador" autocomplete="new-email" />
                <span v-if="formErrors.email" class="text-red-500 text-sm">{{ formErrors.email }}</span>
              </div>
            </div>
          </div>


          <div class="sm:col-span-5">
            <label for="departamento" class="block text-sm font-medium text-gray-900">Departamento</label>
            <div class="mt-2">
              <select v-model="form.departamento" name="departamento"
                class="block w-auto border-0 border-b border-extra-soft-orange bg-transparent text-gray-900 placeholder:text-gray-400 focus:border-soft-orange focus:outline-none focus:ring-0 duration-300 sm:text-sm">
                <option value="">Selecione um departamento</option>
                <option v-for="dep in departamentos" :key="dep" :value="dep">{{ dep }}</option>
              </select>
              <span v-if="formErrors.departamento" class="text-red-500 text-sm">{{ formErrors.departamento }} </span>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-x-6 gap-y-8 sm:col-span-6">
            <div>
              <label for="password" class="block text-sm font-medium text-gray-900">Palavra-passe Padrão</label>
              <div class="mt-2">
                <input v-model="form.password" type="password" name="new-password" id="new-password" 
                  placeholder="Password" autocomplete="new-password"
                  class="block w-auto border-0 border-b border-extra-soft-orange bg-transparent text-gray-900 placeholder:text-gray-400 focus:border-soft-orange focus:outline-none focus:ring-0 duration-300 sm:text-sm" />
                <span v-if="formErrors.password" class="text-red-500 text-sm">{{ formErrors.password }}</span>
              </div>
            </div>

            <label class="inline-flex items-center mb-5 cursor-pointer">
              <input v-model="form.is_admin" type="checkbox" value="" class="sr-only peer" :true-value=true :false-value=false>
              <div
                class="relative w-9 h-5 bg-gray-200 peer-focus:outline-none peer-focus:ring-0 peer-focus:ring-soft-orange dark:peer-focus:ring-0 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all dark:border-gray-600 peer-checked:bg-soft-orange dark:peer-checked:bg-blue-600">
              </div>
              <span class="ms-3 text-sm font-medium text-gray-900 dark:text-gray-300">Admin</span>
            </label>
          </div>

        </div>
      </div>
    </div>

    <div class="mt-2 flex items-center justify-end gap-x-6">
      <button type="submit"
        class="rounded-md bg-extra-soft-orange px-3 py-2 text-sm font-semibold text-gray-400 shadow-sm hover:bg-soft-orange hover:text-black duration-300 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-orange-200">
        Registar
      </button>
    </div>
  </form>
</template>

<script setup>
import { onMounted, ref, defineProps, computed } from 'vue'
import { UserCircleIcon, PencilIcon } from '@heroicons/vue/24/outline'
import api from '@/interceptors/axiosInterceptor'

const departamentos = [
  'Recursos Humanos',
  'Engenharia',
  'Marketing',
  'Financeiro',
  'TI',
  'Operações'
];

const props = defineProps({
  user_data: {
    type: Object,
    required: true
  }
});

const form = ref({
  firstName: '',
  lastName: '',
  email: '',
  departamento: '',
  password: '',
  is_admin: 0
});

const formErrors = ref({
  firstName: '',
  lastName: '',
  email: '',
  departamento: '',
  password: '',
  is_admin: ''
});


const entidade = ref('')

onMounted(() => {
  entidade.value = String(props.user_data.entidade || '')
    .normalize("NFD") // Remove acentos
    .replace(/[\u0300-\u036f]/g, '') // remove acentos
    .replace(/[^a-zA-Z0-9]/g, '') // remove tudo o que não for letra ou numero
    .toLowerCase()  // mete tudo em minusculas
})





const handleSubmit = () => {

  // Limpar erros anteriores
  formErrors.value = {
    firstName: '',
    lastName: '',
    email: '',
    departamento: '',
    password: '',
    is_admin: ''
  };

  let isValid = true;

  if (!form.value.firstName) {
    formErrors.value.firstName = 'Primeiro nome é obrigatório.';
    isValid = false;
  }

  if (!form.value.lastName) {
    formErrors.value.lastName = 'Último nome é obrigatório.';
    isValid = false;
  }

  if (!form.value.email) {
    formErrors.value.email = 'Email é obrigatório.';
    isValid = false;
  }

  if (!form.value.departamento) {
    formErrors.value.departamento = 'Selecione um departamento.';
    isValid = false;
  }

  if (!form.value.password) {
    formErrors.value.password = 'Password é obrigatória.';
    isValid = false;
  }


  if (!isValid) {
    return;
  }

  const emailCompleto = `${form.value.email}@${entidade.value}.com`;
  console.log(form.value.is_admin)
  if (form.value.is_admin) {
    api.post('/utilizadores/registar/admin/', {
      first_name: form.value.firstName,
      last_name: form.value.lastName,
      email: emailCompleto,
      u_departamento: form.value.departamento,
      u_tipo: form.value.is_admin,
      password: form.value.password
    })
      .then(response => {
        console.log('Utilizador registado com Sucesso:', response.data);
      })
      .catch(error => {
        console.error('Erro ao registar utilizador:', error);
      });
  } else {
    api.post('/utilizadores/registar/utilizador/', {
      first_name: form.value.firstName,
      last_name: form.value.lastName,
      email: emailCompleto,
      u_departamento: form.value.departamento,
      u_tipo: form.value.is_admin,
      password: form.value.password
    })
      .then(response => {
        console.log('Utilizador registado com Sucesso:', response.data);
      })
      .catch(error => {
        console.error('Erro ao registar utilizador:', error);
      });
  }
};

</script>
