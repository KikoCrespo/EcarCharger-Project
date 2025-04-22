<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const form = ref({
    name: '',
    email: '',
    nif: '',
    contacto: '',
    morada: '',
    ordem: ''
});

const errors = ref({
    name: '',
    email: '',
    nif: '',
    contacto: '',
    morada: '',
    ordem: ''
});

const successMessage = ref('');
const router = useRouter();

const submitForm = async () => {
    errors.value = {
        name: '',
        email: '',
        nif: '',
        contacto: '',
        morada: '',
        ordem: ''
    };
    successMessage.value = '';

    let hasError = false;

    if (!form.value.name) {
        errors.value.name = 'Nome é obrigatório.';
        hasError = true;
    }
    if (!form.value.email) {
        errors.value.email = 'Email é obrigatório.';
        hasError = true;
    }
    if (!form.value.nif) {
        errors.value.nif = 'NIF é obrigatório.';
        hasError = true;
    }
    if (!form.value.contacto) {
        errors.value.contacto = 'Contacto é obrigatório.';
        hasError = true;
    }
    if (!form.value.morada) {
        errors.value.morada = 'Morada é obrigatória.';
        hasError = true;
    }
    if (!form.value.ordem) {
        errors.value.ordem = 'Ordem é obrigatória.';
        hasError = true;
    }

    if (hasError) return;

    try {
        await axios.post('http://localhost:8000/api/entidade/', form.value);
        successMessage.value = 'Entidade registada com sucesso!';
        // router.push('/entidades'); // Se quiseres redirecionar depois
    } catch (error) {
        console.error(error);
        successMessage.value = 'Erro ao registar entidade.';
    }
};
</script>

<template>
    <div class="max-w-xl mx-auto mt-10 p-8 bg-white rounded shadow">
        <h2 class="text-2xl font-semibold mb-6 text-center">Registar Entidade</h2>

        <form @submit.prevent="submitForm" class="space-y-4">
            <div>
                <label class="block text-sm font-medium">Nome da Entidade</label>
                <input v-model="form.name" class="input" />
                <span v-if="errors.name" class="text-red-500 text-sm">{{ errors.name }}</span>
            </div>

            <div>
                <label class="block text-sm font-medium">Email</label>
                <input v-model="form.email" type="email" class="input" />
                <span v-if="errors.email" class="text-red-500 text-sm">{{ errors.email }}</span>
            </div>

            <div>
                <label class="block text-sm font-medium">NIF</label>
                <input v-model="form.nif" class="input" />
                <span v-if="errors.nif" class="text-red-500 text-sm">{{ errors.nif }}</span>
            </div>

            <div>
                <label class="block text-sm font-medium">Contacto</label>
                <input v-model="form.contacto" class="input" />
                <span v-if="errors.contacto" class="text-red-500 text-sm">{{ errors.contacto }}</span>
            </div>

            <div>
                <label class="block text-sm font-medium">Morada</label>
                <input v-model="form.morada" class="input" />
                <span v-if="errors.morada" class="text-red-500 text-sm">{{ errors.morada }}</span>
            </div>

            <div>
                <label class="block text-sm font-medium">Ordem</label>
                <input v-model="form.ordem" class="input" />
                <span v-if="errors.ordem" class="text-red-500 text-sm">{{ errors.ordem }}</span>
            </div>

            <button type="submit" class="bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700">
                Registar
            </button>

            <p v-if="successMessage" class="text-green-600 mt-4">{{ successMessage }}</p>
        </form>
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
