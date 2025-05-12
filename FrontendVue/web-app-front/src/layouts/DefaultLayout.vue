<script setup>
import { reactive, onMounted } from 'vue';
import axios from 'axios';
import { ref } from 'vue';
import SideBar from '@/components/SideBar.vue';
import NavBar from '@/components/NavBar.vue';
import { ChevronRightIcon} from '@heroicons/vue/24/outline'

const state = reactive({
    isAuthenticated: false,
    user: null, 
});


const getUrl = () => {
    const url = window.location.href;
    const path = new URL(url).pathname;
    const urlParts = path.split('/').filter(part => part !== '');
    return urlParts;
};
const currentUrl = ref(getUrl());


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

    <div class="flex h-full">
        <SideBar v-if="state.user" :user_data="state.user" class="hidden sm:flex "/>
        
        <div class="w-full">
            <NavBar v-if="state.user" :user_data="state.user" class=""/>
            <header class="mt-5 px-6 "> 
                <ul class="flex items-center space-x-2">
                <li>
                    <a href="/" class="text-gray-900 font-medium flex items-center hover:text-soft-orange duration-300">
                    <svg width="15" height="15" viewBox="0 0 15 15" class="fill-current mr-2">
                        <path d="M13.35 14.65H10.22C9.52 14.65 8.94 14.07 8.94 13.37V10.82C8.94 10.56 8.73 10.35 8.48 10.35H6.55C6.29 10.35 6.08 10.56 6.08 10.82V13.35C6.08 14.05 5.5 14.63 4.81 14.63H1.63C0.93 14.63 0.35 14.05 0.35 13.35V5.24C0.35 4.9 0.54 4.57 0.84 4.39L6.97 0.51C7.29 0.3 7.73 0.3 8.06 0.51L14.19 4.39C14.49 4.57 14.65 4.9 14.65 5.24V13.33C14.65 14.07 14.07 14.65 13.35 14.65Z"/>
                    </svg>
                    Home
                    </a>
                </li>
                <template v-for="(segment, index) in currentUrl" :key="index">
                    <li class="flex items-center">
                    <ChevronRightIcon class="w-4 h-4 text-gray-500 dark:text-gray-400" />
                    <span
                        :class="[
                        'text-base font-medium',
                        index === currentUrl.length - 1
                            ? 'text-soft-orange'
                            : 'text-gray-400 hover:text-soft-orange duration-300 '
                        ]"
                    >
                        {{ decodeURIComponent(segment) }}
                    </span>
                    </li>
                </template>
                </ul>
            </header>
            <main class="mt-5 px-5 h-auto overflow-auto">
                <router-view v-if="state.user" :user_data="state.user"/>
            </main>
        </div>
        
    </div>
    

    
    
    
</template>


