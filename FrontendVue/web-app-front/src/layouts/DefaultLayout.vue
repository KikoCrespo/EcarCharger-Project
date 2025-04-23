<script setup>
import { reactive, onMounted } from 'vue';
import axios from 'axios';
import SideMenu from '@/components/SideMenu.vue';
import { ref } from 'vue';
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
    <SideAndNavBarDesktop v-if="state.user" :user_data="state.user" />
    

</template>


