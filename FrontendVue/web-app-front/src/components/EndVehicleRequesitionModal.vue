<template>
  <div v-if="show" class="fixed inset-0 bg-gray-500/75 transition-opacity flex items-center justify-center z-50">
    <div class="bg-white sm:rounded-lg  w-full max-w-md p-6">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-lg font-semibold">Terminar requisição</h3>
        <button @click="closeModal" class="text-gray-500 hover:text-gray-700">
          <XIcon class="h-5 w-5" />
        </button>
      </div>

      <div class="mb-4">
        <div class="flex items-center gap-4 p-3 bg-gray-50 rounded-lg mb-4">
          <img :src="vehicle?.v_img" alt="Vehicle" class="w-40 h-30 object-cover rounded" />
          <div>
            <h4 class="font-medium text-gray-800">{{ vehicle?.v_modelo }} {{vehicle?.v_marca}}</h4>
            <h4 class="font-medium text-gray-600">{{ vehicle?.v_matricula }}</h4>
            <p class="text-gray-600 text-sm">{{ vehicle?.v_categoria_display }}</p>
          </div>
        </div>

        <div class="space-y-4">
          <div>
          
            <label class="block text-sm font-medium text-gray-700 mb-1">Motivo</label>
            <textarea
                v-model="form.reason"
                rows="3"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-soft-orange focus:border-transparent text-sm text-gray-800"
                placeholder="Descreva o motivo para o término da requisição..."
            ></textarea>
          </div>
        </div>
      </div>

      <div class="flex gap-3">
        <button
            class="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-800 py-2 rounded-lg"
            @click="closeModal"
        >
          Cancelar
        </button>
        <button
            class="flex-1 bg-extra-soft-orange hover:bg-soft-orange duration-300  font-semibold text-gray-900 py-2 rounded-lg"
            @click="submitRequest"
            :disabled="!isFormValid"
        >
          Confirmar
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { XIcon } from 'lucide-vue-next';

const props = defineProps({
  show: Boolean,
  vehicle: Object,
  request: Object
});

const emit = defineEmits(['update:show', 'submit-request']);


const form = ref({
  reason: ''
});

// Validar formulário
const isFormValid = computed(() => {
  return form.value.reason.trim().length > 0;
});


const submitRequest = () => {
  if (!isFormValid.value) return;
  console.log('Submitting request with reason:', form.value.reason);

  const requestData = {
    reason: form.value.reason,
    request: props.request,
  };
  
  emit('submit-request', requestData);
  closeModal();

};

const closeModal = () => {
  emit('update:show', false);
  resetForm();
};

const resetForm = () => {
  form.value = {
    reason: '',
  };
};
</script>