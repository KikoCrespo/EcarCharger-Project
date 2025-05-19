<template>
  <div class="min-h-screen ">
    <!-- Header -->

    <div class="flex">
      <!-- Sidebar -->


      <!-- Main Content -->
      <main class="flex-1 p-6 max-h-[800px] overflow-y-auto">
        <div class="max-w-4xl mx-auto">


          <!-- Foto do veículo em círculo -->
          <div class="flex flex-col items-center mb-8">
            <div class="relative">
              <div class="w-48 h-48 rounded-full overflow-hidden border-4 border-orange-500 mb-4">
                <img :src="vehicle.image" :alt="vehicle.model" class="w-full h-full object-cover" />
              </div>
              <div
                  class="absolute -bottom-2 right-0 px-3 py-1 rounded-full text-sm font-medium"
                  :class="{
                  'bg-green-100 text-green-800': vehicle.status === 'available',
                  'bg-orange-100 text-orange-800': vehicle.status === 'in-use',
                  'bg-red-100 text-red-800': vehicle.status === 'maintenance'
                }"
              >
                {{ getStatusText(vehicle.status) }}
              </div>
            </div>
            <h1 class="text-2xl font-bold mt-2">{{ vehicle.plate }}</h1>
            <p class="text-gray-600">{{ vehicle.model }}</p>
          </div>

          <!-- Ações rápidas -->
          <div class="flex justify-center gap-4 mb-8">
            <button
                class="bg-extra-soft-orange hover:bg-soft-orange duration-300  text-gray-900 px-6 py-2 rounded-lg flex items-center gap-2"
                :disabled="vehicle.status !== 'available'"
                :class="{ 'opacity-50 cursor-not-allowed': vehicle.status !== 'available' }"
                @click="showRequestModal = true"
            >
              <CarIcon class="h-5 w-5" />
              <span>Requisitar</span>
            </button>
            <button class="bg-gray-100 hover:bg-gray-200 text-gray-800 duration-300 px-6 py-2 rounded-lg flex items-center gap-2">
              <HistoryIcon class="h-5 w-5" />
              <span>Histórico</span>
            </button>
            <button class="bg-gray-100 hover:bg-gray-200 text-gray-800 duration-300 px-6 py-2 rounded-lg flex items-center gap-2">
              <FileTextIcon class="h-5 w-5" />
              <span>Relatório</span>
            </button>
          </div>

          <!-- Informações do veículo -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <!-- Detalhes básicos -->
            <div class="bg-white rounded-lg border border-gray-200 shadow-sm overflow-hidden">
              <div class="bg-gray-50 px-4 py-3 border-b border-gray-200">
                <h2 class="font-semibold text-lg">Detalhes do Veículo</h2>
              </div>
              <div class="p-4">
                <div class="space-y-3">
                  <div class="flex justify-between">
                    <span class="text-gray-600">Tipo:</span>
                    <span class="font-medium">{{ vehicle.type }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-600">Matrícula:</span>
                    <span class="font-medium">{{ vehicle.plate }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-600">Modelo:</span>
                    <span class="font-medium">{{ vehicle.model }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-600">Ano:</span>
                    <span class="font-medium">{{ vehicle.year }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-600">Cor:</span>
                    <span class="font-medium">{{ vehicle.color }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-600">Lugares:</span>
                    <span class="font-medium">{{ vehicle.seats }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Especificações técnicas -->
            <div class="bg-white rounded-lg border border-gray-200 shadow-sm overflow-hidden">
              <div class="bg-gray-50 px-4 py-3 border-b border-gray-200">
                <h2 class="font-semibold text-lg">Especificações Técnicas</h2>
              </div>
              <div class="p-4">
                <div class="space-y-3">
                  <div class="flex justify-between">
                    <span class="text-gray-600">Potência:</span>
                    <span class="font-medium">{{ vehicle.power }} kw</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-600">Transmissão:</span>
                    <span class="font-medium">{{ vehicle.transmission }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-600">Combustível:</span>
                    <span class="font-medium">{{ vehicle.fuel }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-600">Consumo médio:</span>
                    <span class="font-medium">{{ vehicle.fuelConsumption }} L/100km</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-600">Emissões CO2:</span>
                    <span class="font-medium">{{ vehicle.emissions }} g/km</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="text-gray-600">Capacidade do tanque:</span>
                    <span class="font-medium">{{ vehicle.tankCapacity }} L</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Estatísticas de uso -->
          <div class="mb-8">
            <h2 class="font-semibold text-lg mb-4">Estatísticas de Uso</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div class="bg-white rounded-lg border border-gray-200 shadow-sm p-4">
                <div class="text-gray-500 text-sm mb-1">Quilometragem Total</div>
                <div class="text-2xl font-semibold">{{ formatNumber(vehicle.stats.totalKm) }} km</div>
                <div class="mt-2 text-xs text-gray-500">
                  <span :class="vehicle.stats.kmTrend > 0 ? 'text-green-600' : 'text-red-600'">
                    {{ vehicle.stats.kmTrend > 0 ? '+' : '' }}{{ vehicle.stats.kmTrend }}%
                  </span>
                  desde o mês passado
                </div>
              </div>
              <div class="bg-white rounded-lg border border-gray-200 shadow-sm p-4">
                <div class="text-gray-500 text-sm mb-1">Requisições Totais</div>
                <div class="text-2xl font-semibold">{{ vehicle.stats.totalRequests }}</div>
                <div class="mt-2 text-xs text-gray-500">
                  <span :class="vehicle.stats.requestsTrend > 0 ? 'text-green-600' : 'text-red-600'">
                    {{ vehicle.stats.requestsTrend > 0 ? '+' : '' }}{{ vehicle.stats.requestsTrend }}%
                  </span>
                  desde o mês passado
                </div>
              </div>
              <div class="bg-white rounded-lg border border-gray-200 shadow-sm p-4">
                <div class="text-gray-500 text-sm mb-1">Dias em Uso</div>
                <div class="text-2xl font-semibold">{{ vehicle.stats.daysInUse }}</div>
                <div class="mt-2 text-xs text-gray-500">
                  <span :class="vehicle.stats.daysInUseTrend > 0 ? 'text-green-600' : 'text-red-600'">
                    {{ vehicle.stats.daysInUseTrend > 0 ? '+' : '' }}{{ vehicle.stats.daysInUseTrend }}%
                  </span>
                  desde o mês passado
                </div>
              </div>
            </div>
          </div>

          <!-- Gráficos de uso -->
          <div class="mb-8">
            <h2 class="font-semibold text-lg mb-4">Utilização Mensal</h2>
            <div class="bg-white rounded-lg border border-gray-200 shadow-sm p-4">
              <div class="h-64">
                <canvas ref="usageChart"></canvas>
              </div>
            </div>
          </div>

          <!-- Manutenções -->
          <div class="mb-8">
            <div class="flex justify-between items-center mb-4">
              <h2 class="font-semibold text-lg">Histórico de Manutenções</h2>
              <button
                  class="text-gray-900 hover:text-soft-orange duration-300 flex items-center gap-1"
                  @click="showMaintenanceModal = true"
              >
                <PlusIcon class="h-4 w-4" />
                <span>Adicionar</span>
              </button>
            </div>
            <div class="bg-white rounded-lg border border-gray-200 shadow-sm overflow-hidden">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                <tr>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Data</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tipo</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-mxedium text-gray-500 uppercase tracking-wider">Descrição</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Custo</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Quilometragem</th>
                </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="(maintenance, index) in vehicle.maintenanceHistory" :key="index">
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ formatDate(maintenance.date) }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ maintenance.type }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ maintenance.description }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ formatCurrency(maintenance.cost) }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ formatNumber(maintenance.km) }} km</td>
                </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Próximas manutenções programadas -->
          <div class="mb-8">
            <h2 class="font-semibold text-lg mb-4">Próximas Manutenções Programadas</h2>
            <div class="bg-white rounded-lg border border-gray-200 shadow-sm p-4">
              <div class="space-y-4">
                <div v-for="(scheduled, index) in vehicle.scheduledMaintenance" :key="index" class="flex items-center gap-4">
                  <div class="w-12 h-12 rounded-full bg-orange-100 flex items-center justify-center text-orange-500">
                    <component :is="getMaintenanceIcon(scheduled.type)" class="h-6 w-6" />
                  </div>
                  <div class="flex-1">
                    <h3 class="font-medium">{{ scheduled.type }}</h3>
                    <p class="text-sm text-gray-600">{{ scheduled.description }}</p>
                  </div>
                  <div class="text-right">
                    <div class="font-medium">{{ formatDate(scheduled.dueDate) }}</div>
                    <div class="text-sm text-gray-600">
                      {{ scheduled.kmLeft > 0 ? `ou em ${formatNumber(scheduled.kmLeft)} km` : 'ou a qualquer momento' }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Documentos -->
          <div class="mb-8">
            <div class="flex justify-between items-center mb-4">
              <h2 class="font-semibold text-lg">Documentos</h2>
              <button class="text-gray-900 hover:text-soft-orange duration-300 flex items-center gap-1">
                <UploadIcon class="h-4 w-4" />
                <span>Carregar</span>
              </button>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div v-for="(doc, index) in vehicle.documents" :key="index" class="bg-white rounded-lg border border-gray-200 shadow-sm p-4 flex items-center gap-3">
                <div class="w-10 h-10 rounded bg-gray-100 flex items-center justify-center text-gray-500">
                  <FileIcon class="h-5 w-5" />
                </div>
                <div class="flex-1">
                  <h3 class="font-medium">{{ doc.name }}</h3>
                  <p class="text-xs text-gray-500">Atualizado em {{ formatDate(doc.updatedAt) }}</p>
                </div>
                <button class="text-gray-500 hover:text-gray-700">
                  <DownloadIcon class="h-5 w-5" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>

    <!-- Modal de Requisição -->
    <div v-if="showRequestModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg w-full max-w-md p-6">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-semibold">Requisitar Veículo</h3>
          <button @click="showRequestModal = false" class="text-gray-500 hover:text-gray-700">
            <XIcon class="h-5 w-5" />
          </button>
        </div>

        <div class="mb-4">
          <div class="flex items-center gap-4 p-3 bg-gray-50 rounded-lg mb-4">
            <img :src="vehicle.image" alt="Vehicle" class="w-20 h-20 object-cover rounded" />
            <div>
              <h4 class="font-medium">{{ vehicle.plate }}</h4>
              <p class="text-gray-600 text-sm">{{ vehicle.model }}</p>
            </div>
          </div>

          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Data de Início</label>
              <input
                  type="date"
                  v-model="requestForm.startDate"
                  class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Data de Fim</label>
              <input
                  type="date"
                  v-model="requestForm.endDate"
                  class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Motivo</label>
              <textarea
                  v-model="requestForm.reason"
                  rows="3"
                  class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                  placeholder="Descreva o motivo da requisição..."
              ></textarea>
            </div>
          </div>
        </div>

        <div class="flex gap-3">
          <button
              class="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-800 py-2 rounded-lg"
              @click="showRequestModal = false"
          >
            Cancelar
          </button>
          <button
              class="flex-1 bg-orange-500 hover:bg-orange-600 text-white py-2 rounded-lg"
              @click="submitRequest"
          >
            Confirmar Requisição
          </button>
        </div>
      </div>
    </div>
    <AddMaintenanceModal
        v-model="showMaintenanceModal"
        :veiculo="vehicle"
        @salvar="addMaintenance"
    />
  </div>
</template>

<script setup>
import AddMaintenanceModal from "@/components/AddMaintenanceModal.vue";
import { ref, onMounted } from 'vue';
import {
  XIcon,
  CarIcon,
  HistoryIcon,
  FileTextIcon,
  FileIcon,
  DownloadIcon,
  UploadIcon,
  PlusIcon,

} from 'lucide-vue-next';


// Estado
const showMaintenanceModal = ref(false);
const showRequestModal = ref(false);
const usageChart = ref(null);
const requestForm = ref({
  startDate: '',
  endDate: '',
  reason: ''
});

// Dados simulados
const vehicle = ref({
  id: 2,
  plate: 'BB - 34 - ZX',
  type: 'SUV',
  model: 'Mercedes-Benz GLE',
  year: 2023,
  color: 'Cinza Metálico',
  image: 'https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-NGPn4YUZ9EMbcdOZrhDtwFjnQ3Ku22.png',
  seats: 5,
  power: 360,
  transmission: 'Automático',
  fuel: 'Diesel',
  fuelConsumption: 8.5,
  emissions: 195,
  tankCapacity: 85,
  status: 'available',
  favorite: true,
  stats: {
    totalKm: 15420,
    kmTrend: 12,
    totalRequests: 24,
    requestsTrend: -5,
    daysInUse: 145,
    daysInUseTrend: 8
  },
  usageData: {
    labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
    kilometers: [1200, 1450, 1320, 1600, 1800, 1500],
    requests: [3, 4, 3, 5, 6, 3]
  },
  maintenanceHistory: [
    {
      date: '2023-04-15',
      type: 'Revisão',
      description: 'Revisão programada de 10.000 km',
      cost: 450.00,
      km: 10000
    },
    {
      date: '2023-02-20',
      type: 'Reparação',
      description: 'Substituição de pneus',
      cost: 800.00,
      km: 8500
    },
    {
      date: '2022-12-05',
      type: 'Revisão',
      description: 'Troca de óleo e filtros',
      cost: 250.00,
      km: 5000
    }
  ],
  scheduledMaintenance: [
    {
      type: 'Revisão',
      description: 'Revisão programada de 20.000 km',
      dueDate: '2023-08-15',
      kmLeft: 4580
    },
    {
      type: 'Inspeção',
      description: 'Inspeção anual obrigatória',
      dueDate: '2023-10-30',
      kmLeft: 0
    }
  ],
  documents: [
    {
      name: 'Seguro Automóvel.pdf',
      updatedAt: '2023-01-10',
      type: 'pdf'
    },
    {
      name: 'Manual do Proprietário.pdf',
      updatedAt: '2022-12-15',
      type: 'pdf'
    },
    {
      name: 'Certificado de Matrícula.pdf',
      updatedAt: '2022-12-15',
      type: 'pdf'
    },
    {
      name: 'Histórico de Manutenção.xlsx',
      updatedAt: '2023-04-16',
      type: 'excel'
    }
  ]
});

// Métodos
function getStatusText(status) {
  switch (status) {
    case 'available':
      return 'Disponível';
    case 'in-use':
      return 'Em Uso';
    case 'maintenance':
      return 'Manutenção';
    default:
      return status;
  }
}

function formatNumber(number) {
  return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleDateString('pt-PT');
}

function formatCurrency(value) {
  return value.toLocaleString('pt-PT', { style: 'currency', currency: 'EUR' });
}

function getMaintenanceIcon(type) {
  switch (type.toLowerCase()) {
    case 'revisão':
      return 'SettingsIcon';
    case 'inspeção':
      return 'SearchIcon';
    default:
      return 'ToolIcon';
  }
}

function submitRequest() {


  // Simular sucesso
  showRequestModal.value = false;

  // Atualizar status do veículo (simulação)
  vehicle.value.status = 'in-use';

  // Resetar formulário
  requestForm.value = {
    startDate: '',
    endDate: '',
    reason: ''
  };

  // Notificação de sucesso (implementar conforme seu sistema de notificações)
  alert('Veículo requisitado com sucesso!');
}

function addMaintenance(maintenance) {
  // Adicionar a nova manutenção ao histórico
  vehicle.value.maintenanceHistory.unshift({
    date: maintenance.date,
    type: maintenance.type,
    description: maintenance.description,
    cost: maintenance.cost,
    km: maintenance.km
  });

  // Atualizar quilometragem total do veículo se a nova for maior
  if (maintenance.km > vehicle.value.stats.totalKm) {
    vehicle.value.stats.totalKm = maintenance.km;
  }

  // Se houver próxima manutenção agendada, adicionar à lista
  if (maintenance.nextMaintenance) {
    vehicle.value.scheduledMaintenance.push({
      type: maintenance.type,
      description: `Próxima ${maintenance.type.toLowerCase()} programada`,
      dueDate: maintenance.nextMaintenance.dueDate,
      kmLeft: maintenance.nextMaintenance.kmLeft
    });

    // Ordenar manutenções programadas por data
    vehicle.value.scheduledMaintenance.sort((a, b) => new Date(a.dueDate) - new Date(b.dueDate));
  }

  // Notificação de sucesso
  alert('Manutenção adicionada com sucesso!');
}

// Lifecycle hooks
onMounted(() => {
  // Inicializar a página
  document.title = `Veículo ${vehicle.value.plate} | HMV DOMO`;

  // Definir datas padrão para o formulário de requisição
  const today = new Date();
  const tomorrow = new Date();
  tomorrow.setDate(today.getDate() + 1);

  requestForm.value = {
    startDate: today.toISOString().split('T')[0],
    endDate: tomorrow.toISOString().split('T')[0],
    reason: ''
  };

  // Inicializar gráfico

});
</script>