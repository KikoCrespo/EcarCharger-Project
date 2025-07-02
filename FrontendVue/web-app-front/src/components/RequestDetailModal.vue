<template>
  <div v-if="show" class="fixed inset-0 bg-gray-500/50 backdrop-blur-sm transition-opacity flex items-center justify-center">
    <div class="bg-white sm:rounded-lg h-full w-full max-w-[40vw] max-h-[90vh] items-center justify-center p-6">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-lg font-semibold">Informações de requisitação do Veículo</h3>
        <button @click="closeModal" class="text-gray-500 hover:text-gray-700">
          <XIcon class="h-5 w-5" />
        </button>
      </div>

      <div class="mb-4">
        <div class="flex items-center gap-4 p-3 bg-gray-50 rounded-lg mb-4">
          <img src="../assets/img/carroteste.png" alt="Imagem" class="w-40 h-30 object-cover rounded" />
          <!-- :src="vehicle?.v_img" -->
          <div>
            <h4 class="font-medium">{{ request?.r_veiculo.v_marca }} {{ request?.r_veiculo.v_modelo }} </h4>
            <p class="text-gray-600 text-sm">{{ request.r_veiculo?.v_categoria_display }}</p>
            <p class="text-gray-600 text-sm">{{ request.r_veiculo?.v_matricula }}</p>
          </div>
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Funcionário</label>
          <span>{{ request.r_utilizador.first_name + ' ' + request.r_utilizador.last_name }}</span>
        </div>

        <div class="space-y-5">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Data de Início</label>
            <input type="date" v-model="request.r_data_inicio"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
              :disabled=true />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Data de Fim</label>
            <input v-if="!request.r_ilimitado" type="date" v-model="request.r_data_fim"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
              :disabled=true />
            <span v-else
              class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent">
              --//-- </span>
          </div>

          <div>
            <label for="" class="block text-sm font-medium text-gray-700 mb-1"> Estado</label>
            <div class="flex items-center">
              <div class="h-2.5 w-2.5 rounded-full me-2" :class="request.r_estado_display === 'Aprovada' ? 'bg-green-500' :
                request.r_estado_display === 'Pendente' ? 'bg-yellow-500' :
                  request.r_estado_display === 'Terminada' ? 'bg-gray-300' :
                    'bg-red-500'
                ">
              </div>
              {{ request.r_estado_display }}
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Motivo</label>
            <textarea v-model="request.r_motivo" rows="3"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-soft-orange focus:border-transparent text-sm text-gray-800"
              placeholder="Descreva o motivo da requisição..." :disabled=true></textarea>
          </div>
          <div v-if="request.r_estado_display === 'Terminada'">
            <label class="block text-sm font-medium text-gray-700 mb-1">Motivo da Terminação</label>
            <textarea v-model="request.r_motivo_terminacao" rows="3"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-soft-orange focus:border-transparent text-sm text-gray-800"
              placeholder="Descreva o motivo da requisição..." :disabled=true></textarea>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { XIcon } from 'lucide-vue-next';

const props = defineProps({
  show: Boolean,
  request: Object
});

const emit = defineEmits(['update:show']);



const closeModal = () => {
  emit('update:show', false);
  emit('close')
};
const request = ref({ ...props.request });
</script>