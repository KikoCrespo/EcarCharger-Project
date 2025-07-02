<script setup>
import { ref, computed, onMounted } from 'vue'
import ConfirmModal from './ConfirmModal.vue'
import ActionsListHeader from './ActionsListHeader.vue'
import api from '@/interceptors/axiosInterceptor'

import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue'
import { ArrowDownTrayIcon, PlusIcon, ChevronDownIcon, UserCircleIcon } from '@heroicons/vue/24/outline'

const searchQuery = ref('')
const selectAll = ref(false)
const selectedUser = ref(null)

const showModal = ref(false);
const modalTitle = ref('');
const modalMessage = ref('');
const modalAction = ref('');

const users = ref([])

const props = defineProps({
  user: {
    type: Object,
    required: true
  },
  state: {
    type: Object,
    required: true
  }
})


onMounted(async () => {
  try {
    api.get('/utilizadores/listar/')
      .then((response) => {
        console.log('Resposta da API:', response);

        if (response.data && Array.isArray(response.data.users)) {
          users.value = response.data.users;
          console.log('Utilizadores:', users.value);
        } else {
          console.error('Formato de dados inválido recebido da API.');
        }
      })
      .catch((error) => {
        console.error('Erro ao recuperar dados dos utilizadores:', error);
        state.isAuthenticated = false;
      });
  } catch (error) {
    console.error('Erro ao comunicar com a base de dados:', error);
  }
});


const filteredUsers = computed(() => {
  return users.value.filter(user =>
    user.first_name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    user.email.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

const toggleSelectAll = () => {
  filteredUsers.value.forEach(user => {
    user.checked = selectAll.value;
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

function getSelectedUsers() {
  return users.value.filter(user => user.checked)
}

function openModal(type) {
  console.log('Utilizador selecionado:', selectedUser.value);
  if (type === 1) {
    modalTitle.value = 'Confirmar Promoção'
    modalMessage.value = 'Tens a certeza que queres promover este utilizador?'
    modalAction.value = 'Promover'
  } else if (type === 2) {
    modalTitle.value = 'Confirmar Ativação'
    modalMessage.value = 'Tens a certeza que queres ativar esta conta?'
    modalAction.value = 'Ativar'
  } else if (type === 3) {
    modalTitle.value = 'Confirmar Inativação'
    modalMessage.value = 'Tens a certeza que queres inativar esta conta?'
    modalAction.value = 'Inativar'
  } else if (type == 4) {
    modalTitle.value = 'Confirmar Despromoção'
    modalMessage.value = 'Tens a certeza que queres despromover este utilizador?'
    modalAction.value = 'Despromover'
  } else if (type === 5) {
    modalTitle.value = 'Ação não permitida'
    modalMessage.value = 'Apenas utilizadores não administradores podem ser promovidos.'
    modalAction.value = 'Fechar'
  } else if (type === 6) {
    modalTitle.value = 'Ação não permitida'
    modalMessage.value = 'Este utilizador já se encontra ativo'
    modalAction.value = 'Fechar'
  } else if (type === 7) {
    modalTitle.value = 'Ação não permitida'
    modalMessage.value = 'Este utilizador já se encontra inativo'
    modalAction.value = 'Fechar'
  } else if (type === 8) {
    modalTitle.value = 'Ação não permitida'
    modalMessage.value = 'Este utilizador já se encontra despromovido'
    modalAction.value = 'Fechar'
  } else {
    modalTitle.value = 'Ação Desconhecida'
    modalMessage.value = 'Nenhuma ação foi selecionada.'
    modalAction.value = 'Fechar'
  }
  showModal.value = true
}

async function confirmAction() {
  const selected = getSelectedUsers();
  if (!selected.length) {
    alert("Nenhum utilizador selecionado.");
    return;
  }

  for (const userSelected of selected) {
    let payload = {};
    let endpoint = ``;
    if (modalAction.value === 'Promover') {
      if (userSelected.is_staff === false) {
        payload = {};
        endpoint = `/utilizadores/promover/${userSelected.id}/`;
      } else {
        openModal(5);
        return;
      }
    } else if (modalAction.value === 'Ativar') {
      console.log('Ativar conta do utilizador:', userSelected);
      if (userSelected.is_active === false) {
        payload = { novo_estado: true };
        endpoint = `/utilizadores/estado/${userSelected.id}/`;
      } else {
        openModal(6)
        return;
      }
    } else if (modalAction.value === 'Inativar') {
      console.log('inativar conta do utilizador:', userSelected);
      if (userSelected.is_active === true) {
        payload = { novo_estado: false };
        endpoint = `/utilizadores/estado/${userSelected.id}/`;
      } else {
        openModal(7);
        return;
      }
    } else if (modalAction.value === 'Despromover') {
      if (userSelected.is_staff === true) {
        payload = {};
        endpoint = `/utilizadores/despromover/${userSelected.id}/`;
      } else {
        openModal(8);
        return;
      }

    } else {
      console.warn("Ação desconhecida:", modalAction.value);
      return;
    }

    try {
      await api.patch(endpoint, payload, {
      });
      console.log(`Utilizador ${userSelected.email} atualizado com sucesso.`);
    } catch (error) {
      console.error(`Erro ao atualizar utilizador ${userSelected.email}:`, error);
    }
  }
  showModal.value = false;
  await fetchUsers();
}

async function fetchUsers() {
  try {

    const response = await api.get('/utilizadores/listar/', {
    });
    users.value = response.data.users || [];
  } catch (error) {
    console.error('Erro ao recuperar dados dos utilizadores:', error);
  }
}



function closeModal() {
  showModal.value = false
}
</script>

<template v-if="user.is_staff">

  <div class="flex justify-between bg-white p-4 rounded-lg shadow-sm mb-4">
    <div class="flex flex-col md:flex-row items-center justify-between">
      <ActionsListHeader />
    </div>
    <div>
      <span class="sm:ml-3">
        <router-link to="/utilizadores/adicionar" class="inline-flex items-center rounded-md bg-extra-soft-orange px-3 py-2 text-sm font-semibold text-gray-900 shadow-xs hover:bg-soft-orange duration-300">
          <PlusIcon class="mr-1.5 -ml-0.5 size-5" aria-hidden="true" />
          Adicionar utilizador
        </router-link>
      </span>

      <span class="sm:ml-3">
        <button @click="toogleActions" id="dropdownActionButton" data-dropdown-toggle="dropdownAction"
          class="inline-flex items-center rounded-md  px-3 py-2 text-sm font-semibold text-gray-900 border border-extra-soft-orange focus:outline-none hover:border-soft-orange focus:ring-2 focus:ring-soft-orange">
          <ChevronDownIcon class="mr-1.5 -ml-0.5 size-5 transition-transform duration-300"
            :class="{ 'rotate-180': actionsOpen }" aria-hidden="true" />
          Ações
        </button>
      </span>
      <div id="dropdownAction" class="z-10 hidden bg-white divide-y divide-soft-orange rounded-lg shadow-sm w-44 mt-2">
        <button class="block w-full text-left px-4 py-2 hover:text-gray-500">
          Editar
        </button>
        <ul class="py-1 text-sm text-gray-900" aria-labelledby="dropdownActionButton">
          <li>
            <button @click="openModal(2)" class="block w-full text-left px-4 py-2 hover:text-gray-500">
              Ativar Conta
            </button>
          </li>
          <li>
            <button @click="openModal(3)" class="block w-full text-left px-4 py-2 hover:text-gray-500">
              Inativar Conta
            </button>
          </li>
        </ul>
        <ul class="py-1 text-sm text-gray-900" >
          <li>
            <button @click="openModal(1)" class="block w-full text-left px-4 py-2 hover:text-gray-500">
              Promover
            </button>
          </li>
          <li>
            <button @click="openModal(4)" class="block w-full text-left px-4 py-2 hover:text-gray-500">
              Despromover
            </button>
          </li>
        </ul>

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


  <div class="relative h-full max-h-[73vh] overflow-x-auto shadow-md sm:rounded-lg p-3 bg-white">

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
          placeholder="Pesquisar por utilizadores" />
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
              <label for="push-everything" class="ml-2 block text-sm/6 font-medium text-gray-900">Ativo</label>
            </div>
          </li>
          <li>
            <div class="flex block w-full text-left px-4 py-2 items-center">
              <input id="push-everything" name="push-notifications" type="radio"
                class="relative size-4 appearance-none rounded-full border border-gray-300 bg-white before:absolute before:inset-1 before:rounded-full before:bg-white not-checked:before:hidden checked:border-soft-orange checked:bg-soft-orange focus-visible:outline-2 focus-visible:outline-offset-2  disabled:border-gray-300 disabled:bg-gray-100 disabled:before:bg-gray-400 " />
              <label for="push-everything" class="ml-2 block text-sm/6 font-medium text-gray-900">Inativo</label>
            </div>
          </li>
          <li>
            <div class="flex block w-full text-left px-4 py-2 items-center">
              <input id="push-everything" name="push-notifications" type="radio" checked=""
                class="relative size-4 appearance-none rounded-full border border-gray-300 bg-white before:absolute before:inset-1 before:rounded-full before:bg-white not-checked:before:hidden checked:border-soft-orange checked:bg-soft-orange focus-visible:outline-2 focus-visible:outline-offset-2  disabled:border-gray-300 disabled:bg-gray-100 disabled:before:bg-gray-400 " />
              <label for="push-everything" class="ml-2 block text-sm/6 font-medium text-gray-900">Ambos</label>
            </div>
          </li>
        </ul>
      </div>
      <span class="sm:ml-3 p-4">
        <button @click="toogleRole" id="dropdownRoleButton" data-dropdown-toggle="dropdownRole"
          class="inline-flex items-center rounded-md  px-3 py-2 text-sm font-semibold text-gray-900 border border-extra-soft-orange focus:outline-none hover:border-soft-orange focus:ring-2 focus:ring-soft-orange">
          <ChevronDownIcon class="mr-1.5 -ml-0.5 size-5 transition-transform duration-300"
            :class="{ 'rotate-180': roleOpen }" aria-hidden="true" />
          Departamento
        </button>
      </span>
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
                <input id="checkbox-all-search" type="checkbox" v-model="selectAll" @change="toggleSelectAll"
                  class="w-4 h-4 text-soft-orange border-gray-300 rounded-sm focus:ring-soft-orange focus:ring-2">
              </div>
            </th>
            <th class="px-6 py-3">Nome</th>
            <th class="px-6 py-3">Departamento</th>
            <th class="px-6 py-3">Data de registo</th>
            <th class="px-6 py-3">Estado</th>
            <th class="px-6 py-3">Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in filteredUsers" :key="user.id" class="border-b border-soft-orange">
            <td class="p-4">
              <input type="checkbox" v-model="user.checked"
                class="w-4 h-4 text-soft-orange border-gray-300 rounded-sm focus:ring-soft-orange focus:ring-2" />
            </td>
            <td class="flex items-center px-6 py-4 text-gray-900 whitespace-nowrap">
              <img v-if="user.u_img_perfil" class="w-12 h-12 rounded-full" :src="user.u_img_perfil" alt="image" />
              <UserCircleIcon v-else class="w-12 h-12 text-gray-300" aria-hidden="true" />
              <div class="ps-3">
                <div class="text-base font-semibold">{{ user.first_name }}</div>
                <div class="font-normal text-gray-500">{{ user.email }}</div>
              </div>
            </td>
            <td class="px-6 py-4 text-gray-900">{{ user.u_departamento }}</td>
            <td class="px-6 py-4 text-gray-900">{{ user.date_joined }}</td>
            <td class="px-6 py-4 text-gray-900">
              <div class="flex items-center">
                <div class="h-2.5 w-2.5 rounded-full me-2" :class="user.is_active ? 'bg-green-500' : 'bg-red-500'">
                </div>
                {{ user.is_active ? 'Ativo' : 'Inativo' }}
              </div>
            </td>
            <td class="px-6 py-4">
              <a href="#" class="font-medium text-blue-600 hover:underline">Visualizar</a>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <ConfirmModal :open="showModal" :title="modalTitle" :message="modalMessage" :action="modalAction"
    @close="showModal = false" @confirm="confirmAction" />
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
