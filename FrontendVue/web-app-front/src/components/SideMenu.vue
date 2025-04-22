<template>
    <div class="w-64 bg-orange-400 text-white p-4">
        <h2 class="text-2xl font-semibold mb-6">HMV</h2>
        <ul>
            <li class="mb-4">
                <router-link to="/home" class="text-white hover:text-gray-300">Home</router-link>
            </li>
            <li class="mb-4">
                <option value="" class="text-white hover:text-gray-300" @click="toggleUser">
                    Utilizadores
                </option>
                <!-- Option ocultas -->
                <router-link to="/entidades/adicionar" v-if="isOptionVisibleUser" value="">Lista
                    Utilizadores
                </router-link>
            </li>
            <li class="mb-4">
                <option value="" class="text-white hover:text-gray-300" @click="toggleEntidade">
                    Entidades
                </option>
                <!-- Option ocultas -->
                <router-link to="/entidades/adicionar" v-if="isOptionVisibleEntidade" value="">Adicionar
                    Entidade
                </router-link>
                <router-link to="/entidades/lista" v-if="isOptionVisibleEntidade" value="">Lista
                    Entidade
                </router-link>
            </li>
            
        </ul>
    </div>
</template>

<script setup>
import { ref } from 'vue';

// Estado para controlar a visibilidade do option
const isOptionVisibleEntidade = ref(false);
const isOptionVisibleUser = ref(false);

// Função para alternar a visibilidade do option
const toggleEntidade = () => {
    isOptionVisibleEntidade.value = !isOptionVisibleEntidade.value;
};
const toggleUser = () => {
    isOptionVisibleUser.value = !isOptionVisibleUser.value;
};
</script>

<style scoped>
/* Adicione seus estilos personalizados aqui */
</style>