<template>
  <div v-if="modelValue" class="fixed inset-0 bg-gray-500/75 transition-opacity flex items-center justify-center z-50">
    <div class="bg-white rounded-lg w-full max-w-md p-6">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-lg font-semibold">Adicionar Manutenção</h3>
        <button @click="fecharModal" class="text-gray-500 hover:text-gray-700">
          <XIcon class="h-5 w-5" />
        </button>
      </div>

      <div class="mb-4">
        <div class="flex items-center gap-4 p-3 bg-gray-50 rounded-lg mb-4">
          <img :src="veiculo.image" alt="Vehicle" class="w-20 h-20 object-cover rounded" />
          <div>
            <h4 class="font-medium">{{ veiculo.plate }}</h4>
            <p class="text-gray-600 text-sm">{{ veiculo.model }}</p>
          </div>
        </div>

        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Tipo de Manutenção</label>
            <select
                v-model="formData.tipo"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
            >
              <option value="">Selecione o tipo</option>
              <option value="Revisão">Revisão</option>
              <option value="Reparação">Reparação</option>
              <option value="Inspeção">Inspeção</option>
              <option value="Troca de Óleo">Troca de Óleo</option>
              <option value="Troca de Pneus">Troca de Pneus</option>
              <option value="Outro">Outro</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Data</label>
            <input
                type="date"
                v-model="formData.data"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Quilometragem</label>
            <input
                type="number"
                v-model="formData.km"
                placeholder="Quilometragem atual"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Custo (€)</label>
            <input
                type="number"
                v-model="formData.custo"
                step="0.01"
                placeholder="0.00"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Descrição</label>
            <textarea
                v-model="formData.descricao"
                rows="3"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                placeholder="Descreva a manutenção realizada..."
            ></textarea>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Oficina / Responsável</label>
            <input
                type="text"
                v-model="formData.oficina"
                placeholder="Nome da oficina ou responsável"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
            />
          </div>

          <div>
            <label class="flex items-center gap-2">
              <input type="checkbox" v-model="formData.agendarProxima" class="rounded text-orange-500 focus:ring-orange-500" />
              <span class="text-sm text-gray-700">Agendar próxima manutenção</span>
            </label>
          </div>

          <div v-if="formData.agendarProxima" class="pl-6 space-y-4 border-l-2 border-orange-100">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Data da Próxima Manutenção</label>
              <input
                  type="date"
                  v-model="formData.proximaData"
                  class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Quilometragem para Próxima Manutenção</label>
              <input
                  type="number"
                  v-model="formData.proximaKm"
                  placeholder="Quilometragem para próxima manutenção"
                  class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
              />
            </div>
          </div>
        </div>
      </div>

      <div class="flex gap-3">
        <button
            class="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-800 py-2 rounded-lg"
            @click="fecharModal"
        >
          Cancelar
        </button>
        <button
            class="flex-1 bg-orange-500 hover:bg-orange-600 text-white py-2 rounded-lg"
            @click="salvarManutencao"
            :disabled="!formValido"
            :class="{ 'opacity-50 cursor-not-allowed': !formValido }"
        >
          Salvar Manutenção
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { XIcon } from 'lucide-vue-next';

// Props
const props = defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  veiculo: {
    type: Object,
    required: true
  }
});

// Emits
const emit = defineEmits(['update:modelValue', 'salvar']);

// Estado do formulário
const formData = ref({
  tipo: '',
  data: new Date().toISOString().split('T')[0],
  km: '',
  custo: '',
  descricao: '',
  oficina: '',
  agendarProxima: false,
  proximaData: '',
  proximaKm: ''
});

// Validação do formulário
const formValido = computed(() => {
  return (
      formData.value.tipo &&
      formData.value.data &&
      formData.value.km &&
      formData.value.custo !== '' &&
      formData.value.descricao
  );
});

// Métodos
function fecharModal() {
  emit('update:modelValue', false);
  resetarFormulario();
}

function salvarManutencao() {
  if (!formValido.value) return;

  const manutencao = {
    type: formData.value.tipo,
    date: formData.value.data,
    km: parseInt(formData.value.km),
    cost: parseFloat(formData.value.custo),
    description: formData.value.descricao,
    workshop: formData.value.oficina
  };

  // Se agendou próxima manutenção
  if (formData.value.agendarProxima) {
    manutencao.nextMaintenance = {
      dueDate: formData.value.proximaData,
      kmLeft: formData.value.proximaKm ? parseInt(formData.value.proximaKm) - parseInt(formData.value.km) : 0
    };
  }

  emit('salvar', manutencao);
  fecharModal();
}

function resetarFormulario() {
  formData.value = {
    tipo: '',
    data: new Date().toISOString().split('T')[0],
    km: '',
    custo: '',
    descricao: '',
    oficina: '',
    agendarProxima: false,
    proximaData: '',
    proximaKm: ''
  };
}

// Inicializar quilometragem com a do veículo quando o modal é aberto
watch(() => props.modelValue, (novoValor) => {
  if (novoValor && props.veiculo) {
    formData.value.km = props.veiculo.stats?.totalKm || '';

    // Calcular data padrão para próxima manutenção (3 meses depois)
    const proximaData = new Date();
    proximaData.setMonth(proximaData.getMonth() + 3);
    formData.value.proximaData = proximaData.toISOString().split('T')[0];
  }
});
</script>