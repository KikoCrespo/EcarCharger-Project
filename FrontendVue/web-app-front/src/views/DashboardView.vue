

<template>
  <div class="flex w-full flex-col items-center">
    <button
        @click="toggleConnection"
        class="mb-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
    >
      {{ isConnected ? 'Parar Carregamento' : 'Iniciar Carregamento' }}
    </button>

    <div id="chart">
      <apexchart type="radialBar" height="390" :options="chartOptions" :series="series" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

// Estados reativos
const isConnected = ref(false)
const socket = ref(null)
const series = ref([0, 0, 0, 0])

// Configurações do gráfico (mantidas como no original)
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

// Fechar conexão quando o componente é desmontado
onBeforeUnmount(() => {
  if (socket.value) {
    socket.value.close()
  }
})
</script>


