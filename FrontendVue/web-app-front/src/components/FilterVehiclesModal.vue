<template>
  <div v-if="show" class="fixed inset-0 bg-gray-500/75 transition-opacity flex items-center justify-center z-50">
    <div class="bg-white rounded-lg w-full max-w-md p-6">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-lg font-semibold">Filtrar Veículos</h3>
        <button @click="closeModal" class="text-gray-500 hover:text-gray-700">
          <XIcon class="h-5 w-5" />
        </button>
      </div>

      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Tipo de Veículo</label>
          <div class="space-y-2">
            <label class="flex items-center gap-2">
              <input type="checkbox" v-model="localFilters.types.suv" class="rounded text-soft-orange focus:ring-soft-orange" />
              <span>SUV</span>
            </label>
            <label class="flex items-center gap-2">
              <input type="checkbox" v-model="localFilters.types.citadino" class="rounded text-soft-orange focus:ring-soft-orange" />
              <span>Citadino</span>
            </label>
            <label class="flex items-center gap-2">
              <input type="checkbox" v-model="localFilters.types.sedan" class="rounded text-soft-orange focus:ring-soft-orange" />
              <span>Sedan</span>
            </label>
            <label class="flex items-center gap-2">
              <input type="checkbox" v-model="localFilters.types.utilitario" class="rounded text-soft-orange focus:ring-soft-orange" />
              <span>Utilitário</span>
            </label>
            <label class="flex items-center gap-2">
              <input type="checkbox" v-model="localFilters.types.comercial" class="rounded text-soft-orange focus:ring-soft-orange" />
              <span>Comercial</span>
            </label>
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Estado</label>
          <div class="space-y-2">
            <label class="flex items-center gap-2">
              <input type="checkbox" v-model="localFilters.state.available" class="rounded text-soft-orange focus:ring-soft-orange" />
              <span>Disponível</span>
            </label>
            <label class="flex items-center gap-2">
              <input type="checkbox" v-model="localFilters.state.inUse" class="rounded text-soft-orange focus:ring-soft-orange" />
              <span>Em Uso</span>
            </label>
            <label class="flex items-center gap-2">
              <input type="checkbox" v-model="localFilters.state.maintenance" class="rounded text-soft-orange focus:ring-soft-orange" />
              <span>Em Manutenção</span>
            </label>
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Capacidade</label>
          <div class="space-y-2">
            <label class="flex items-center gap-2">
              <input type="checkbox" v-model="localFilters.seats.two" class="rounded text-soft-orange focus:ring-soft-orange" />
              <span>2 Lugares</span>
            </label>
            <label class="flex items-center gap-2">
              <input type="checkbox" v-model="localFilters.seats.four" class="rounded text-soft-orange focus:ring-soft-orange" />
              <span>4 Lugares</span>
            </label>
            <label class="flex items-center gap-2">
              <input type="checkbox" v-model="localFilters.seats.five" class="rounded text-soft-orange focus:ring-soft-orange" />
              <span>5 Lugares</span>
            </label>
            <label class="flex items-center gap-2">
              <input type="checkbox" v-model="localFilters.seats.seven" class="rounded text-soft-orange focus:ring-soft-orange" />
              <span>7+ Lugares</span>
            </label>
          </div>
        </div>
      </div>

      <div class="mt-6 flex gap-3">
        <button
            class="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-800 duration-300 py-2 rounded-lg"
            @click="resetFilters"
        >
          Limpar
        </button>
        <button
            class="flex-1 bg-extra-soft-orange hover:bg-soft-orange duration-300  font-semibold text-gray-900 py-2 rounded-lg"
            @click="applyFilters"
        >
          Aplicar
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { XIcon } from 'lucide-vue-next';

const props = defineProps({
  show: Boolean,
  filters: Object
});

const emit = defineEmits(['update:show', 'apply-filters', 'reset-filters']);

// Criamos uma cópia local dos filtros para trabalhar no modal
const localFilters = ref(JSON.parse(JSON.stringify(props.filters)));

// Atualiza os filtros locais quando os props mudam
watch(() => props.filters, (newFilters) => {
  localFilters.value = JSON.parse(JSON.stringify(newFilters));
}, { deep: true });

const closeModal = () => {
  emit('update:show', false);
};

const applyFilters = () => {
  emit('apply-filters', localFilters.value);
  closeModal();
};

const resetFilters = () => {
  emit('reset-filters');
  closeModal();
};
</script>