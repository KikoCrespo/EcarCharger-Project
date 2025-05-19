<template>

    <h1 class="dashboard-title">Dashboard</h1>

    <div class="dashboard-grid">
      <!-- Coluna da esquerda -->
      <div class="dashboard-column">
        <charging-stations-list
            :stations="chargingStations"
            :selected-station="selectedStation"
            @select-station="selectStation"
        />
      </div>

      <!-- Coluna central e direita -->
      <div class="dashboard-main">
        <!-- Medidores -->


        <!-- Área central com data e botão -->
        <div class="central-area">
          <div class="date-display">
            <div v-if="isConnected" id="chart">
              <apexchart type="radialBar" height="390" :options="chartOptions" :series="series" />
            </div>
            <p v-else>{{ currentDateTime }}</p>
          </div>
          <button class="new-charging-btn" @click="startNewCharging">
            {{ isConnected ? 'Parar Carregamento' : 'Iniciar Carregamento' }}
          </button>
        </div>

        <!-- Estatísticas -->
        <div class="statistics-section">
          <h2 class="section-title">Estatísticas</h2>

          <div class="statistics-grid">
            <!-- Consumo -->
            <div class="statistics-card">
              <consumption-card
                  :consumption="285"
                  :trend="-8.6"
                  :period="'last week'"
              />
            </div>

            <!-- Gráfico de linha -->
            <div class="statistics-card">
              <line-chart
                  :series="consumptionSeries"
                  :categories="consumptionCategories"
              />
            </div>

            <!-- Rating de gastos -->
            <div class="statistics-card">
              <expenses-bubble-chart
                  :expenses="expensesData"
              />
            </div>
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

</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import ChargingStationsList from '@/components/Dashboard/ChargingStationsList.vue';
//import GaugeChart from '@/components/Dashboard/GaugeChart.vue';
import ConsumptionCard from '@/components/Dashboard/ConsumptionCard.vue';
import LineChart from '@/components/Dashboard/LineChart.vue';
import ExpensesBubbleChart from '@/components/Dashboard/ExpensesBubbleChart.vue';
import VehicleSelectionModal from '@/components/Dashboard/VehicleSelectionModal.vue';

// Estado
const currentDateTime = ref(formatDateTime(new Date()));
const selectedStation = ref(null);
const showVehicleModal = ref(false);

const isConnected = ref(false)
const socket = ref(null)
const series = ref([0, 0, 0, 0])

//Socket

function startNewCharging() {
  // Verificar se há um posto selecionado
  if (!selectedStation.value) {
    alert('Por favor, selecione um posto de carregamento disponível primeiro.');
    return;
  }

  // Abrir a modal de seleção de veículo
  showVehicleModal.value = true;
}

function handleVehicleSelection({ vehicle, station }) {
  // Aqui você implementaria a lógica para iniciar o carregamento
  // com o veículo selecionado e o posto de carregamento
  console.log('Iniciando carregamento:', {
    vehicle: vehicle,
    station: station || selectedStation.value
  });

  // Atualizar o status do veículo para 'in-use'
  const vehicleIndex = vehicles.value.findIndex(v => v.id === vehicle.id);
  if (vehicleIndex !== -1) {
    vehicles.value[vehicleIndex].status = 'in-use';
  }

  // Atualizar o status do posto de carregamento
  const stationToUse = station || selectedStation.value;
  if (stationToUse) {
    const stationIndex = chargingStations.value.findIndex(s => s.id === stationToUse.id);
    if (stationIndex !== -1) {
      chargingStations.value[stationIndex].status = 'in-use';
    }
  }

  // Resetar a seleção de posto
  selectedStation.value = null;

  // Mostrar uma notificação de sucesso (você pode implementar um sistema de notificações)
  alert(`Carregamento iniciado para ${vehicle.model} (${vehicle.plate})`);
  toggleConnection();
}

const toggleConnection = async () => {
  if (!isConnected.value) {
    try {
      // Inicia a conexão
      startWebSocket();

      const response = await fetch('http://192.168.1.106:5000/send-data', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });

      if (!response.ok) {
        throw new Error('Falha ao iniciar');
      }

    } catch (error) {
      console.error('Erro:', error);
      socket.value?.close();
      isConnected.value = false;
    }
  } else {
    try {
      // Envia requisição de parada
      await fetch('http://192.168.1.106:5000/stop-read', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });

    } catch (error) {
      console.error('Erro ao parar:', error);
    } finally {
      socket.value?.close();
    }
  }
}

const startWebSocket = () => {
  socket.value = new WebSocket('ws://localhost:8000/ws/sensor/')

  socket.value.onopen = () => {
    console.log('WebSocket connected')
    isConnected.value = true
  }

  socket.value.onmessage = (event) => {
    const data = JSON.parse(event.data)
    console.log('Received sensor data:', data)

    if (data === null) {
      // Fecha a conexão quando recebe null
      socket.value.close()
      return
    }

    series.value = [
      parseFloat(data.voltage.toFixed(2)),
      parseFloat(data.current.toFixed(2)),
      parseFloat(data.power.toFixed(2)),
      parseFloat(data.frequency.toFixed(2))
    ]
  }

  socket.value.onclose = () => {
    console.log('WebSocket disconnected')
    isConnected.value = false
    series.value = [0, 0, 0, 0]
  }

  socket.value.onerror = (error) => {
    console.error('WebSocket error:', error)
    isConnected.value = false
  }
}

onBeforeUnmount(() => {
  if (socket.value) {
    socket.value.close()
  }
})

const chartOptions = ref({
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
})


// Dados simulados
const chargingStations = ref([
  {
    id: 1,
    name: 'Garagem',
    status: 'available',
    type: 'Rápido',
    power: '50kW'
  },
  {
    id: 2,
    name: 'Armazém 1.2',
    status: 'in-use',
    type: 'Normal',
    power: '22kW'
  },
  {
    id: 3,
    name: 'Armazém 1.3',
    status: 'available',
    type: 'Rápido',
    power: '50kW'
  },
  {
    id: 4,
    name: 'Armazém 1.2',
    status: 'in-use',
    type: 'Normal',
    power: '22kW'
  },
  {
    id: 5,
    name: 'Armazém 1.2',
    status: 'in-use',
    type: 'Lento',
    power: '7.4kW'
  }
]);

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
    name: 'Last 6 days',
    data: [75, 125, 150, 130, 100, 180],
    color: '#f39c12'
  },
  {
    name: 'Last Week',
    data: [85, 100, 120, 110, 95, 140],
    color: '#bdc3c7'
  }
]);

const consumptionCategories = ref(['01', '02', '03', '04', '05', '06']);

const expensesData = ref([
  { month: 'Março', value: 140.60, color: '#8e44ad' },
  { month: 'Julho', value: 123.12, color: '#1abc9c' },
  { month: 'Dezembro', value: 212.30, color: '#f39c12' }
]);

// Métodos
function formatDateTime(date) {
  const day = String(date.getDate()).padStart(2, '0');
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const year = date.getFullYear();
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');

  return `${day}-${month}-${year} ${hours}:${minutes}`;
}

function updateDateTime() {
  currentDateTime.value = formatDateTime(new Date());
}

function selectStation(station) {
  // Só permite selecionar postos disponíveis
  if (station.status === 'available') {
    selectedStation.value = station;
  } else {
    alert('Este posto não está disponível para carregamento.');
  }
}



// Lifecycle hooks
onMounted(() => {
  // Atualizar a data/hora a cada minuto
  setInterval(updateDateTime, 60000);
});
</script>

<style scoped>
.dashboard {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
  background-color: #f8f9fa;
  min-height: 100vh;
}

.dashboard-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #333;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 20px;
}

.gauges-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.central-area {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 15px;
  background-color: white;
}

.date-display {
  font-size: 18px;
  color: #555;
}

.new-charging-btn {
  background-color: #f8c291;
  color: #333;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
}

.new-charging-btn:hover {
  background-color: #f6b17f;
}

.section-title {
  font-size: 20px;
  font-weight: 500;
  margin-bottom: 20px;
  position: relative;
  text-align: center;
}

.section-title::before,
.section-title::after {
  content: '';
  position: absolute;
  top: 50%;
  height: 1px;
  background-color: #e0e0e0;
  width: calc(50% - 100px);
}

.section-title::before {
  left: 0;
}

.section-title::after {
  right: 0;
}

.statistics-grid {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 20px;
}

.statistics-grid .statistics-card:last-child {
  grid-column: span 2;
}

.statistics-card {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  padding: 15px;
}

@media (max-width: 1024px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }

  .gauges-container {
    grid-template-columns: repeat(2, 1fr);
  }

  .statistics-grid {
    grid-template-columns: 1fr;
  }

  .statistics-grid .statistics-card:last-child {
    grid-column: auto;
  }
}

@media (max-width: 640px) {
  .gauges-container {
    grid-template-columns: 1fr;
  }

  .central-area {
    flex-direction: column;
    gap: 15px;
  }

  .date-display {
    font-size: 16px;
  }
}
</style>