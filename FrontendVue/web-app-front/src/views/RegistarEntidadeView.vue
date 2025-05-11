<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axiosInterceptor from '../interceptors/axiosInterceptor';



  const socket = new WebSocket("ws://localhost:8000/ws/sensor/");

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log("Received sensor data:", data);
    if(data === null){
        console.log("Sensor 1: Sensor em modo de espera");
    }
    this.sensorData = data;  // Exemplo: guarda os dados no estado

  };

  socket.onopen = () => {
    console.log("WebSocket connected");
  };

  socket.onerror = (error) => {
    console.error("WebSocket error:", error);
  };


const form = ref({
    e_nome: '',
    e_email: '',
    e_nif: '',
    e_contacto: '',
    e_morada: '',
    e_ordem: ''
});

const errors = ref({
    e_nome: '',
    e_email: '',
    e_nif: '',
    e_contacto: '',
    e_morada: '',
    e_ordem: ''
});

const successMessage = ref('');
const router = useRouter();

const submitForm = async () => {
    errors.value = {
        e_nome: '',
        e_email: '',
        e_nif: '',
        e_contacto: '',
        e_morada: '',
        e_ordem: ''
    };
    successMessage.value = '';

    let hasError = false;

    if (!form.value.e_nome) {
        errors.value.e_nome = 'Nome é obrigatório.';
        hasError = true;
    }
    if (!form.value.e_email) {
        errors.value.e_email = 'Email é obrigatório.';
        hasError = true;
    }
    if (!form.value.e_nif) {
        errors.value.e_nif = 'NIF é obrigatório.';
        hasError = true;
    }
    if (!form.value.e_contacto) {
        errors.value.e_contacto = 'Contacto é obrigatório.';
        hasError = true;
    }
    if (!form.value.e_morada) {
        errors.value.e_morada = 'Morada é obrigatória.';
        hasError = true;
    }
    if (!form.value.e_ordem) {
        errors.value.e_ordem = 'Ordem é obrigatória.';
        hasError = true;
    }

    if (hasError) return;

    try {
        await axiosInterceptor.post('/entidades/registar', form.value);
        successMessage.value = 'Entidade registada com sucesso!';
        // router.push('/entidades'); // Se quiseres redirecionar depois
    } catch (error) {
        if (error.response) {
            console.error('Erro da API:', error.response.data);
            alert(error.response.data.error || 'Erro ao registar entidade');
        } else {
            console.error('Erro inesperado:', error.message);
            alert('Erro de rede ou inesperado');
        }
    }
};
</script>

<template>
    <div class="flex w-full">
        <div class="w-200  mt-10 p-8 bg-white rounded shadow justify-center">
            <p class="text-2xl font-semibold mb-6">
                <span class="text-[#c0c0c0]">Entidades &gt;</span>
                <span class="text-[#00000]"> Adicionar Entidade</span>
            </p>

            <form @submit.prevent="submitForm" class="space-y-4 ">
                <div>
                    <label class="block text-sm font-medium">Nome da Entidade</label>
                    <input v-model="form.e_nome" class="input" />
                    <span v-if="errors.e_nome" class="text-red-500 text-sm">{{ errors.e_nome }}</span>
                </div>

                <div>
                    <label class="block text-sm font-medium">Email</label>
                    <input v-model="form.e_email" type="email" class="input" />
                    <span v-if="errors.e_email" class="text-red-500 text-sm">{{ errors.e_email }}</span>
                </div>

                <div>
                    <label class="block text-sm font-medium">NIF</label>
                    <input v-model="form.e_nif" class="input" />
                    <span v-if="errors.e_nif" class="text-red-500 text-sm">{{ errors.e_nif }}</span>
                </div>

                <div>
                    <label class="block text-sm font-medium">Contacto</label>
                    <input v-model="form.e_contacto" class="input" />
                    <span v-if="errors.e_contacto" class="text-red-500 text-sm">{{ errors.e_contacto }}</span>
                </div>

                <div>
                    <label class="block text-sm font-medium">Morada</label>
                    <input v-model="form.e_morada" class="input" />
                    <span v-if="errors.e_morada" class="text-red-500 text-sm">{{ errors.e_morada }}</span>
                </div>

                <div>
                    <label class="block text-sm font-medium">Ordem</label>
                    <input v-model="form.e_ordem" class="input" />
                    <span v-if="errors.e_ordem" class="text-red-500 text-sm">{{ errors.e_ordem }}</span>
                </div>

                <button type="submit" class="bg-[#ffA500] text-white py-2 px-4 rounded hover:bg-[#ffA500]-100">
                    Registar
                </button>

                <p v-if="successMessage" class="text-green-600 mt-4">{{ successMessage }}</p>
            </form>
        </div>
    </div>
</template>

<style scoped>
.input {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #ccc;
    border-radius: 0.375rem;
}
</style>
