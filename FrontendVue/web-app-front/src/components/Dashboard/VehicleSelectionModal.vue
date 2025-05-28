<template>
  <div v-if="modelValue" class="fixed inset-0 bg-gray-500/75 transition-opacity flex items-center justify-center z-50" @click.self="closeModal">
    <div class="bg-white rounded-lg w-11/12 max-w-2xl max-h-[90vh] flex flex-col shadow-xl">
      <div class="flex justify-between items-center p-4 border-b border-gray-200">
        <h3 class="text-lg font-semibold">Selecionar Veículo</h3>
        <button @click="closeModal" class="text-gray-500 hover:text-gray-700 focus:outline-none">
          <XIcon class="h-5 w-5" />
        </button>
      </div>

      <div class="p-5 overflow-y-auto flex-1">
        <div class="relative mb-4">
          <input
              type="text"
              v-model="searchQuery"
              placeholder="Pesquisar veículo..."
              class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
          />
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
        </div>

        <div class="flex flex-col gap-3 max-h-96 overflow-y-auto">
          <div
              v-for="vehicle in filteredVehicles"
              :key="vehicle.id"
              class="flex items-center p-3 border rounded-lg cursor-pointer transition-all duration-200"
              :class="{
              'border-gray-200 hover:bg-gray-50 hover:border-gray-300': !(selectedVehicle && selectedVehicle.id === vehicle.id),
              'bg-orange-50 border-orange-500': selectedVehicle && selectedVehicle.id === vehicle.id
            }"
              @click="selectVehicle(vehicle)"
          >
            <div class="w-16 h-16 rounded-md overflow-hidden flex-shrink-0 mr-4">
              <img :src="vehicle.image" :alt="vehicle.model" class="w-full h-full object-cover" />
            </div>
            <div class="flex-1">
              <div class="font-semibold">{{ vehicle.model }}</div>
              <div class="text-sm text-gray-600">{{ vehicle.plate }}</div>
            </div>
            <div
                class="px-3 py-1 rounded-full text-xs font-medium whitespace-nowrap"
                :class="{
                'bg-green-100 text-green-800': vehicle.status === 'available',
                'bg-red-100 text-red-800': vehicle.status === 'in-use',
                'bg-blue-100 text-blue-800': vehicle.status === 'maintenance'
              }"
            >
              {{ getStatusText(vehicle.status) }}
            </div>
          </div>

          <div v-if="filteredVehicles.length === 0" class="text-center py-5 text-gray-500 italic">
            Nenhum veículo encontrado com os critérios de pesquisa.
          </div>
        </div>
      </div>

      <div class="flex justify-end gap-3 p-4 border-t border-gray-200">
        <button
            class="px-4 py-2 border border-gray-300 rounded-lg font-medium text-gray-700 hover:bg-gray-50 transition-colors"
            @click="closeModal"
        >
          Cancelar
        </button>
        <button
            class="px-4 py-2 rounded-lg font-medium text-white transition-colors"
            :class="{
            'bg-orange-500 hover:bg-orange-600': selectedVehicle && selectedVehicle.status === 'available',
            'bg-gray-400 cursor-not-allowed': !selectedVehicle || selectedVehicle.status !== 'available'
          }"
            :disabled="!selectedVehicle || selectedVehicle.status !== 'available'"
            @click="confirmSelection"
        >
          Iniciar Carregamento
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { XIcon } from 'lucide-vue-next';

const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  vehicles: {
    type: Array,
    required: true
  },
  selectedStation: {
    type: Object,
    default: null
  }
});

const emit = defineEmits(['update:modelValue', 'select-vehicle']);

const searchQuery = ref('');
const selectedVehicle = ref(null);

const filteredVehicles = computed(() => {
  if (!searchQuery.value) {
    return props.vehicles;
  }

  const query = searchQuery.value.toLowerCase();
  return props.vehicles.filter(vehicle =>
      vehicle.model.toLowerCase().includes(query) ||
      vehicle.plate.toLowerCase().includes(query)
  );
});

function getStatusText(status) {
  switch (status) {
    case 'available':
      return 'Disponível';
    case 'in-use':
      return 'Em uso';
    case 'maintenance':
      return 'Manutenção';
    default:
      return status;
  }
}

function selectVehicle(vehicle) {
  selectedVehicle.value = vehicle;
}

function closeModal() {
  emit('update:modelValue', false);
  // Reset state when closing
  searchQuery.value = '';
  selectedVehicle.value = null;
}

function confirmSelection() {
  if (selectedVehicle.value && selectedVehicle.value.status === 'available') {
    emit('select-vehicle', {
      vehicle: selectedVehicle.value,
      station: props.selectedStation
    });
    closeModal();
  }
}

// Reset selection when modal opens
watch(() => props.modelValue, (newValue) => {
  if (newValue) {
    selectedVehicle.value = null;
    searchQuery.value = '';
  }
});
</script>