<template>
    <div
        class="sidebar h-full p-2 w-[300px] overflow-y-auto text-center bg-background-orange flex flex-col justify-between">
        <div>
            <div class="text-xl">
                <div class="p-2.5 mt-1 flex items-center justify-center">
                    <img src="../assets/img/hmvdomologo.png" alt="HMVDOMO" class="h-18 w-auto">
                </div>
            </div>

            <div
                class="p-2.5 mt-20 flex items-center rounded-md px-4 duration-300 cursor-pointer hover:bg-soft-orange text-gray-900">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                    stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round"
                        d="m2.25 12 8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25" />
                </svg>
                <span class="text-[15px] ml-4 font-bold text-gray-900">Dashboard</span>
            </div>


            <div class="p-2.5 mt-3 flex items-center rounded-md px-4 duration-300 cursor-pointer hover:bg-soft-orange text-gray-900"
                @click="toggleFrota">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="size-6">
                    <path fill="currentColor"
                        d="M7.7 3.25a2.25 2.25 0 0 0-2.107 1.46L4.64 7.25H2.75a.75.75 0 0 0 0 1.5h1.33l-.044.116A2.25 2.25 0 0 0 2.5 11v7a1.5 1.5 0 0 0 3 0v-1h13v1a1.5 1.5 0 0 0 3 0v-7c0-.993-.643-1.835-1.535-2.134l-.043-.116h1.328a.75.75 0 0 0 0-1.5h-1.89l-.951-2.54a2.25 2.25 0 0 0-2.107-1.46zM20 11v4.5h-3.25V14a2.25 2.25 0 0 0-2.25-2.25h-5A2.25 2.25 0 0 0 7.25 14v1.5H4V11a.75.75 0 0 1 .75-.75h14.5A.75.75 0 0 1 20 11m-1.68-2.25H5.68l1.316-3.513A.75.75 0 0 1 7.7 4.75h8.602a.75.75 0 0 1 .702.487zm-3.07 6.75h-6.5V14a.75.75 0 0 1 .75-.75h5a.75.75 0 0 1 .75.75z" />
                </svg>
                <div class="flex justify-between w-full items-center">
                    <span class="text-[15px] ml-4 text-black font-bold">Frota</span>
                    <span class="text-sm transition-transform duration-300" :class="{ 'rotate-180': carsOpen }">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                            stroke="currentColor" class="size-5">
                            <path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
                        </svg>
                    </span>
                </div>
            </div>

            <!--Submenu da frota-->
            <div class="text-left text-sm mt-2 w-4/5 mx-auto text-black font-bold" v-show="carsOpen">

                <router-link to="/frota/meus-veiculos"
                    class="block cursor-pointer p-2 hover:bg-soft-orange rounded-md mt-1">
                    Meus Veículos
                </router-link>
                <router-link to="/frota/consultar"
                    class="block cursor-pointer p-2 hover:bg-soft-orange rounded-md mt-1">
                    Consultar Frota
                </router-link>
                <router-link to="/frota/adicionar-veiculo" v-if="user_data.type"
                    class="block cursor-pointer p-2 hover:bg-soft-orange rounded-md mt-1">
                    Adicionar Veículo
                </router-link>
            </div>



            <div v-if="user_data.type"
                class="p-2.5 mt-3 flex items-center rounded-md px-4 duration-300 cursor-pointer hover:bg-soft-orange text-gray-900"
                @click="toggleStatistic">
                <svg xmlns="http://www.w3.org/2000/svg" class="size-6" viewBox="0 0 24 24">
                    <g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"
                        stroke-width="2">
                        <path stroke-miterlimit="5.759" d="M3 3v16a2 2 0 0 0 2 2h16" />
                        <path stroke-miterlimit="5.759" d="m7 14l4-4l4 4l6-6" />
                        <path d="M18 8h3v3" />
                    </g>
                </svg>
                <div class="flex justify-between w-full items-center">
                    <span class="text-[15px] ml-4 text-black font-bold">Estatísticas</span>
                    <span class="text-sm transition-transform duration-300" :class="{ 'rotate-180': statisticOpen }">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                            stroke="currentColor" class="size-5">
                            <path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
                        </svg>
                    </span>
                </div>
            </div>
            <!--Submenu da estatisticas-->
            <div v-if="user_data.type" class="text-left text-sm mt-2 w-4/5 mx-auto text-black font-bold"
                v-show="statisticOpen">
                <h1 class="cursor-pointer p-2 hover:bg-soft-orange rounded-md mt-1">
                    Pessoais
                </h1>
                <h1 class="cursor-pointer p-2 hover:bg-soft-orange rounded-md mt-1">
                    Funcionários
                </h1>
                <h1 class="cursor-pointer p-2 hover:bg-soft-orange rounded-md mt-1">
                    Todas
                </h1>
            </div>

            <div v-else
                class="p-2.5 mt-3 flex items-center rounded-md px-4 duration-300 cursor-pointer hover:bg-soft-orange text-gray-900">
                <svg xmlns="http://www.w3.org/2000/svg" class="size-6" viewBox="0 0 24 24">
                    <g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"
                        stroke-width="2">
                        <path stroke-miterlimit="5.759" d="M3 3v16a2 2 0 0 0 2 2h16" />
                        <path stroke-miterlimit="5.759" d="m7 14l4-4l4 4l6-6" />
                        <path d="M18 8h3v3" />
                    </g>
                </svg>
                <span class="text-[15px] ml-4 font-bold text-gray-900">Estatísticas</span>
            </div>



            <div v-if="user_data.type"
                class="p-2.5 mt-3 flex items-center rounded-md px-4 duration-300 cursor-pointer hover:bg-soft-orange text-gray-900"
                @click="toggleUsers">
                <svg xmlns="http://www.w3.org/2000/svg" class="size-6" viewBox="0 0 24 24">
                    <path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"
                        stroke-width="2"
                        d="M5 7a4 4 0 1 0 8 0a4 4 0 1 0-8 0M3 21v-2a4 4 0 0 1 4-4h4a4 4 0 0 1 4 4v2m1-17.87a4 4 0 0 1 0 7.75M21 21v-2a4 4 0 0 0-3-3.85" />
                </svg>
                <div class="flex justify-between w-full items-center">
                    <span class="text-[15px] ml-4 text-black font-bold">Utilizadores</span>
                    <span class="text-sm transition-transform duration-300" :class="{ 'rotate-180': usersOpen }">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                            stroke="currentColor" class="size-5">
                            <path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
                        </svg>
                    </span>
                </div>
            </div>

            <!-- Submenu Utilizadores -->
            <div v-if="user_data.type" class="text-left text-sm mt-2 w-4/5 mx-auto text-black font-bold"
                v-show="usersOpen">
                <router-link to="/utilizadores/listar"
                    class="block cursor-pointer p-2 hover:bg-soft-orange rounded-md mt-1">
                    Listar
                </router-link>
                <router-link to="/utilizadores/adicionar"
                    class="block cursor-pointer p-2 hover:bg-soft-orange rounded-md mt-1">
                    Adicionar utilizador
                </router-link>
                <router-link to="/utilizadores/pedidos"
                    class="block cursor-pointer p-2 hover:bg-soft-orange rounded-md mt-1">
                    Pedidos de alteração
                </router-link>
            </div>

            <!-- menu de postos de carregamento -->
            <div v-if="user_data.type"
                class="p-2.5 mt-3 flex items-center rounded-md px-4 duration-300 cursor-pointer hover:bg-soft-orange text-gray-900"
                @click="togglePostos">
                <fuel-icon class="size-6" />
                <div class="flex justify-between w-full items-center">
                    <span class="text-[15px] ml-4 text-black font-bold">Postos</span>
                    <span class="text-sm transition-transform duration-300" :class="{ 'rotate-180': PostosOpen }">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                            stroke="currentColor" class="size-5">
                            <path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
                        </svg>
                    </span>
                </div>
            </div>

            <!-- Submenu Postos -->
            <div v-if="user_data.type" class="text-left text-sm mt-2 w-4/5 mx-auto text-black font-bold"
                v-show="PostosOpen">
                <router-link to="/postos/listar" class="block cursor-pointer p-2 hover:bg-soft-orange rounded-md mt-1">
                    Listar
                </router-link>
                <router-link v-if="user_data.supa" to="/postos/adicionar"
                    class="block cursor-pointer p-2 hover:bg-soft-orange rounded-md mt-1">
                    Adicionar Posto
                </router-link>
                <router-link v-if="user_data.supa" to="/postos/iot/adicionar"
                    class="block cursor-pointer p-2 hover:bg-soft-orange rounded-md mt-1">
                    Adicionar IOT
                </router-link>
            </div>

            <!-- Menu entidade -->
            <div v-if="user_data.supa"
                class="p-2.5 mt-3 flex items-center rounded-md px-4 duration-300 cursor-pointer hover:bg-soft-orange text-gray-900" @click="toggleEntidades">
                <BuildingOffice2Icon class="size-6" />
                <div class="flex justify-between w-full items-center">
                    <span class="text-[15px] ml-4 text-black font-bold">Entidades</span>
                    <span class="text-sm transition-transform duration-300" :class="{ 'rotate-180': EntidadesOpen }">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                            stroke="currentColor" class="size-5">
                            <path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
                        </svg>
                    </span>
                </div>
            </div>

            <!-- Submenu Postos -->
            <div v-if="user_data.supa" class="text-left text-sm mt-2 w-4/5 mx-auto text-black font-bold"
                v-show="EntidadesOpen">
                <router-link to="/postos/listar" class="block cursor-pointer p-2 hover:bg-soft-orange rounded-md mt-1">
                    Listar
                </router-link>
                <router-link  to="/entidades/adicionar"
                    class="block cursor-pointer p-2 hover:bg-soft-orange rounded-md mt-1">
                    Adicionar Entidade
                </router-link>
            </div>



        </div>
        <div>
            <div
                class="p-2.5 mt-3 flex items-center rounded-md px-4 duration-300 cursor-pointer hover:bg-soft-orange text-gray-900">
                <svg xmlns="http://www.w3.org/2000/svg" class="size-6" viewBox="0 0 24 24">
                    <path fill="currentColor"
                        d="m19.59 15.5l-1.82-1.3c.3-1.08.32-2.25 0-3.42l1.82-1.28L18.14 7l-2.03.92c-.79-.8-1.79-1.42-2.96-1.71L12.95 4h-2.9l-.2 2.21c-1.17.29-2.17.91-2.96 1.71L4.86 7L3.41 9.5l1.82 1.28c-.32 1.17-.3 2.34 0 3.42l-1.82 1.3L4.86 18l2.03-.93c.79.79 1.79 1.39 2.96 1.7l.2 2.23h2.9l.2-2.23c1.17-.31 2.17-.91 2.96-1.7l2.03.93l1.45-2.5M13.5 3c.27 0 .5.2.5.46l.18 2.04c.76.28 1.44.69 2.05 1.18l1.85-.87c.23-.12.52-.04.66.19l2 3.5c.14.21.06.5-.16.65l-1.67 1.17c.13.8.12 1.59 0 2.36l1.67 1.17c.22.15.3.44.16.65l-2 3.5c-.14.21-.43.29-.66.17l-1.85-.86c-.61.49-1.29.89-2.05 1.19l-.18 2c0 .29-.23.5-.5.5h-4a.5.5 0 0 1-.5-.5l-.18-2c-.76-.3-1.44-.7-2.05-1.19l-1.85.86c-.23.12-.52.04-.66-.17l-2-3.5c-.14-.21-.06-.5.16-.65l1.67-1.17c-.12-.77-.13-1.56 0-2.36l-1.67-1.17c-.22-.15-.3-.44-.16-.65l2-3.5c.14-.23.43-.31.66-.19l1.85.87c.61-.49 1.29-.9 2.05-1.18L9 3.46c0-.26.23-.46.5-.46h4m-2 6a3.5 3.5 0 0 1 3.5 3.5a3.5 3.5 0 0 1-3.5 3.5A3.5 3.5 0 0 1 8 12.5A3.5 3.5 0 0 1 11.5 9m0 1A2.5 2.5 0 0 0 9 12.5a2.5 2.5 0 0 0 2.5 2.5a2.5 2.5 0 0 0 2.5-2.5a2.5 2.5 0 0 0-2.5-2.5Z" />
                </svg>
                <span class="text-[15px] ml-4 text-black font-bold">Definições</span>
            </div>
            <div
                class="p-2.5 mt-3 flex items-center rounded-md px-4 duration-300 cursor-pointer hover:bg-soft-orange text-gray-900">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                    stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round"
                        d="M15.75 9V5.25A2.25 2.25 0 0 0 13.5 3h-6a2.25 2.25 0 0 0-2.25 2.25v13.5A2.25 2.25 0 0 0 7.5 21h6a2.25 2.25 0 0 0 2.25-2.25V15m3 0 3-3m0 0-3-3m3 3H9" />
                </svg>
                <span class="text-[15px] ml-4 text-black font-bold">Terminar sessão</span>
            </div>
        </div>



    </div>
</template>

<script setup>
import { ref } from 'vue';
import { defineProps } from 'vue';
import { FuelIcon } from 'lucide-vue-next';
import { BuildingOffice2Icon } from '@heroicons/vue/24/outline';


const props = defineProps({
    user_data: {
        type: Object,
        required: true
    }
});

const PostosOpen = ref(false);
const usersOpen = ref(false);
const carsOpen = ref(false);
const statisticOpen = ref(false);
const EntidadesOpen = ref(false);

const toggleStatistic = () => {
    statisticOpen.value = !statisticOpen.value;
};

const toggleFrota = () => {
    carsOpen.value = !carsOpen.value;
};

const toggleUsers = () => {
    usersOpen.value = !usersOpen.value;
};

const togglePostos = () => {
    PostosOpen.value = !PostosOpen.value;
};


const toggleEntidades = () => {
    EntidadesOpen.value = !EntidadesOpen.value;
};
</script>
