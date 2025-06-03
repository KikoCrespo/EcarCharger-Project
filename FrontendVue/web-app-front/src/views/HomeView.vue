<template>
  <div class="p-5 max-w-7xl mx-auto min-h-screen">
    <h1 class="text-2xl font-bold mb-5 text-gray-800">Dashboard</h1>

    <div class="space-y-6">
      <!-- Primeira linha: Postos de Carregamento + GaugeChart -->
      <div class="grid grid-cols-1 lg:grid-cols-[350px_1fr] gap-5">
        <!-- Postos de Carregamento - agora com altura fixa -->
        <div class="h-[350px]">
          <charging-stations-list
              :stations="chargingStations"
              :selected-station="selectedStation"
              @select-station="selectStation"
          />
        </div>

        <!-- GaugeChart -->
        <div>
          <gauge-chart
              :is-connected="isConnected"
              :session-id="sessionId"
              :session-closed="sessionClosed"
              :session-start-time="sessionStartTime"
              :session-summary="sessionSummary"
              :auto-end-time="autoEndTime"
              :series="series"
              :current-date-time="currentDateTime"
              @start-charging="startNewCharging"
              @finish-charging="finishCharging"
              @confirm-auto-end="confirmAutoEnd"
              @reset-session="resetSession"
          />
        </div>
      </div>

      <!-- Segunda linha: Estatísticas -->
      <div class="space-y-4">
        <div class="flex items-center">
          <hr class="flex-grow border-t-2 border-gray-300">
          <h2 class="mx-2 text-xl font-medium  text-gray-900 text-center relative">Estatísticas</h2>
          <hr class="flex-grow border-t-2 border-gray-300">
        </div>
        <div class="grid grid-cols-1 lg:grid-cols-[2fr_1fr] gap-5">
          <!-- Gráfico de linha (maior) -->
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-4 overflow-hidden">
            <div class="w-full h-full">
              <line-chart
                  :series="consumptionSeries"
                  :categories="consumptionCategories"
              />
            </div>
          </div>

          <!-- Consumo (menor) -->
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
            <consumption-card
                :consumption="totalEnergy"
                :trend="energyTrend"
                :period="'last week'"
            />
          </div>

          <!-- Rating de gastos -->
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-4 lg:col-span-2 overflow-hidden">
            <expenses-bubble-chart
                :expenses="expensesData"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Seleção de Veículo -->
    <vehicle-selection-modal
        v-model="showVehicleModal"
        :vehicles="vehicles"
        :selected-station="selectedStation"
        @select-vehicle="handleVehicleSelection"
    />
  </div>
</template>


<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import ChargingStationsList from '@/components/Dashboard/ChargingStationsList.vue';
//import GaugeChart from '@/components/Dashboard/GaugeChart.vue';
import ConsumptionCard from '@/components/Dashboard/ConsumptionCard.vue';
import LineChart from '@/components/Dashboard/LineChart.vue';
import ExpensesBubbleChart from '@/components/Dashboard/ExpensesBubbleChart.vue';
import VehicleSelectionModal from '@/components/Dashboard/VehicleSelectionModal.vue';
import api from '@/interceptors/axiosInterceptor'
import GaugeChart from '@/components/Dashboard/GaugeChart.vue';

const props = defineProps({
  user_data: {
    type: Object,
    required: true
  }
});


// Estado
const currentDateTime = ref(formatDateTime(new Date()));
const selectedStation = ref(null);
const showVehicleModal = ref(false);

// Dados principais
const totalEnergy = ref(0);
const energyTrend = ref(0);

// Sessão de carregamento
const isConnected = ref(false)
const sessionId = ref(null)
const sessionClosed = ref(false)
const sessionStartTime = ref(null)
const sessionSummary = ref(null)
const autoEndTime = ref(null)
const socket = ref(null)
const series = ref([0, 0, 0, 0])
const shouldReconnect = ref(true) // Nova flag para controlar reconexão

const vehicleId = ref(0);
const stationId = ref(0);
const userId = ref(0);

//Socket

function startNewCharging() {
  if (!selectedStation.value) {
    alert('Por favor, selecione um posto de carregamento disponível primeiro.');
    return;
  }

  // Add additional validation
  if (selectedStation.value.status !== true) {
    alert('O posto selecionado não está disponível.');
    return;
  }

  showVehicleModal.value = true;
}

function handleMessage(msg) {
  const d = JSON.parse(msg.data)
  console.log('📨 Mensagem recebida:', d); // Debug

  if (d.status === 'charging_started') {
    sessionId.value = d.session_id
    sessionStartTime.value = new Date().toISOString()
    isConnected.value = true
    sessionClosed.value = false
    localStorage.setItem('charging_session', JSON.stringify({
      id: sessionId.value,
      startTime: sessionStartTime.value,
      closed: false
    }))
    return
  }

  if (d.status === 'session_resumed') {
    sessionId.value = d.session_id
    sessionStartTime.value = d.start_time
    isConnected.value = true
    return
  }

  if (d.status === 'charging_auto_ended') {
    console.log('🛑 Carregamento finalizado automaticamente - INICIANDO PROCESSO'); // Debug

    // PRIMEIRO: Impedir qualquer reconexão futura
    shouldReconnect.value = false
    console.log('🚫 shouldReconnect definido como false'); // Debug

    // SEGUNDO: Fechar socket imediatamente
    if (socket.value) {
      console.log('🔌 Fechando socket atual'); // Debug
      socket.value.onclose = null // Remover handler de close para evitar reconexão
      socket.value.onerror = null // Remover handler de erro
      socket.value.close()
      socket.value = null
      console.log('✅ Socket fechado e limpo'); // Debug
    }

    // TERCEIRO: Atualizar estados
    isConnected.value = false
    sessionClosed.value = true
    console.log('📊 Estados atualizados - isConnected:', isConnected.value, 'sessionClosed:', sessionClosed.value); // Debug

    // QUARTO: Registrar o momento exato da paragem automática
    autoEndTime.value = new Date().toISOString()
    localStorage.setItem('charging_session', JSON.stringify({
      id: sessionId.value,
      startTime: sessionStartTime.value,
      autoEndTime: autoEndTime.value,
      closed: true
    }))

    console.log('✅ Processo de auto_end CONCLUÍDO - botão deve aparecer'); // Debug
    return
  }

  if (d.status === 'session_summary') {
    sessionSummary.value = d.summary;
    // Fechar o socket após receber o resumo
    if (socket.value) {
      socket.value.close();
    }
    return;
  }

  if (d.status === 'error') {
    console.error('WS Error:', d.message)
    isConnected.value = false
    return
  }

  if (d.status === 'charging_data' && d.data) {
    // Atualiza gráfico com novos dados
    series.value = [
      d.data.voltage || 0,
      d.data.current || 0,
      d.data.power || 0,
      d.data.frequency || 0
    ]
  }
}

function handleVehicleSelection({ vehicle, station }) {
  console.log('🚗 Veículo selecionado:', vehicle); // Debug
  vehicleId.value = vehicle.id
  stationId.value = station.id
  userId.value = props.user_data.id

  localStorage.removeItem('charging_session')
  sessionClosed.value = false
  sessionSummary.value = null
  autoEndTime.value = null
  shouldReconnect.value = true // Resetar flag de reconexão

  socket.value = new WebSocket('ws://localhost:8000/ws/sensor/')

  socket.value.onopen = () => {
    isConnected.value = true
    socket.value.send(JSON.stringify({
      action: 'start_charging',
      vehicle_id: vehicleId.value,
      station_id: stationId.value,
      user_id: userId.value
    }))
  }

  socket.value.onmessage = handleMessage

  socket.value.onclose = () => {
    isConnected.value = false
    if (sessionId.value && !sessionClosed.value) {
      setTimeout(() => reconnectSocket(sessionId.value), 2000)
    }
  }

  socket.value.onerror = () => {
    isConnected.value = false
  }

}


function reconnectSocket(savedId) {
  console.log('🔄 Tentativa de reconexão - sessionClosed:', sessionClosed.value, 'shouldReconnect:', shouldReconnect.value); // Debug

  // Não reconectar se a sessão já foi fechada ou se não deve reconectar
  if (sessionClosed.value || !shouldReconnect.value) {
    console.log('🚫 Reconexão BLOQUEADA - sessão fechada ou reconexão desabilitada')
    return
  }

  console.log('🔌 Iniciando nova conexão WebSocket'); // Debug
  socket.value = new WebSocket('ws://localhost:8000/ws/sensor/')

  socket.value.onopen = () => {
    console.log('✅ Socket reconectado com sucesso'); // Debug
    isConnected.value = true
    socket.value.send(JSON.stringify({
      action: 'resume_charging',
      session_id: savedId,
    }))
  }

  socket.value.onmessage = handleMessage

  socket.value.onclose = () => {
    console.log('🔌 Socket fechado - verificando se deve reconectar'); // Debug
    isConnected.value = false
    // Só reconectar se permitido e sessão ativa
    if (sessionId.value && !sessionClosed.value && shouldReconnect.value) {
      console.log('⏰ Agendando nova reconexão em 2 segundos'); // Debug
      setTimeout(() => reconnectSocket(sessionId.value), 2000)
    } else {
      console.log('🚫 Reconexão não agendada'); // Debug
    }
  }

  socket.value.onerror = () => {
    console.log('❌ Erro no socket'); // Debug
    isConnected.value = false
  }
}


function finishCharging() {
  if (socket.value && socket.value.readyState === WebSocket.OPEN) {
    socket.value.send(JSON.stringify({
      action: 'charging_stopped',
      session_id: sessionId.value
    }))
  }
}

// Confirmação de término automático
function confirmAutoEnd() {
  console.log('🔵 Confirmando fim automático'); // Debug

  if (!autoEndTime.value) {
    console.error('Data de fim automático não encontrada')
    return
  }

  // Criar nova conexão para enviar confirmação
  const confirmSocket = new WebSocket('ws://localhost:8000/ws/sensor/')

  confirmSocket.onopen = () => {
    console.log('🔌 Socket de confirmação conectado')
    confirmSocket.send(JSON.stringify({
      action: 'confirm_auto_end',
      session_id: sessionId.value,
      end_time: autoEndTime.value
    }))
  }

  confirmSocket.onmessage = handleMessage

  confirmSocket.onerror = (error) => {
    console.error('Erro na conexão de confirmação:', error)
  }
}

// Resetar sessão para iniciar novo carregamento
function resetSession() {
  shouldReconnect.value = true // Resetar flag de reconexão
  cleanupAfterSession();
  isConnected.value = false;
  sessionId.value = null;
  sessionClosed.value = false;
  sessionStartTime.value = null;
  sessionSummary.value = null;
  autoEndTime.value = null;
  series.value = [0, 0, 0, 0];
  localStorage.removeItem('charging_session');
}

// Limpar estado após sessão
function cleanupAfterSession() {
  localStorage.removeItem('charging_session')
  sessionId.value = null
  sessionClosed.value = false
  sessionStartTime.value = null
  sessionSummary.value = null
  autoEndTime.value = null
  series.value = [0, 0, 0, 0]
}

onBeforeUnmount(() => {
  if (socket.value) {
    socket.value.close()
  }
})

/*const chartOptions = ref({
  chart: {
    height: 390,
    type: 'radialBar'
  },
  plotOptions: {
    radialBar: {
      offsetY: 0,
      startAngle: 0,
      endAngle: 270,
      hollow: {
        margin: 5,
        size: '30%',
        background: 'transparent'
      },
      dataLabels: {
        name: {
          show: false
        },
        value: {
          show: false
        }
      },
      barLabels: {
        enabled: true,
        useSeriesColors: true,
        offsetX: -8,
        fontSize: '16px',
        formatter: function (seriesName, opts) {
          return seriesName + ': ' + opts.w.globals.series[opts.seriesIndex]
        }
      }
    }
  },
  colors: ['#1ab7ea', '#0084ff', '#39539E', '#0077B5'],
  labels: ['Tensão (V)', 'Corrente (A)', 'Potência (W)', 'Frequência (Hz)'],
  responsive: [
    {
      breakpoint: 480,
      options: {
        legend: {
          show: false
        }
      }
    }
  ]
})*/


// Dados simulados
const chargingStations = ref([]);

const vehicles = ref([
  {
    id: 1,
    model: 'Tesla Model 3',
    plate: 'AA-11-BB',
    status: 'available',
    image: 'https://placeholder.svg?height=200&width=300',
    batteryLevel: 45,
    range: 180
  },
  {
    id: 2,
    model: 'Nissan Leaf',
    plate: 'CC-22-DD',
    status: 'in-use',
    image: 'https://placeholder.svg?height=200&width=300',
    batteryLevel: 78,
    range: 210
  },
  {
    id: 3,
    model: 'BMW i3',
    plate: 'EE-33-FF',
    status: 'available',
    image: 'https://placeholder.svg?height=200&width=300',
    batteryLevel: 32,
    range: 120
  },
  {
    id: 4,
    model: 'Renault Zoe',
    plate: 'GG-44-HH',
    status: 'maintenance',
    image: 'https://placeholder.svg?height=200&width=300',
    batteryLevel: 15,
    range: 60
  },
  {
    id: 5,
    model: 'Hyundai Kona Electric',
    plate: 'II-55-JJ',
    status: 'available',
    image: 'https://placeholder.svg?height=200&width=300',
    batteryLevel: 90,
    range: 350
  }
]);

const consumptionSeries = ref([
  {
    name: 'Semana atual',
    data: [0,0,0,0,0,0],
    color: '#f39c12'
  },
  {
    name: 'Semana Anterior',
    data: [0,0,0,0,0,0],
    color: '#bdc3c7'
  }
]);

const consumptionCategories = ref(['1', '2', '3', '4', '5', '6', '7']);

const expensesData = ref([]);

// Métodos
function formatDateTime(date) {
  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const year = date.getFullYear();
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');

  return `${day}-${month}-${year} ${hours}:${minutes}`;
}

function formatDateTimeSecond(isoString) {
  if (!isoString) return '';
  const date = new Date(isoString);
  return date.toLocaleString();
}

function formatDuration(seconds) {
  if (!seconds) return '0s';
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const remainingSeconds = Math.floor(seconds % 60);

  let result = '';
  if (hours > 0) result += `${hours}h `;
  if (minutes > 0) result += `${minutes}m `;
  if (remainingSeconds > 0 || result === '') result += `${remainingSeconds}s`;

  return result;
}


function updateDateTime() {
  currentDateTime.value = formatDateTime(new Date());
}

function selectStation(station) {
  // Só permite selecionar postos disponíveis
  if (station.status === true) {
    selectedStation.value = station;
  } else {
    alert('Este posto não está disponível para carregamento.');
  }
}



// Lifecycle hooks
onMounted(async () =>  {
  // Atualizar a data/hora a cada minuto
  setInterval(updateDateTime, 60000);

  const savedSession = localStorage.getItem('charging_session')
  if (savedSession) {
    const session = JSON.parse(savedSession)
    sessionId.value = session.id
    sessionStartTime.value = session.startTime
    sessionClosed.value = session.closed || false
    autoEndTime.value = session.autoEndTime || null

    console.log('🔄 Sessão recuperada:', {
      sessionId: sessionId.value,
      sessionClosed: sessionClosed.value,
      autoEndTime: autoEndTime.value
    }); // Debug

    // Reconectar apenas se a sessão não estiver concluída
    if (!sessionClosed.value) {
      reconnectSocket(sessionId.value)
    }
  }

  try {
    const response = await api.get('/dashboard/');
    if (response.data) {
      // Armazena os dados do usuário e os totais
      const userData = {

        consumosSemanais_now: response.data.consumos_semanais_now,
        consumosSemanais_before: response.data.consumos_semanais_before,
        custosMensais: response.data.maiores_custos_mensais,
        postos: response.data.postos,
        totalQuantidadeSemanal: response.data.total_quantidade_semanal,
        totalQuantidadeSemanal_before: response.data.total_quantidade_semanal_before,

      };

      // Atualizar valores principais
      totalEnergy.value = userData.totalQuantidadeSemanal
      console.log(userData.totalQuantidadeSemanal)

        if(userData.totalQuantidadeSemanal_before !== 0) {
          // Cálculo da tendência de energia
          energyTrend.value = (userData.totalQuantidadeSemanal - userData.totalQuantidadeSemanal_before) / userData.totalQuantidadeSemanal_before * 100;

        } else {
          energyTrend.value = userData.totalQuantidadeSemanal > 0 ? 100 : 0; // Se não houver energia antes, mas houver agora, consideramos um aumento de 100%
        }

      consumptionSeries.value = [
        {
          name: 'Semana atual',
          data: [
            userData.consumosSemanais_now['monday'],
            userData.consumosSemanais_now['tuesday'],
            userData.consumosSemanais_now['wednesday'],
            userData.consumosSemanais_now['thursday'],
            userData.consumosSemanais_now['friday'],
            userData.consumosSemanais_now['saturday'],
            userData.consumosSemanais_now['sunday']
          ],
          color: '#f39c12'
        },
        {
          name: 'Semana Anterior',
          data: [
            userData.consumosSemanais_before['monday'],
            userData.consumosSemanais_before['tuesday'],
            userData.consumosSemanais_before['wednesday'],
            userData.consumosSemanais_before['thursday'],
            userData.consumosSemanais_before['friday'],
            userData.consumosSemanais_before['saturday'],
            userData.consumosSemanais_before['sunday']
          ],
          color: '#bdc3c7'
        }
      ];

      chargingStations.value = Object.entries(userData.postos).map (([key, station]) => ({
        id: key,
        address: station.morada,
        status: station.estado,
      }));

      expensesData.value = Object.entries(userData.custosMensais).map(([key, mes]) => ({
        month: key,
        value: mes.custo,
        color: '#' + Math.floor(Math.random() * 16777215).toString(16) // Gera uma cor aleatória
      }));

    } else {
      console.error('Formato de dados inválido recebido da API.');
    }
  } catch (error) {
    console.error('Error:', error);
    state.isAuthenticated = false;
  }
});
</script>

<style scoped>

   /* Estilo para a scrollbar personalizada */
 .custom-scrollbar::-webkit-scrollbar {
   width: 6px;
 }

.custom-scrollbar::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 10px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}


</style>