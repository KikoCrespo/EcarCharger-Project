<script setup>
import { ref, computed, onMounted } from 'vue'
import ConfirmModal from './ConfirmModal.vue'
import RequestDetailModal from './RequestDetailModal.vue'
import ActionsListHeader from './ActionsListHeader.vue'
import api from '@/interceptors/axiosInterceptor'

import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue'
import { ArrowDownTrayIcon, PlusIcon, ChevronDownIcon, UserCircleIcon } from '@heroicons/vue/24/outline'
//import { c } from 'vite/dist/node/moduleRunnerTransport.d-CXw_Ws6P'

const searchQuery = ref('')
const selectAll = ref(false)
const showModal = ref(false);
const modalTitle = ref('');
const modalMessage = ref('');
const modalAction = ref('');
const requests = ref([])
const selectedRequest = ref(null);
const showRequestModal = ref(false);
const desiredState = ref(null);





onMounted(async () => {
    try {
        const response = await api.get('/frota/requisicoes/listar/')

        if (response.data && Array.isArray(response.data.requisicoes)) {
            requests.value = response.data.requisicoes;
        } else {
            console.error('Formato de dados inválido recebido da API.');
        }
    } catch (error) {
        console.error('Erro ao comunicar com a base de dados:', error);
    }
})


const filteredRequests = computed(() => {
    return requests.value.filter(request =>
        request.r_utilizador.first_name?.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        request.r_utilizador.last_name?.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        request.r_veiculo.v_matricula?.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
})

const toggleSelectAll = () => {
    filteredRequests.value.forEach(request => {
        request.checked = selectAll.value;
    })
}

const actionsOpen = ref(false);

const toogleActions = () => {
    actionsOpen.value = !actionsOpen.value;
}

const filtersOpen = ref(false);

const toogleFilters = () => {
    filtersOpen.value = !filtersOpen.value;
}

const roleOpen = ref(false);

const toogleRole = () => {
    roleOpen.value = !roleOpen.value;
}

function getSelectedRequest() {
    return requests.value.find(request => request.checked)
}

function openRequestDetail(request) {
    this.selectedRequest = request;
    this.showRequestModal = true;
}

function openModal(type) {
    if (type === 1) {
        modalTitle.value = 'Confirmar Requisição'
        modalMessage.value = 'Tens a certeza que queres aceitar a requisição?'
        modalAction.value = 'Confirmar'
        desiredState.value = 2 // Aceite
        selectedRequest.value = getSelectedRequest(); // Define a requisição selecionada
    } else if (type === 2) {
        modalTitle.value = 'Rejeitar Requisição'
        modalMessage.value = 'Tens a certeza que queres rejeitar esta requisição?'
        modalAction.value = 'Rejeitar'
        desiredState.value = 3 // Rejeitada
        selectedRequest.value = getSelectedRequest();
    } else if (type === 3) {
        modalTitle.value = 'Confirmar o Termino da requisição'
        modalMessage.value = 'Tens a certeza que queres terminar esta requisição?'
        modalAction.value = 'Terminar'
        desiredState.value = 4 // Terminado
        selectedRequest.value = getSelectedRequest();
    }else if(type === 4){
        modalTitle.value = 'Requisição já rejeitada'
        modalMessage.value = 'A requisição já se encontra rejeitada.'
        modalAction.value = 'Fechar'
        desiredState.value = null // Não aplicável
        selectedRequest.value = getSelectedRequest();
    }else if(type === 5){
        modalTitle.value = 'Requisição já terminada'
        modalMessage.value = 'A requisição já se encontra terminada.'
        modalAction.value = 'Fechar'
        desiredState.value = null // Não aplicável
        selectedRequest.value = getSelectedRequest();
    }
    else {
        console.error('Tipo de modal desconhecido:', type);
        return;
    }
    showModal.value = true
}

async function confirmAction(selectedRequest) {
    console.log('requisição selecionada:', selectedRequest);
    console.log('estado desejado:', desiredState.value);

    if (!selectedRequest || !desiredState.value) {
        console.error('Nenhuma requisição selecionada ou estado desejado não definido.');
        return;
    }
    
    if(selectedRequest.r_estado === 4) {
        openModal(5);
        return;
    }

    if(selectedRequest.r_estado === desiredState.value) {
        console.warn('A requisição já está no estado desejado.');
        openModal(4); // Modal de aviso
        return;
    }
    if(selectedRequest.r_estado === 3 && desiredState.value === 3) {
        openModal(4);
        return;
    }
    

    try {
        const response = await api.put('/frota/requisicoes/alterar_estado/', {
            requisicao_id: selectedRequest.id,
            novo_estado: desiredState.value
        });

        console.log('Requisição atualizada:', response.data);

        const index = requests.value.findIndex(req => req.id === selectedRequest.id);
        if (index !== -1) {
            requests.value[index].r_estado = desiredState.value;
            requests.value[index].r_estado_display = desiredState.value === 2 ? 'Aprovada'
                : desiredState.value === 3 ? 'Rejeitada'
                    : desiredState.value === 4 ? 'Terminada'
                        : 'Pendente';
        }

    } catch (error) {

        console.error('Erro ao atualizar requisição:', error);
    } finally {
        showModal.value = false;
        selectedRequest.value = null;
        desiredState.value = null;
    }
}


function closeModal() {
    showModal.value = false
    selectedRequest.value = null;
}
</script>

<template>

    <div class="flex justify-between bg-white p-4 rounded-lg shadow-sm">
        <div class="flex flex-col md:flex-row items-center justify-between">
            <ActionsListHeader />
        </div>
        <div>

            <span class="sm:ml-3">
                <button @click="toogleActions" id="dropdownActionButton" data-dropdown-toggle="dropdownAction"
                    class="inline-flex items-center rounded-md  px-3 py-2 text-sm font-semibold text-gray-900 border border-extra-soft-orange focus:outline-none hover:border-soft-orange focus:ring-2 focus:ring-soft-orange">
                    <ChevronDownIcon class="mr-1.5 -ml-0.5 size-5 transition-transform duration-300"
                        :class="{ 'rotate-180': actionsOpen }" aria-hidden="true" />
                    Ações
                </button>
            </span>
            <div id="dropdownAction"
                class="z-10 hidden bg-white divide-y divide-soft-orange rounded-lg shadow-sm w-44 mt-2">
                <ul class="py-1 text-sm text-gray-900" aria-labelledby="dropdownActionButton">
                    <li>
                        <button @click="() => { openModal(1); }"
                            class="block w-full text-left px-4 py-2 hover:text-gray-500">
                            Aceitar
                        </button>
                    </li>
                    <li>
                        <button @click="() => { openModal(2); }"
                            class="block w-full text-left px-4 py-2 hover:text-gray-500">
                            Rejeitar
                        </button>
                    </li>
                </ul>
                <button @click="() => { openModal(3); }"
                    class="block w-full text-left px-4 py-2 text-gray-700 hover:text-gray-500">
                    Terminar
                </button>
            </div>



            <span class="sm:ml-3">
                <button
                    class="inline-flex items-center rounded-md  px-3 py-2 text-sm font-semibold text-gray-900 border border-extra-soft-orange focus:outline-none hover:border-soft-orange focus:ring-2 focus:ring-soft-orange">
                    <ArrowDownTrayIcon class="mr-1.5 -ml-0.5 size-5" aria-hidden="true" />
                    Exportar
                </button>
            </span>
        </div>

    </div>


    <div class="relative h-full max-h-[73vh] overflow-x-auto shadow-md sm:rounded-lg p-3 bg-white mt-4 shadow-sm">

        <div class="flex items-center justify-start flex-wrap md:flex-nowrap space-y-4 md:space-y-0 pb-4">
            <!-- Search -->
            <div class="relative">
                <div class="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none">
                    <svg class="w-4 h-4 text-gray-900" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
                        viewBox="0 0 20 20">
                        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z" />
                    </svg>
                </div>
                <input v-model="searchQuery" type="text" id="table-search-users"
                    class="block p-2 ps-10 text-sm rounded-lg w-80 bg-transparent border-extra-soft-orange hover:border-soft-orange focus:ring-soft-orange placeholder-gray-500 text-gray-900"
                    placeholder="Procurar Requisições" />
            </div>

            <span class="sm:ml-3 p-4">
                <button @click="toogleFilters" id="dropdownFilterButton" data-dropdown-toggle="dropdownFilter"
                    class="inline-flex items-center rounded-md  px-3 py-2 text-sm font-semibold text-gray-900 border border-extra-soft-orange focus:outline-none hover:border-soft-orange focus:ring-2 focus:ring-soft-orange">
                    <ChevronDownIcon class="mr-1.5 -ml-0.5 size-5 transition-transform duration-300"
                        :class="{ 'rotate-180': filtersOpen }" aria-hidden="true" />
                    Estado
                </button>
            </span>
            <div id="dropdownFilter"
                class="z-10 hidden bg-white divide-y divide-soft-orange rounded-lg shadow-sm w-44 mt-2 mr-4">
                <ul class="py-1 text-sm text-gray-900" aria-labelledby="dropdownFilterButton">
                    <li>
                        <div class="flex block w-full text-left px-4 py-2 items-center">
                            <input id="push-everything" name="push-notifications" type="radio"
                                class="relative size-4 appearance-none rounded-full border border-gray-300 bg-white before:absolute before:inset-1 before:rounded-full before:bg-white not-checked:before:hidden checked:border-soft-orange checked:bg-soft-orange focus-visible:outline-2 focus-visible:outline-offset-2  disabled:border-gray-300 disabled:bg-gray-100 disabled:before:bg-gray-400 " />
                            <label for="push-everything"
                                class="ml-2 block text-sm/6 font-medium text-gray-900">Pendente</label>
                        </div>
                    </li>
                    <li>
                        <div class="flex block w-full text-left px-4 py-2 items-center">
                            <input id="accept-request" name="push-notifications" type="radio"
                                class="relative size-4 appearance-none rounded-full border border-gray-300 bg-white before:absolute before:inset-1 before:rounded-full before:bg-white not-checked:before:hidden checked:border-soft-orange checked:bg-soft-orange focus-visible:outline-2 focus-visible:outline-offset-2  disabled:border-gray-300 disabled:bg-gray-100 disabled:before:bg-gray-400 " />
                            <label for="accept-request"
                                class="ml-2 block text-sm/6 font-medium text-gray-900">Aceite</label>
                        </div>
                    </li>
                    <li>
                        <div class="flex block w-full text-left px-4 py-2 items-center">
                            <input id="refuse-request" name="push-notifications" type="radio" checked=""
                                class="relative size-4 appearance-none rounded-full border border-gray-300 bg-white before:absolute before:inset-1 before:rounded-full before:bg-white not-checked:before:hidden checked:border-soft-orange checked:bg-soft-orange focus-visible:outline-2 focus-visible:outline-offset-2  disabled:border-gray-300 disabled:bg-gray-100 disabled:before:bg-gray-400 " />
                            <label for="refuse-request"
                                class="ml-2 block text-sm/6 font-medium text-gray-900">Terminado</label>
                        </div>
                    </li>
                </ul>
            </div>
            <div id="dropdownRole"
                class="z-10 hidden bg-white divide-y divide-soft-orange rounded-lg shadow-sm w-44 mt-2 mr-4">
                <ul class="py-1 text-sm text-gray-900" aria-labelledby="dropdownRoleButton">
                    <li>
                        <label class="flex block w-full text-left px-4 py-2">
                            <input type="checkbox"
                                class="h-5 w-5 text-amber-600 border border-soft-orange rounded focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-soft-orange disabled:border-gray-300 disabled:bg-gray-100 disabled:checked:bg-gray-100" />
                            <span class="ml-2">Recursos Humanos</span>
                        </label>
                    </li>
                    <li>
                        <label class="flex block w-full text-left px-4 py-2">
                            <input type="checkbox"
                                class="h-5 w-5 text-amber-600 border border-soft-orange rounded focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-soft-orange disabled:border-gray-300 disabled:bg-gray-100 disabled:checked:bg-gray-100" />
                            <span class="ml-2">Engenharia</span>
                        </label>
                    </li>
                    <li>
                        <label class="flex block w-full text-left px-4 py-2">
                            <input type="checkbox"
                                class="h-5 w-5 text-amber-600 border border-soft-orange rounded focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-soft-orange disabled:border-gray-300 disabled:bg-gray-100 disabled:checked:bg-gray-100" />
                            <span class="ml-2">Marketing</span>
                        </label>
                    </li>
                    <li>
                        <label class="flex block w-full text-left px-4 py-2">
                            <input type="checkbox"
                                class="h-5 w-5 text-amber-600 border border-soft-orange rounded focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-soft-orange disabled:border-gray-300 disabled:bg-gray-100 disabled:checked:bg-gray-100" />
                            <span class="ml-2">TI</span>
                        </label>
                    </li>
                    <li>
                        <label class="flex block w-full text-left px-4 py-2">
                            <input type="checkbox"
                                class="h-5 w-5 text-amber-600 border border-soft-orange rounded focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-soft-orange disabled:border-gray-300 disabled:bg-gray-100 disabled:checked:bg-gray-100" />
                            <span class="ml-2">Financeiro</span>
                        </label>
                    </li>
                    <li>
                        <label class="flex block w-full text-left px-4 py-2">
                            <input type="checkbox"
                                class="h-5 w-5 text-amber-600 border border-soft-orange rounded focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-soft-orange disabled:border-gray-300 disabled:bg-gray-100 disabled:checked:bg-gray-100" />
                            <span class="ml-2">Operações</span>
                        </label>
                    </li>
                </ul>
            </div>




        </div>

        <!-- Tabela Scroll com header fixo -->
        <div class="max-h-96 overflow-y-auto">
            <table class="w-full text-sm text-left text-gray-500">
                <thead class="text-xs text-gray-900 uppercase bg-extra-soft-orange sticky top-0">
                    <tr>
                        <th scope="col" class="p-4">
                            <div class="flex items-center">
                                <input id="checkbox-all-search" type="checkbox" v-model="selectAll"
                                    @change="toggleSelectAll"
                                    class="w-4 h-4 text-soft-orange border-gray-300 rounded-sm focus:ring-soft-orange focus:ring-2">
                            </div>
                        </th>
                        <th class="px-6 py-3">Utilizador</th>
                        <th class="px-6 py-3">Veiculo</th>
                        <th class="px-6 py-3">Matricula</th>
                        <th class="px-6 py-3">Data Inicio</th>
                        <th class="px-6 py-3">Data Fim</th>
                        <th class="px-6 py-3">Estado</th>
                        <th class="px-6 py-3">Informações</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="request in filteredRequests" :key="request.id" class="border-b border-soft-orange">
                        <td class="p-4">
                            <input type="checkbox" v-model="request.checked" class="w-4 h-4 text-soft-orange" />
                        </td>

                        <td class="px-6 py-4 text-gray-900">{{ request.r_utilizador.first_name }}
                            {{ request.r_utilizador.last_name }}</td>
                        <td class="px-6 py-4 text-gray-900">{{ request.r_veiculo.v_marca }} {{
                            request.r_veiculo.v_modelo }}</td>
                        <td class="px-6 py-4 text-gray-900">{{ request.r_veiculo.v_matricula }}</td>
                        <td class="px-6 py-4 text-gray-900">{{ request.r_data_inicio }}</td>
                        <td v-if="request.r_data_fim" class="px-6 py-4 text-gray-900" placeholder="-">{{
                            request.r_data_fim }}</td>
                        <td v-else class="px-6 py-4 text-gray-900">-- // --</td>
                        <td class="px-6 py-4 text-gray-900">
                            <div class="flex items-center">
                                <div class="h-2.5 w-2.5 rounded-full me-2" :class="request.r_estado_display === 'Aprovada' ? 'bg-green-500' :
                                        request.r_estado_display === 'Pendente' ? 'bg-yellow-500' :
                                            request.r_estado_display === 'Terminada' ? 'bg-gray-300' :
                                                'bg-red-500'
                                " </div>
                                    {{ request.r_estado_display }}
                                </div>
                        </td>
                        <td class="px-6 py-4">
                            <button @click="openRequestDetail(request)"
                                class="text-soft-orange hover:text-gray-500 focus:outline-none">
                                ver
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

    <ConfirmModal :open="showModal" :title="modalTitle" :message="modalMessage" :action="modalAction"
        @close="showModal = false" v-if="selectedRequest" :request="selectedRequest"
        @confirm="confirmAction(selectedRequest)" />

    <RequestDetailModal v-if="selectedRequest" :show="showRequestModal" :request="selectedRequest"
        @update:show="showRequestModal = $event" @close="closeModal()" />

</template>

<style scoped>
/* Scrollbar customizada opcional */
::-webkit-scrollbar {
    width: 20px;
}

::-webkit-scrollbar-thumb {
    background-color: #d4d4d4;
    border-radius: 10px;
    background-clip: content-box;
    border: 5px solid transparent;
}
</style>
