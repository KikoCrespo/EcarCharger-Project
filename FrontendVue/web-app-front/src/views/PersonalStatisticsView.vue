<template>

    <h1 class="text-2xl font-bold mb-6 text-gray-800">Estatísticas</h1>

    <!-- Filtros e Período -->
    <div class="bg-white rounded-lg shadow-sm p-4 mb-6 flex flex-col md:flex-row justify-between items-center gap-4">
      <div class="flex items-center gap-2">
        <span class="text-sm font-medium text-gray-700">Período:</span>
        <div class="inline-flex rounded-md shadow-sm" role="group">
          <button
              type="button"
              class="px-4 py-2 text-sm font-medium rounded-l-lg border border-gray-200 focus:z-10 focus:ring-2 focus:ring-orange-500 transition-colors"
              :class="period === 'weekly' ? 'bg-orange-100 text-orange-800 border-orange-200' : 'bg-white text-gray-700 hover:bg-gray-50'"
              @click="period = 'weekly'"
          >
            Semanal
          </button>
          <button
              type="button"
              class="px-4 py-2 text-sm font-medium rounded-r-lg border border-gray-200 focus:z-10 focus:ring-2 focus:ring-orange-500 transition-colors"
              :class="period === 'monthly' ? 'bg-orange-100 text-orange-800 border-orange-200' : 'bg-white text-gray-700 hover:bg-gray-50'"
              @click="period = 'monthly'"
          >
            Mensal
          </button>
        </div>
      </div>

      <!--
      <div class="flex items-center gap-3">

        <div class="relative">
          <input
              type="date"
              v-model="startDate"
              class="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
          />
        </div>
        <span class="text-gray-500">até</span>
        <div class="relative">
          <input
              type="date"
              v-model="endDate"
              class="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
          />
        </div>
        <button
            class="px-4 py-2 bg-soft-orange text-white rounded-lg hover:bg-orange-600 transition-colors text-sm font-medium"
            @click="applyDateFilter"
        >
          Aplicar
        </button>
      </div>
      -->
    </div>

    <!-- Cards de Resumo -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">

      <div class="bg-white rounded-lg shadow-sm p-5">
        <h3 class="text-base font-medium mb-2">Energia Total Consumida</h3>
        <div class="text-3xl font-bold mb-1">{{ totalEnergy.toFixed(2) }} kWh</div>
        <div
            class="flex items-center text-sm"
            :class="energyTrend > 0 ? 'text-red-600' : 'text-green-600'"
        >
          <div class="mr-1">
            <ChevronUp v-if="energyTrend > 0 && energyTrend <=50" class="w-4 h-4" />
            <ChevronsUp v-if="energyTrend > 50" class="w-4 h-4" />
            <ChevronDown v-if="energyTrend < 0 && energyTrend >= -50" class="w-4 h-4" />
            <ChevronsDown v-if="energyTrend < -50" class="w-4 h-4" />
          </div>
          <span>{{ Math.abs(chargingsTrend) }}% vs {{ period === 'weekly' ? 'semana anterior' : 'mês anterior' }}</span>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-sm p-5">
        <h3 class="text-base font-medium mb-2">Custo Total</h3>
        <div class="text-3xl font-bold mb-1">{{ formatCurrency(totalCost) }}</div>
        <div
            class="flex items-center text-sm"
            :class="costDiff > 0 ? 'text-red-600' : 'text-green-600'"
        >
          <div class="mr-1">
            <Plus v-if="costDiff > 0" class="w-4 h-4" />
            <Minus v-else class="w-4 h-4" />
          </div>
          <span>{{ Math.abs(costDiff) }}€ vs {{ period === 'weekly' ? 'semana anterior' : 'mês anterior' }}</span>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-sm p-5">
        <h3 class="text-base font-medium mb-2">Carregamentos</h3>
        <div class="text-3xl font-bold mb-1">{{ totalChargings }}</div>
        <div
            class="flex items-center text-sm"
            :class="chargingsTrend > 0 ? 'text-green-600' : 'text-red-600'"
        >
          <div class="mr-1">
            <ChevronUp v-if="chargingsTrend > 0 && chargingsTrend <=50" class="w-4 h-4" />
            <ChevronsUp v-if="chargingsTrend > 50" class="w-4 h-4" />
            <ChevronDown v-if="chargingsTrend < 0 && chargingsTrend >= -50" class="w-4 h-4" />
            <ChevronsDown v-if="chargingsTrend < -50" class="w-4 h-4" />
          </div>
          <span>{{ Math.abs(chargingsTrend) }}% vs {{ period === 'weekly' ? 'semana anterior' : 'mês anterior' }}</span>
        </div>
      </div>
    </div>

    <!-- Gráfico de Custos -->
    <div class="bg-white rounded-lg shadow-sm mb-6 overflow-hidden">
      <weekly-cost-chart
          :period="period"
          :cost-data="costData"
      />
    </div>

    <!-- Histórico de Carregamentos -->
    <div class="bg-white rounded-lg shadow-sm mb-6 overflow-hidden">
      <charging-history-table
          :charging-history="filteredChargingHistory"
      />
    </div>

</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import WeeklyCostChart from '@/components/Statistics/WeeklyCostChart.vue';
import ChargingHistoryTable from '@/components/Statistics/ChargingHistoryTable.vue';
import api from '@/interceptors/axiosInterceptor'
import {
  ChevronUp,
  ChevronsUp,
  ChevronDown,
  ChevronsDown,
  Minus,
  Plus
} from 'lucide-vue-next';



// Estado
const period = ref('weekly');
const startDate = ref(formatDateForInput(new Date(new Date().setDate(new Date().getDate() - 30))));
const endDate = ref(formatDateForInput(new Date()));
const users = ref({});


// Inicialização dos dados
const totalEnergy = ref(0);
const energyTrend = ref(0);
const totalCost = ref(0);
const costDiff = ref(0);
const totalChargings = ref(0);
const chargingsTrend = ref(0);

// Dados para o gráfico de custos
const weeklyCostData = ref([
  { name: 'Semana Atual', data: [0, 0, 0, 0, 0, 0, 0], color: '#f39c12' },
  { name: 'Semana Anterior', data: [0,0,0,0,0,0,0], color: '#bdc3c7' }
]);

const monthlyCostData = ref([
  { name: 'Ano Atual', data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], color: '#f39c12' },
  { name: 'Ano Anterior', data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], color: '#bdc3c7' }
]);

const costData = computed(() => {
  return period.value === 'weekly' ? weeklyCostData.value : monthlyCostData.value;
});

// Histórico de carregamentos
const chargingHistory = ref([]);

// Filtragem do histórico por data
const filteredChargingHistory = computed(() => {
  const start = new Date(startDate.value);
  const end = new Date(endDate.value);
  end.setHours(23, 59, 59, 999); // Definir para o final do dia

  return chargingHistory.value.filter(charge => {
    const chargeDate = new Date(charge.date);
    return chargeDate >= start && chargeDate <= end;
  });
});

// Métodos
function applyDateFilter() {
  console.log('Aplicando filtro de data:', startDate.value, 'até', endDate.value);
  // Aqui você poderia fazer uma chamada à API para buscar dados filtrados
  // No momento estamos apenas usando o computed filteredChargingHistory
}

function formatDateForInput(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');

  return `${year}-${month}-${day}`;
}

function formatCurrency(value) {
  return new Intl.NumberFormat('pt-PT', {
    style: 'currency',
    currency: 'EUR'
  }).format(value);
}

function formatDuration(minutes) {
  const hrs = Math.floor(minutes / 60);
  const mins = minutes % 60;
  return `${hrs}h ${mins.toString().padStart(2, '0')}m`;
}


onMounted(async () => {
  try {


    const response = await api.get('/estatisticas/pessoais/');

    console.log('Resposta da API:', response);

    if (response.data) {
      // Armazena os dados do usuário e os totais
      const userData = {
        userId: response.data.user_id,
        firstName: response.data.first_name,
        lastName: response.data.last_name,
        custoSemanais_before: response.data.custo_semanais_before,
        custoSemanais_now: response.data.custo_semanais_now,
        custoMensais_before: response.data.custo_mensais_before,
        custoMensais_now: response.data.custo_mensais_now,

        totalCarregamentosMensal: response.data.total_carregamentos_mensal,
        totalCarregamentosMensal_before: response.data.total_carregamentos_mensal_before,
        totalQuantidadeMensal: response.data.total_quantidade_mensal,
        totalQuantidadeMensal_before: response.data.total_quantidade_mensal_before,
        totalCustoMensal: response.data.total_custo_mensal,
        totalCustoMensal_before: response.data.total_custo_mensal_before,

        totalCarregamentosSemanal: response.data.total_carregamentos_semanal,
        totalCarregamentosSemanal_before: response.data.total_carregamentos_semanal_before,
        totalQuantidadeSemanal: response.data.total_quantidade_semanal,
        totalQuantidadeSemanal_before: response.data.total_quantidade_semanal_before,
        totalCustoSemanal: response.data.total_custo_semanal,
        totalCustoSemanal_before: response.data.total_custo_semanal_before,

        carregamentos: response.data.carregamentos,

      };

    
      chargingHistory.value = Object.entries(userData.carregamentos).map(([key, charge]) => ({
        date: new Date(charge.ca_data_inicio),
        station: charge.posto || 'Desconhecido',
        vehicle: charge.veiculo || 'Desconhecido',
        duration: formatDuration(charge.duracao),
        energy: charge.energia,
        cost: charge.custo
      }));


      // Atualizar valores principais
      totalEnergy.value = period.value === 'weekly'
          ? userData.totalQuantidadeSemanal
          : userData.totalQuantidadeMensal;

      totalCost.value = period.value === 'weekly'
          ? userData.totalCustoSemanal
          : userData.totalCustoMensal;

      totalChargings.value = period.value === 'weekly'
          ? userData.totalCarregamentosSemanal
          : userData.totalCarregamentosMensal;

      if(period.value === 'weekly') {

        if(userData.totalQuantidadeSemanal_before !== 0) {
          // Cálculo da tendência de energia
          energyTrend.value = (userData.totalQuantidadeSemanal - userData.totalQuantidadeSemanal_before) / userData.totalQuantidadeSemanal_before * 100;

        } else {
          energyTrend.value = userData.totalQuantidadeSemanal > 0 ? 100 : 0; // Se não houver energia antes, mas houver agora, consideramos um aumento de 100%
        }

        costDiff.value = userData.totalCustoSemanal - userData.totalCustoSemanal_before;

        if(userData.totalCarregamentosSemanal_before !== 0) {
          // Cálculo da tendência de carregamentos
          chargingsTrend.value = (userData.totalCarregamentosSemanal - userData.totalCarregamentosSemanal_before) / userData.totalCarregamentosSemanal_before * 100;

        } else {
          chargingsTrend.value = userData.totalCarregamentosSemanal > 0 ? 100 : 0; // Se não houver carregamentos antes, mas houver agora, consideramos um aumento de 100%
        }

      } else {

        if(userData.totalQuantidadeMensal_before !== 0) {
          // Cálculo da tendência de energia
          energyTrend.value = (userData.totalQuantidadeMensal - userData.totalQuantidadeMensal_before) / userData.totalQuantidadeMensal_before * 100;

        } else {
          energyTrend.value = userData.totalQuantidadeMensal > 0 ? 100 : 0; // Se não houver energia antes, mas houver agora, consideramos um aumento de 100%
        }

        costDiff.value = userData.totalCustoMensal - userData.totalCustoMensal_before;

        if(userData.totalCarregamentosMensal_before !== 0) {
          // Cálculo da tendência de carregamentos
          chargingsTrend.value = (userData.totalCarregamentosMensal - userData.totalCarregamentosMensal_before) / userData.totalCarregamentosMensal_before * 100;

        } else {
          chargingsTrend.value = userData.totalCarregamentosMensal > 0 ? 100 : 0; // Se não houver carregamentos antes, mas houver agora, consideramos um aumento de 100%
        }
      }



      weeklyCostData.value = [
        { name: 'Semana Atual', data: [userData.custoSemanais_now['monday'],userData.custoSemanais_now['tuesday'],userData.custoSemanais_now['wednesday'],userData.custoSemanais_now['thursday'],userData.custoSemanais_now['friday'],userData.custoSemanais_now['saturday'],userData.custoSemanais_now['sunday']], color: '#f39c12' },
        { name: 'Semana Anterior', data: [userData.custoSemanais_before['monday'],userData.custoSemanais_before['tuesday'],userData.custoSemanais_before['wednesday'],userData.custoSemanais_before['thursday'],userData.custoSemanais_before['friday'],userData.custoSemanais_before['saturday'],userData.custoSemanais_before['sunday']], color: '#bdc3c7' }
      ];

      monthlyCostData.value = [
        { name: 'Ano Atual', data: [userData.custoMensais_now['1'],userData.custoMensais_now['2'],userData.custoMensais_now['3'],userData.custoMensais_now['4'],userData.custoMensais_now['5'],userData.custoMensais_now['6'],userData.custoMensais_now['7'],userData.custoMensais_now['8'],userData.custoMensais_now['9'],userData.custoMensais_now['10'],userData.custoMensais_now['11'],userData.custoMensais_now['12']], color: '#f39c12' },
        { name: 'Ano Anterior', data: [userData.custoMensais_before['1'],userData.custoMensais_before['2'],userData.custoMensais_before['3'],userData.custoMensais_before['4'],userData.custoMensais_before['5'],userData.custoMensais_before['6'],userData.custoMensais_before['7'],userData.custoMensais_before['8'],userData.custoMensais_before['9'],userData.custoMensais_before['10'],userData.custoMensais_before['11'],userData.custoMensais_before['12']], color: '#bdc3c7' }
      ];

    } else {
      console.error('Formato de dados inválido recebido da API.');
    }
  } catch (error) {
    console.error('Erro ao recuperar dados dos utilizadores:', error);
    state.isAuthenticated = false;
  }
});


</script>