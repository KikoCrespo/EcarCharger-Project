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
               class="block p-2 ps-10 text-sm rounded-lg w-80 bg-transparent duration-300 border-extra-soft-orange hover:border-soft-orange focus:ring-soft-orange placeholder-gray-500 text-gray-900"
               placeholder="Pesquisar veículos" />
      </div>
      <div>
        <button
            class="bg-extra-soft-orange hover:bg-soft-orange duration-300 text-sm font-semibold text-gray-900 px-4 py-2 rounded-lg flex items-center gap-2"
            @click="showFilterModal = true"
        >
          <FilterIcon class="h-5 w-5" />
          <span>Filtrar</span>
        </button>
      </div>
    </div>
  </div>

  <!-- Filtros ativos -->
  <div v-if="activeFilters.length > 0" class="flex flex-wrap gap-2 mb-4">
    <div
        v-for="(filter, index) in activeFilters"
        :key="index"
        class="bg-orange-100 text-orange-800 px-3 py-1 rounded-full text-sm flex items-center gap-1"
    >
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
      <div class="text-gray-500 text-sm mb-1">Disponíveis</div>
      <div class="text-2xl font-semibold text-green-600">{{ availableVehicles }}</div>
    </div>
    <div class="bg-white rounded-lg shadow p-4 border border-gray-100">
      <div class="text-gray-500 text-sm mb-1">Em Uso</div>
      <div class="text-2xl font-semibold text-orange-500">{{ inUseVehicles }}</div>
    </div>
    <div class="bg-white rounded-lg shadow p-4 border border-gray-100">
      <div class="text-gray-500 text-sm mb-1">Em Manutenção</div>
      <div class="text-2xl font-semibold text-red-500">{{ maintenanceVehicles }}</div>
    </div>
  </div>

  <!-- Lista de veículos -->
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 max-h-[600px] overflow-y-auto">
    <div
        v-for="vehicle in filteredVehicles"
        :key="vehicle.id"
        class="bg-white rounded-lg border border-gray-200 overflow-hidden hover:shadow-md transition-shadow"
    >
      <div class="relative">
        <img src="../assets/img/carroteste.png" :alt="vehicle.model" class="w-full h-48 object-contain bg-gradient-to-t from-extra-soft-orange to-orange-50" />
        <div
            class="absolute top-3 right-3 px-2 py-1 rounded-full text-xs font-medium"
            :class="{
                      'bg-green-100 text-green-800': vehicle.status === 'available',
                      'bg-orange-100 text-orange-800': vehicle.status === 'in-use',
                      'bg-red-100 text-red-800': vehicle.status === 'maintenance'
                    }"
        >
          {{ getStatusText(vehicle.status) }}
        </div>
      </div>

      <div class="p-4">
        <div class="flex justify-between items-start mb-2">
          <div>
            <h3 class="font-bold text-lg">{{ vehicle.plate }}</h3>
            <p class="text-gray-600">{{ vehicle.type }}</p>
          </div>
          <button
              class="text-gray-500 hover:text-gray-700"
              @click="toggleFavorite(vehicle.id)"
          >
            <component :is="vehicle.favorite ? 'HeartIconSolid' : 'HeartIcon'" class="h-5 w-5" />
          </button>
        </div>

        <div class="grid grid-cols-2 gap-2 mb-4">
          <div class="flex items-center gap-1 text-gray-600">
            <UsersIcon class="h-4 w-4" />
            <span>{{ vehicle.seats }}</span>
          </div>
          <div class="flex items-center gap-1 text-gray-600">
            <BoltIcon class="h-4 w-4" />
            <span>{{ vehicle.power }} kw</span>
          </div>
          <div class="flex items-center gap-1 text-gray-600">
            <Cog class="h-4 w-4" />
            <span>{{ vehicle.transmission }}</span>
          </div>
          <div class="flex items-center gap-1 text-gray-600">
            <FuelIcon class="h-4 w-4" />
            <span>{{ vehicle.fuel }}</span>
          </div>
        </div>

        <div class="flex gap-2">
          <button
              class="flex-1 bg-gray-100 hover:bg-gray-200 duration-300 text-gray-800 py-2 rounded-lg flex items-center justify-center gap-1"
              @click="viewVehicleDetails(vehicle.id)"
          >
            <EyeIcon class="h-4 w-4" />
            <span>Visualizar</span>
          </button>
          <button
              class="flex-1 bg-extra-soft-orange hover:bg-soft-orange duration-300  text-gray-900 py-2 rounded-lg flex items-center justify-center gap-1"
              :disabled="vehicle.status !== 'available'"
              :class="{ 'opacity-50 cursor-not-allowed': vehicle.status !== 'available' }"
              @click="openRequestModal(vehicle)"
          >
            <CarIcon class="h-4 w-4" />
            <span>Requisição</span>
          </button>

        </div>
      </div>
    </div>
    <RequestVehicleModal
        v-if="selectedVehicle"
        :show="showRequestModal"
        :vehicle="selectedVehicle"
        @update:show="showRequestModal = $event"
        @submit-request="handleRequest"
    />
  </div>

  <FilterModal
      :show="showFilterModal"
      :filters="filters"
      @update:show="showFilterModal = $event"
      @apply-filters="applyFilters"
      @reset-filters="resetFilters"
  />




</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import RequestVehicleModal from "@/components/RequestVehicleModal.vue";
import FilterModal from "@/components/FilterVehiclesModal.vue";
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
const selectedVehicle = ref(null);

// Filtros
const filters = ref({
  types: {
    suv: false,
    citadino: false,
    sedan: false,
    utilitario: false
  },
  status: {
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

// Dados simulados
const vehicles = ref([
  {
    id: 1,
    plate: 'AA - 12 - BQ',
    type: 'Citadino',
    model: 'Mercedes-Benz Classe A',
    image: 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-NGPn4YUZ9EMbcdOZrhDtwFjnQ3Ku22.png',
    seats: 4,
    power: 360,
    transmission: 'Automático',
    fuel: 'Gasolina',
    status: 'available',
    favorite: false
  },
  {
    id: 2,
    plate: 'BB - 34 - ZX',
    type: 'SUV',
    model: 'Mercedes-Benz GLE',
    image: 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-NGPn4YUZ9EMbcdOZrhDtwFjnQ3Ku22.png',
    seats: 5,
    power: 360,
    transmission: 'Automático',
    fuel: 'Diesel',
    status: 'in-use',
    favorite: true
  },
  {
    id: 3,
    plate: 'CC - 56 - YW',
    type: 'SUV',
    model: 'Mercedes-Benz GLC',
    image: 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-NGPn4YUZ9EMbcdOZrhDtwFjnQ3Ku22.png',
    seats: 5,
    power: 320,
    transmission: 'Automático',
    fuel: 'Híbrido',
    status: 'available',
    favorite: false
  },
  {
    id: 4,
    plate: 'DD - 78 - VU',
    type: 'Sedan',
    model: 'Mercedes-Benz Classe C',
    image: 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-NGPn4YUZ9EMbcdOZrhDtwFjnQ3Ku22.png',
    seats: 5,
    power: 280,
    transmission: 'Automático',
    fuel: 'Diesel',
    status: 'maintenance',
    favorite: false
  },
  {
    id: 5,
    plate: 'EE - 90 - TS',
    type: 'Utilitário',
    model: 'Mercedes-Benz Vito',
    image: 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-NGPn4YUZ9EMbcdOZrhDtwFjnQ3Ku22.png',
    seats: 7,
    power: 240,
    transmission: 'Manual',
    fuel: 'Diesel',
    status: 'available',
    favorite: false
  },
  {
    id: 6,
    plate: 'FF - 12 - RQ',
    type: 'SUV',
    model: 'Mercedes-Benz GLA',
    image: 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-NGPn4YUZ9EMbcdOZrhDtwFjnQ3Ku22.png',
    seats: 5,
    power: 300,
    transmission: 'Automático',
    fuel: 'Gasolina',
    status: 'in-use',
    favorite: false
  },
  {
    id: 7,
    plate: 'GG - 34 - PO',
    type: 'Citadino',
    model: 'Mercedes-Benz Classe B',
    image: 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-NGPn4YUZ9EMbcdOZrhDtwFjnQ3Ku22.png',
    seats: 4,
    power: 260,
    transmission: 'Automático',
    fuel: 'Híbrido',
    status: 'available',
    favorite: false
  },
  {
    id: 8,
    plate: 'HH - 56 - NM',
    type: 'Sedan',
    model: 'Mercedes-Benz Classe E',
    image: 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-NGPn4YUZ9EMbcdOZrhDtwFjnQ3Ku22.png',
    seats: 5,
    power: 400,
    transmission: 'Automático',
    fuel: 'Diesel',
    status: 'available',
    favorite: false
  },
  {
    id: 9,
    plate: 'II - 78 - LK',
    type: 'SUV',
    model: 'Mercedes-Benz GLS',
    image: 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-NGPn4YUZ9EMbcdOZrhDtwFjnQ3Ku22.png',
    seats: 7,
    power: 450,
    transmission: 'Automático',
    fuel: 'Gasolina',
    status: 'maintenance',
    favorite: false
  },
  {
    id: 10,
    plate: 'JJ - 90 - JI',
    type: 'Utilitário',
    model: 'Mercedes-Benz Sprinter',
    image: 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-NGPn4YUZ9EMbcdOZrhDtwFjnQ3Ku22.png',
    seats: 9,
    power: 280,
    transmission: 'Manual',
    fuel: 'Diesel',
    status: 'available',
    favorite: false
  },
  {
    id: 11,
    plate: 'KK - 12 - HG',
    type: 'Sedan',
    model: 'Mercedes-Benz Classe S',
    image: 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-NGPn4YUZ9EMbcdOZrhDtwFjnQ3Ku22.png',
    seats: 5,
    power: 500,
    transmission: 'Automático',
    fuel: 'Híbrido',
    status: 'in-use',
    favorite: false
  },
  {
    id: 12,
    plate: 'LL - 34 - FE',
    type: 'SUV',
    model: 'Mercedes-Benz EQC',
    image: 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-NGPn4YUZ9EMbcdOZrhDtwFjnQ3Ku22.png',
    seats: 5,
    power: 420,
    transmission: 'Automático',
    fuel: 'Elétrico',
    status: 'available',
    favorite: false
  }
]);

// Computed properties
const filteredVehicles = computed(() => {
  let result = vehicles.value;

  // Aplicar pesquisa
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    result = result.filter(vehicle =>
        vehicle.plate.toLowerCase().includes(query) ||
        vehicle.type.toLowerCase().includes(query) ||
        vehicle.model.toLowerCase().includes(query)
    );
  }

  // Aplicar filtros
  const hasTypeFilters = Object.values(filters.value.types).some(value => value);
  const hasStatusFilters = Object.values(filters.value.status).some(value => value);
  const hasSeatsFilters = Object.values(filters.value.seats).some(value => value);

  if (hasTypeFilters) {
    result = result.filter(vehicle => {
      const type = vehicle.type.toLowerCase();
      return (
          (filters.value.types.suv && type === 'suv') ||
          (filters.value.types.citadino && type === 'citadino') ||
          (filters.value.types.sedan && type === 'sedan') ||
          (filters.value.types.utilitario && type === 'utilitário')
      );
    });
  }

  if (hasStatusFilters) {
    result = result.filter(vehicle => {
      return (
          (filters.value.status.available && vehicle.status === 'available') ||
          (filters.value.status.inUse && vehicle.status === 'in-use') ||
          (filters.value.status.maintenance && vehicle.status === 'maintenance')
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



const totalVehicles = computed(() => vehicles.value.length);
const availableVehicles = computed(() => vehicles.value.filter(v => v.status === 'available').length);
const inUseVehicles = computed(() => vehicles.value.filter(v => v.status === 'in-use').length);
const maintenanceVehicles = computed(() => vehicles.value.filter(v => v.status === 'maintenance').length);

// Métodos
function getStatusText(status) {
  switch (status) {
    case 'available': return 'Disponível';
    case 'in-use': return 'Em Uso';
    case 'maintenance': return 'Manutenção';
    default: return status;
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

  if (filter === 'Disponível') filters.value.status.available = false;
  if (filter === 'Em Uso') filters.value.status.inUse = false;
  if (filter === 'Em Manutenção') filters.value.status.maintenance = false;

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

  // Status
  if (filters.value.status.available) activeFilters.value.push('Disponível');
  if (filters.value.status.inUse) activeFilters.value.push('Em Uso');
  if (filters.value.status.maintenance) activeFilters.value.push('Em Manutenção');

  // Lugares
  if (filters.value.seats.two) activeFilters.value.push('2 Lugares');
  if (filters.value.seats.four) activeFilters.value.push('4 Lugares');
  if (filters.value.seats.five) activeFilters.value.push('5 Lugares');
  if (filters.value.seats.seven) activeFilters.value.push('7+ Lugares');

  currentPage.value = 1;
}

function resetFilters() {
  filters.value = {
    types: { suv: false, citadino: false, sedan: false, utilitario: false },
    status: { available: false, inUse: false, maintenance: false },
    seats: { two: false, four: false, five: false, seven: false }
  };
  activeFilters.value = [];
}

// Modal de requisição
const openRequestModal = (vehicle) => {
  if (vehicle.status !== 'available') return;
  selectedVehicle.value = vehicle;
  showRequestModal.value = true;
};

const handleRequest = (requestData) => {
  console.log('Requisição confirmada:', requestData);
  showRequestModal.value = false;
  selectedVehicle.value = null;
  alert(`Veículo ${requestData.vehicleId} requisitado com sucesso!`);
};


</script>