<template>

  <div class="flex justify-end items-center mb-6">

    <div class="flex gap-3">
      <div class="relative">
        <div class="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none">
          <svg class="w-4 h-4 text-gray-900" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
            viewBox="0 0 20 20">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z" />
          </svg>
        </div>
        <input v-model="searchQuery" type="text" id="table-search-users"
          class="block p-2 ps-10 text-sm rounded-lg w-80  duration-300 bg-transparent border-extra-soft-orange hover:border-soft-orange focus:ring-soft-orange placeholder-gray-500 text-gray-900"
          placeholder="Pesquisar veículos" />
      </div>
      <div>
        <button
          class="bg-extra-soft-orange hover:bg-soft-orange duration-300 text-sm font-semibold text-gray-900 px-4 py-2 rounded-lg flex items-center gap-2"
          @click="showFilterModal = true">
          <FilterIcon class="h-5 w-5" />
          <span>Filtrar</span>
        </button>
      </div>
    </div>
  </div>

  <!-- Filtros ativos -->
  <div v-if="activeFilters.length > 0" class="flex flex-wrap gap-2 mb-4">
    <div v-for="(filter, index) in activeFilters" :key="index"
      class="bg-orange-100 text-orange-800 px-3 py-1 rounded-full text-sm flex items-center gap-1">
      {{ filter }}
      <XIcon class="h-4 w-4 cursor-pointer" @click="removeFilter(index)" />
    </div>
  </div>

  <!-- Status da frota -->
  <div class="grid grid-cols-4 gap-6 mb-8">
    <div class="bg-white rounded-lg shadow p-4 border border-gray-100">
      <div class="text-gray-500 text-sm mb-1">Total de Veículos</div>
      <div class="text-2xl font-semibold">{{ totalVehicles }}</div>
    </div>
    <div class="bg-white rounded-lg shadow p-4 border border-gray-100">
      <div class="text-gray-500 text-sm mb-1">Em Uso</div>
      <div class="text-2xl font-semibold text-green-600">{{ availableVehicles }}</div>
    </div>
    <div class="bg-white rounded-lg shadow p-4 border border-gray-100">
      <div class="text-gray-500 text-sm mb-1">Pendentes</div>
      <div class="text-2xl font-semibold text-orange-500">{{ PendingVehicles }}</div>
    </div>
    <div class="bg-white rounded-lg shadow p-4 border border-gray-100">
      <div class="text-gray-500 text-sm mb-1">Em Manutenção</div>
      <div class="text-2xl font-semibold text-red-500">{{ maintenanceVehicles }}</div>
    </div>
  </div>

  <!-- Lista de veículos -->
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 max-h-[600px] overflow-y-auto">
    <div v-for="vehicle in filteredVehicles" :key="vehicle.v_matricula"
      class="bg-white rounded-lg border border-gray-200 overflow-hidden hover:shadow-md transition-shadow">
      <div class="relative">
        <img src="../assets/img/Veiculoteste.png" :alt="vehicle.v_modelo"
          class="w-full h-48 object-contain bg-gradient-to-t from-extra-soft-orange to-orange-50" />
        <div class="absolute top-3 right-3 px-2 py-1 rounded-full text-xs font-medium" :class="{
          'bg-green-100 text-green-800': getVehicleRequestStatus(vehicle) === 'Aprovada',
          'bg-orange-100 text-orange-800': getVehicleRequestStatus(vehicle) === 'Pendente',
          'bg-red-100 text-red-800': vehicle.v_estado_display === 'Em Manutencao'
        }">
          <span v-if="vehicle.v_estado_display !== 'Em Manutencao'">{{ getStatusText(getVehicleRequestStatus(vehicle))}}</span>
          <span v-else>Em Manutenção</span>
        </div>
      </div>

      <div class="p-4">
        <div class="flex justify-between items-start mb-2">
          <div>
            <h3 class="font-bold text-lg">{{ vehicle.v_matricula }}</h3>
            <p class="text-gray-600">{{ vehicle.v_categoria_display }}</p>
          </div>
          <button class="text-gray-500 hover:text-gray-700" @click="toggleFavorite(vehicle.id)">
            <!--             <component :is="vehicle.favorite ? 'HeartIconSolid' : 'HeartIcon'" class="h-5 w-5" />
 --> </button>
        </div>

        <div class="grid grid-cols-2 gap-2 mb-4">
          <div class="flex items-center gap-1 text-gray-600">
            <UsersIcon class="h-4 w-4" />
            <span>{{ vehicle.v_assentos }}</span>
          </div>
          <div class="flex items-center gap-1 text-gray-600">
            <BoltIcon class="h-4 w-4" />
            <span>{{ vehicle.v_potencia }} kw</span>
          </div>
          <div class="flex items-center gap-1 text-gray-600">
            <Cog class="h-4 w-4" />
            <span>{{ vehicle.v_transmissao }}</span>
          </div>
          <div class="flex items-center gap-1 text-gray-600">
            <FuelIcon class="h-4 w-4" />
            <span>{{ vehicle.v_combustivel }}</span>
          </div>
        </div>

        <div class="flex gap-2">
          <button
            class="flex-1 bg-gray-100 hover:bg-gray-200 duration-300 text-gray-800 py-2 rounded-lg flex items-center justify-center gap-1"
            @click="openRequestModal(getVehicleRequest(vehicle))">
            <EyeIcon class="h-4 w-4" />
            <span>Visualizar</span>
          </button>
          <button
            class="flex-1 bg-extra-soft-orange hover:bg-soft-orange duration-300  text-gray-900 py-2 rounded-lg flex items-center justify-center gap-1"
            :disabled="getVehicleRequestStatus(vehicle) === 'Pendente'"
            :class="{ 'opacity-50 cursor-not-allowed': getVehicleRequestStatus(vehicle) === 'Pendente' }"
            @click="openFinishRequestModal(getVehicleRequest(vehicle))">
            <CarIcon class="h-4 w-4" />
            <span>Terminar Requisição</span>
          </button>

        </div>
      </div>
    </div>
    <EndVehicleRequesitionModal v-if="selectedRequest" :show="showFinishRequestModal" :request="selectedRequest"
      :vehicle="selectedVehicle" @update:show="showFinishRequestModal = $event" @submit-request="handleRequest" />

  </div>
  <RequestDetailModal v-if="selectedRequest" :show="showRequestModal" :request="selectedRequest"
    @update:show="showRequestModal = $event" @close="closeModal()" />

  <FilterModal :show="showFilterModal" :filters="filters" @update:show="showFilterModal = $event"
    @apply-filters="applyFilters" @reset-filters="resetFilters" />




</template>x

<script setup>
import { ref, computed, onMounted } from 'vue';
import EndVehicleRequesitionModal from "@/components/EndVehicleRequesitionModal.vue";
import FilterModal from "@/components/FilterVehiclesModal.vue";
import RequestDetailModal from "@/components/RequestDetailModal.vue";
import api from '@/interceptors/axiosInterceptor'
import {
  FilterIcon,
  XIcon,
  UsersIcon,
  BoltIcon,
  FuelIcon,
  EyeIcon,
  CarIcon,
  Cog,

} from 'lucide-vue-next';




// Estado
const searchQuery = ref('');
const currentPage = ref(1);
const itemsPerPage = 9;
const showFilterModal = ref(false);
const showRequestModal = ref(false);
const showFinishRequestModal = ref(false);
const selectedVehicle = ref(null);

const vehicles = ref([]);
const request = ref([]);
const selectedRequest = ref(null);

// Filtros
const filters = ref({
  types: {
    suv: false,
    citadino: false,
    sedan: false,
    utilitario: false,
    comercial: false
  },
  state: {
    available: false,
    inUse: false,
    maintenance: false
  },
  seats: {
    two: false,
    four: false,
    five: false,
    seven: false
  }
});

// Filtros ativos
const activeFilters = ref([]);


onMounted(async () => {
  try {

    api.get('/frota/requisicoes/utilizador/listar/', {
    })
      .then((response) => {
        console.log('Resposta da API:', response);

        if (response.data && Array.isArray(response.data.requisicoes)) {
          request.value = response.data.requisicoes;
          vehicles.value = request.value.filter(req => req.r_estado_display === 'Pendente' || req.r_estado_display === 'Aprovada').map(req => req.r_veiculo) || [];

          console.log('Requisições:', request.value);
          console.log('Veículos:', vehicles.value);
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


// Computed properties
const filteredVehicles = computed(() => {
  let result = vehicles.value;

  // Aplicar pesquisa
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    result = result.filter(vehicle =>
      vehicle.v_matricula.toLowerCase().includes(query) ||
      vehicle.v_categoria_display.toLowerCase().includes(query) ||
      vehicle.v_modelo.toLowerCase().includes(query)
    );
  }

  // Aplicar filtros
  const hasTypeFilters = Object.values(filters.value.types).some(value => value);
  const hasStatusFilters = Object.values(filters.value.state).some(value => value);
  const hasSeatsFilters = Object.values(filters.value.seats).some(value => value);

  if (hasTypeFilters) {
    result = result.filter(vehicle => {
      const type = vehicle.v_categoria_display.toLowerCase();
      return (
        (filters.value.types.suv && type === 'SUV') ||
        (filters.value.types.citadino && type === 'Citadino') ||
        (filters.value.types.sedan && type === 'Sedan') ||
        (filters.value.types.utilitario && type === 'Utilitario') ||
        (filters.value.types.comercial && type === 'Comercial')
      );
    });
  }

  if (hasStatusFilters) {
    result = result.filter(vehicle => {
      return (
        (filters.value.state.available && vehicle.v_estado === 1) ||
        (filters.value.state.inUse && vehicle.v_estado === 2) ||
        (filters.value.state.maintenance && vehicle.v_estado === 3)
      );
    });
  }

  if (hasSeatsFilters) {
    result = result.filter(vehicle => {
      return (
        (filters.value.seats.two && vehicle.seats === 2) ||
        (filters.value.seats.four && vehicle.seats === 4) ||
        (filters.value.seats.five && vehicle.seats === 5) ||
        (filters.value.seats.seven && vehicle.seats >= 7)
      );
    });
  }

  // Paginação
  const startIndex = (currentPage.value - 1) * itemsPerPage;
  return result.slice(startIndex, startIndex + itemsPerPage);
});


function getVehicleRequestStatus(vehicle) {
  const req = request.value.find(r => r.r_veiculo.v_matricula === vehicle.v_matricula);
  return req ? req.r_estado_display : null;
}

function getVehicleRequest(vehicle) {
  const req = request.value.find(r => r.r_veiculo.v_matricula === vehicle.v_matricula);
  return req ? req : null;
}

const totalVehicles = computed(() => vehicles.value.length);
const availableVehicles = computed(() => request.value.filter(r => r.r_estado_display === 'Aprovada').length);
const PendingVehicles = computed(() => request.value.filter(r => r.r_estado_display === 'Pendente').length);
const maintenanceVehicles = computed(() => vehicles.value.filter(v => v.v_estado === 'Em Manutencao').length);

// Métodos
function getStatusText(v_estado) {
  switch (v_estado) {
    case 1: return 'Disponível';
    case 2: return 'Em Uso';
    case 3: return 'Manutenção';
    default: return v_estado;
  }
}

function toggleFavorite(id) {
  const vehicle = vehicles.value.find(v => v.id === id);
  if (vehicle) vehicle.favorite = !vehicle.favorite;
}

function viewVehicleDetails(id) {
  console.log('Ver detalhes do veículo:', id);
}

function removeFilter(index) {
  const filter = activeFilters.value[index];
  activeFilters.value.splice(index, 1);

  if (filter === 'SUV') filters.value.types.suv = false;
  if (filter === 'Citadino') filters.value.types.citadino = false;
  if (filter === 'Sedan') filters.value.types.sedan = false;
  if (filter === 'Utilitário') filters.value.types.utilitario = false;
  if (filter === 'Comercial') filters.value.types.comercial = false;

  if (filter === 'Disponível') filters.value.state.available = false;
  if (filter === 'Em Uso') filters.value.state.inUse = false;
  if (filter === 'Em Manutenção') filters.value.state.maintenance = false;

  if (filter === '2 Lugares') filters.value.seats.two = false;
  if (filter === '4 Lugares') filters.value.seats.four = false;
  if (filter === '5 Lugares') filters.value.seats.five = false;
  if (filter === '7+ Lugares') filters.value.seats.seven = false;
}

function applyFilters(newFilters) {
  filters.value = JSON.parse(JSON.stringify(newFilters));

  // Atualizar filtros ativos
  activeFilters.value = [];

  // Tipos
  if (filters.value.types.suv) activeFilters.value.push('SUV');
  if (filters.value.types.citadino) activeFilters.value.push('Citadino');
  if (filters.value.types.sedan) activeFilters.value.push('Sedan');
  if (filters.value.types.utilitario) activeFilters.value.push('Utilitário');
  if (filters.value.types.comercial) activeFilters.value.push('Comercial');

  // Status
  if (filters.value.state.available) activeFilters.value.push('Disponível');
  if (filters.value.state.inUse) activeFilters.value.push('Em Uso');
  if (filters.value.state.maintenance) activeFilters.value.push('Em Manutenção');

  // Lugares
  if (filters.value.seats.two) activeFilters.value.push('2 Lugares');
  if (filters.value.seats.four) activeFilters.value.push('4 Lugares');
  if (filters.value.seats.five) activeFilters.value.push('5 Lugares');
  if (filters.value.seats.seven) activeFilters.value.push('7+ Lugares');

  currentPage.value = 1;
}

function resetFilters() {
  filters.value = {
    types: { suv: false, citadino: false, sedan: false, utilitario: false, comercial: false },
    state: { available: false, inUse: false, maintenance: false },
    seats: { two: false, four: false, five: false, seven: false }
  };
  activeFilters.value = [];
}

// Modal de finalização da requisição
const openFinishRequestModal = (request) => {
  selectedRequest.value = request;
  selectedVehicle.value = request.r_veiculo;
  showFinishRequestModal.value = true;
};

// Modal de detalhes da requisição
const openRequestModal = (request) => {
  selectedRequest.value = request;
  showRequestModal.value = true;
};

function closeModal() {
  showRequestModal.value = false
  selectedRequest.value = null;
}

const handleRequest = async (requestData) => {
  console.log('Dados da requisição:', requestData);
  const reason = requestData.reason;
  const request = requestData.request;

  try {
    const response = await api.put('/frota/requisicoes/alterar_estado/', {
      requisicao_id: request.id,
      novo_estado: 4,
      motivo_terminacao: reason
    });

    console.log('Requisição atualizada:', response.data);
  } catch (error) {

    console.error('Erro ao terminar requisição:', error);

  } finally {
    showFinishRequestModal.value = false;
    selectedRequest.value = null;
    selectedVehicle.value = null;
    window.location.reload();
  }
};


</script>