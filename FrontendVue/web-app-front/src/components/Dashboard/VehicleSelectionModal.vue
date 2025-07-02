<template>
  <div v-if="modelValue" class="fixed inset-0 bg-gray-500/50 backdrop-blur-sm transition-opacity flex items-center justify-center z-50 p-4" @click.self="closeModal">
    <div class="bg-white rounded-xl w-full max-w-4xl max-h-[85vh] flex flex-col shadow-2xl">
      <!-- Header -->
      <div class="flex justify-between items-center px-6 py-4 border-b border-gray-200">
        <h3 class="text-xl font-semibold text-gray-900">Selecionar Veículo</h3>
        <button @click="closeModal" class="text-gray-500 hover:text-gray-700 focus:outline-none p-1 rounded-lg hover:bg-gray-100 transition-colors">
          <XIcon class="h-5 w-5" />
        </button>
      </div>

      <!-- Content -->
      <div class="px-6 py-5 overflow-y-auto flex-1">
        <!-- Search -->
        <div class="relative mb-6">
          <input
              type="text"
              v-model="searchQuery"
              placeholder="Pesquisar veículo..."
              class="block p-2 ps-10 text-sm rounded-lg w-full bg-transparent border-extra-soft-orange hover:border-soft-orange focus:ring-soft-orange placeholder-gray-500 text-gray-900"
          />
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
        </div>

        <!-- Vehicle List -->
        <div class="space-y-3 max-h-96 overflow-y-auto">
          <div
              v-for="vehicle in filteredVehicles"
              :key="vehicle.id"
              class="flex items-center p-4  rounded-xl cursor-pointer transition-all duration-200"
              :class="{
              'border-2 border-gray-200 hover:bg-gray-50 hover:border-gray-300': !(selectedVehicle && selectedVehicle.id === vehicle.id),
              'bg-extra-soft-orange/50': selectedVehicle && selectedVehicle.id === vehicle.id
            }"
              @click="selectVehicle(vehicle)"
          >
            <!-- Vehicle Image -->
            <div class="w-20 h-20 rounded-lg overflow-hidden flex-shrink-0 mr-5 bg-gray-100">
              <img v-if="vehicle.v_img":src="vehicle.v_img" :alt="vehicle.v_modelo" class="w-full h-full object-cover" />
              <img v-else src="@/assets/img/carroteste.png" alt="Veículo Padrão" class="w-full h-full object-fill" />
            </div>

            <!-- Vehicle Info -->
            <div class="flex-1 min-w-0">
              <div class="font-semibold text-lg text-gray-900 mb-1">{{ vehicle.v_modelo }}</div>
              <div class="text-sm text-gray-600">Matrícula: {{ vehicle.v_matricula }}</div>
            </div>

            <!-- Status Badge -->
            <div
                class="px-3 py-1.5 rounded-full text-xs font-medium whitespace-nowrap"
                :class="{
                'bg-green-100 text-green-800': vehicle.v_estado_display === 'Em uso',
                'bg-red-100 text-red-800': vehicle.v_estado_display === 'Em Manutencao'
              }"
            >
              {{ vehicle.v_estado_display }}
            </div>
          </div>

          <!-- Empty State -->
          <div v-if="filteredVehicles.length === 0" class="text-center py-12 text-gray-500">
            <div class="text-lg mb-2">Nenhum veículo encontrado</div>
            <div class="text-sm">Tente ajustar os critérios de pesquisa.</div>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="flex justify-end gap-3 px-6 py-4 border-t border-gray-200 bg-gray-50/50">
        <button
            class="inline-flex items-center rounded-md bg-gray-100 px-3 py-2 text-sm font-semibold text-gray-900 shadow-xs hover:bg-gray-300 duration-300"
            @click="closeModal"
        >
          Cancelar
        </button>
        <button
            class="px-6 py-2.5 rounded-lg font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2"
            :class="{
            'inline-flex items-center rounded-md bg-extra-soft-orange px-3 py-2 text-sm font-semibold text-gray-900 shadow-xs hover:bg-soft-orange duration-300': selectedVehicle && selectedVehicle.v_estado_display === 'Em uso',
            'inline-flex items-center rounded-md bg-gray-300 px-3 py-2 text-sm font-semibold shadow-xs duration-300 text-white cursor-not-allowed': !selectedVehicle || selectedVehicle.v_estado_display !== 'Em uso'
          }"
            :disabled="!selectedVehicle ||selectedVehicle.v_estado_display !== 'Em uso'"
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
      vehicle.v_modelo.toLowerCase().includes(query) ||
      vehicle.v_matricula.toLowerCase().includes(query)
  );
});



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
  if (selectedVehicle.value && selectedVehicle.value.v_estado_display === 'Em uso') {
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