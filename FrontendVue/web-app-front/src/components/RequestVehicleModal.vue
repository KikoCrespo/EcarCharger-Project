<template>
  <div v-if="show" class="fixed inset-0 bg-gray-500/75 transition-opacity flex items-center justify-center z-50">
    <div class="bg-white sm:rounded-lg h-full w-full max-w-md p-6">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-lg font-semibold">Requisitar Veículo</h3>
        <button @click="closeModal" class="text-gray-500 hover:text-gray-700">
          <XIcon class="h-5 w-5" />
        </button>
      </div>

      <div class="mb-4">
        <div class="flex items-center gap-4 p-3 bg-gray-50 rounded-lg mb-4">
          <img :src="vehicle?.image" alt="Vehicle" class="w-20 h-20 object-cover rounded" />
          <div>
            <h4 class="font-medium">{{ vehicle?.plate }}</h4>
            <p class="text-gray-600 text-sm">{{ vehicle?.type }}</p>
          </div>
        </div>

        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Data de Início</label>
            <input
                type="date"
                v-model="form.startDate"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                :min="minDate"
                :disabled="form.unlimitedPeriod"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Data de Fim</label>
            <input
                type="date"
                v-model="form.endDate"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                :min="form.startDate || minDate"
                :disabled="form.unlimitedPeriod"
            />
          </div>

          <div class="flex items-center">
            <input
                type="checkbox"
                id="unlimitedPeriod"
                v-model="form.unlimitedPeriod"
                class="h-4 w-4 text-orange-500 focus:ring-orange-500 border-gray-300 rounded"
            />
            <label for="unlimitedPeriod" class="ml-2 block text-sm text-gray-700">
              Período ilimitado
            </label>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Motivo</label>
            <textarea
                v-model="form.reason"
                rows="3"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-soft-orange focus:border-transparent text-sm text-gray-800"
                placeholder="Descreva o motivo da requisição..."
            ></textarea>
          </div>
        </div>
      </div>

      <div class="flex gap-3">
        <button
            class="flex-1 bg-gray-100 hover:bg-gray-200 duration-300 text-gray-800 py-2 rounded-lg"
            @click="closeModal"
        >
          Cancelar
        </button>
        <button
            class="flex-1 bg-extra-soft-orange hover:bg-soft-orange duration-300  font-semibold text-gray-900 py-2 rounded-lg"
            @click="submitRequest"
            :disabled="!isFormValid"
        >
          Confirmar Requisição
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { XIcon } from 'lucide-vue-next';

const props = defineProps({
  show: Boolean,
  vehicle: Object
});

const emit = defineEmits(['update:show', 'submit-request']);

// Obter data atual no formato YYYY-MM-DD
const today = new Date();
const minDate = today.toISOString().split('T')[0];

const form = ref({
  startDate: minDate, // Data atual como padrão
  endDate: '',
  reason: '',
  unlimitedPeriod: false
});

// Observar mudanças no checkbox de período ilimitado
watch(() => form.value.unlimitedPeriod, (newVal) => {
  if (newVal) {
    form.value.endDate = ''; // Limpa a data de fim quando marcado como ilimitado
  } else {
    // Se desmarcado, define uma data padrão de fim (7 dias após a data de início)
    const startDate = new Date(form.value.startDate);
    startDate.setDate(startDate.getDate() + 7);
    form.value.endDate = startDate.toISOString().split('T')[0];
  }
});

// Validar formulário
const isFormValid = computed(() => {
  if (form.value.unlimitedPeriod) {
    return form.value.reason.trim().length > 0;
  }
  return form.value.startDate &&
      form.value.endDate &&
      form.value.reason.trim().length > 0 &&
      new Date(form.value.endDate) >= new Date(form.value.startDate);
});

const closeModal = () => {
  emit('update:show', false);
  resetForm();
};

const submitRequest = () => {
  if (!isFormValid.value) return;

  const requestData = {
    vehicleId: props.vehicle.id,
    reason: form.value.reason,
    unlimitedPeriod: form.value.unlimitedPeriod
  };

  if (!form.value.unlimitedPeriod) {
    requestData.startDate = form.value.startDate;
    requestData.endDate = form.value.endDate;
  }

  emit('submit-request', requestData);
  closeModal();
};

const resetForm = () => {
  form.value = {
    startDate: minDate,
    endDate: '',
    reason: '',
    unlimitedPeriod: false
  };
};
</script>