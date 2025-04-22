<script setup>
import { reactive, onMounted } from 'vue';
import axios from 'axios';
import SideMenu from '@/components/SideMenu.vue';
import SideAndNavBarDesktop from '@/components/SideAndNavBarDesktop.vue'

const state = reactive({
    isAuthenticated: false,
    user: null, 
});

// Função para verificar o token e obter os dados do utilizador
onMounted(() => {
    const token = sessionStorage.getItem('access');
    if (token) {
        axios
            .get('http://localhost:8000/api/perfil/', {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
            .then((response) => {
                // Atualiza o estado com as informações do utilizador
                state.isAuthenticated = true;
                state.user = response.data.user;
                console.log('Dados do utilizador:', state.user);
            })
            .catch((error) => {
                console.error('Erro ao recuperar dados do utilizador:', error);
                state.isAuthenticated = false;
            });
    }else {
        state.isAuthenticated = false;
        console.log('Token não encontrado. Utilizador não autenticado.');
    }
});

</script>

<template>
    <SideAndNavBarDesktop/>
    
    <SideMenu id="SideMenu" class="h-full" />

    <!-- Header -->
    <header id="cabecalho" class="w-full h-16 flex items-center justify-between p-6 bg-white shadow z-10">
        <!-- Verifica se o state.user está definido antes de tentar acessar o nome -->
        <p class="text-gray-600" v-if="state.user && state.user.first_name">Olá, {{ state.user.first_name }}</p>
        <p v-else>Carregando...</p>
        <p v-if="state.user">Ultimo acesso, {{ state.user.ultimo_registo}}</p>

    </header>

</template>


