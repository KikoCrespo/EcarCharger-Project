<script setup>
import { reactive, onMounted } from 'vue';
import api from '@/interceptors/axiosInterceptor'
import { ref } from 'vue';
import SideBar from '@/components/SideBar.vue';
import NavBar from '@/components/NavBar.vue';
import { ChevronRightIcon } from '@heroicons/vue/24/outline'
import IconHome from "@/assets/icons/IconHome.vue";

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
        api.get('/perfil/', {
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
    } else {
        state.isAuthenticated = false;
        console.log('Token não encontrado. Utilizador não autenticado.');
    }
});




</script>

<template>

    <div class="flex h-screen">
        <SideBar v-if="state.user" :user_data="state.user" class="hidden sm:flex " />

        <div class="w-full">
            <NavBar v-if="state.user" :user_data="state.user" class="" />
            <header class="mt-5 px-6 ">
                <ul class="flex items-center space-x-2">
                    <li>
                        <a href="/"
                            class="text-gray-900 font-medium flex items-center hover:text-soft-orange duration-300">
                            <IconHome size="18" class="mr-0.5" />
                            Home
                        </a>
                    </li>
                    <template v-for="(segment, index) in currentUrl" :key="index">
                        <li class="flex items-center">
                            <ChevronRightIcon class="w-4 h-4 text-gray-500 dark:text-gray-400" />
                            <span :class="[
                                'text-base font-medium',
                                index === currentUrl.length - 1
                                    ? 'text-soft-orange'
                                    : 'text-gray-400 hover:text-soft-orange duration-300 '
                            ]">
                                {{ decodeURIComponent(segment) }}
                            </span>
                        </li>
                    </template>
                </ul>
            </header>
            <main class="mt-5 px-5 h-[85vh] overflow-auto">
                <router-view v-if="state.user" :user_data="state.user" />
            </main>
        </div>

    </div>





</template>
