<template>
  <div class="max-w-md mx-auto mt-10 p-6 bg-white rounded shadow">
    <h1 class="text-xl font-bold text-center mb-4">Painel de Carregamento</h1>

    <!-- Gráfico radial -->
    <apexchart
        type="radialBar"
        height="350"
        :options="chartOptions"
        :series="series"
    />

    <!-- Botões conforme estado -->
    <div class="mt-6 flex justify-center gap-4">
      <!-- Iniciar se nada ativo e sem sessão pendente -->
      <button
          v-if="!sessionId && !sessionClosed"
          @click="startCharging"
          class="px-4 py-2 bg-green-500 text-white rounded"
      >
        Iniciar Carregamento
      </button>

      <!-- Terminar durante carregamento -->
      <button
          v-if="isConnected"
          @click="finishCharging"
          class="px-4 py-2 bg-red-500 text-white rounded"
      >
        Terminar Carregamento
      </button>

      <!-- Concluir após paragem automática -->
      <button
          v-if="sessionClosed && !isConnected"
          @click="finishCharging"
          class="px-4 py-2 bg-blue-600 text-white rounded"
      >
        Concluir Carregamento
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onBeforeUnmount, onMounted } from 'vue'
import axios from 'axios'
import ApexChart from 'vue3-apexcharts'

const isConnected   = ref(false)
const sessionId     = ref(null)
const sessionClosed = ref(false)
const socket        = ref(null)
const series        = ref([0, 0, 0, 0])

// Arrays para médias
const voltages    = ref([])
const currents    = ref([])
const powers      = ref([])
const frequencies = ref([])

// IDs de exemplo
const vehicleId = 1
const stationId = 2
const userId    = 3


const chartOptions = {
  chart: { height: 350, type: 'radialBar' },
  plotOptions: {
    radialBar: {
      startAngle: 0,
      endAngle: 270,
      hollow: { size: '30%' },
      dataLabels: { name: { show: false }, value: { show: false } },
      barLabels: {
        enabled: true,
        formatter: (name, opts) =>
            name + ': ' + opts.w.globals.series[opts.seriesIndex].toFixed(2)
      }
    }
  },
  labels: ['Tensão (V)', 'Corrente (A)', 'Potência (W)', 'Freq. (Hz)']
}

function handleMessage(msg) {
  const d = JSON.parse(msg.data)

  if (d.status === 'charging_started') {
    sessionId.value = d.session_id
    localStorage.setItem('sessionId', d.session_id)
    return
  }

  if (d.status === 'charging_auto_ended') {
    isConnected.value = false
    sessionClosed.value = true
    localStorage.setItem('sessionClosed', 'true')
    return
  }

  if (d.status === 'error') {
    console.error('WS Error:', d.message)
    isConnected.value = false
    return
  }

  if (d.status === 'charging_data' && d.data) {
    const { voltage, current, power, frequency } = d.data
    voltages.value.push(voltage)
    currents.value.push(current)
    powers.value.push(power)
    frequencies.value.push(frequency)
    series.value = [voltage, current, power, frequency]
  }
}

// Conecta ou reconecta o socket (sem reenviar start_charging)
function reconnectSocket() {
  socket.value = new WebSocket('ws://localhost:8000/ws/sensor/')
  socket.value.onopen    = () => { isConnected.value = true }
  socket.value.onmessage = handleMessage
  socket.value.onclose   = () => {
    isConnected.value = false
    // se ainda houver sessão pendente, tentamos reconectar
    if (sessionId.value && !sessionClosed.value) {
      setTimeout(reconnectSocket, 2000)
    }
  }
  socket.value.onerror   = () => { isConnected.value = false }
}

onMounted(() => {
  // Recarrega sessão pendente
  const savedId = localStorage.getItem('sessionId')
  const savedClosed = localStorage.getItem('sessionClosed') === 'true'
  if (savedId) {
    sessionId.value = savedId
    sessionClosed.value = savedClosed
    reconnectSocket()
  }
})

// Inicia a sessão: limpa flags e envia start_charging
function startCharging() {
  localStorage.removeItem('sessionId')
  localStorage.removeItem('sessionClosed')
  voltages.value = []; currents.value = []; powers.value = []; frequencies.value = []
  sessionClosed.value = false

  socket.value = new WebSocket('ws://localhost:x8000/ws/sensor/')
  socket.value.onopen    = () => {
    isConnected.value = true
    socket.value.send(JSON.stringify({
      action: 'start_charging',
      vehicle_id: vehicleId,
      station_id: stationId,
      user_id: userId
    }))
  }
  socket.value.onmessage = handleMessage
  socket.value.onclose   = () => { isConnected.value = false }
  socket.value.onerror   = () => { isConnected.value = false }
}

// Fecha socket, calcula médias e envia ao Django
async function finishCharging() {
  socket.value?.close()
  isConnected.value = false

  const avg = arr => arr.length ? arr.reduce((a,b)=>a+b,0)/arr.length : 0
  const payload = {
    voltage:   parseFloat(avg(voltages.value).toFixed(2)),
    current:   parseFloat(avg(currents.value).toFixed(2)),
    power:     parseFloat(avg(powers.value).toFixed(2)),
    frequency: parseFloat(avg(frequencies.value).toFixed(2)),
  }
  if (!sessionId.value) return

  try {
    await axios.post(
        `http://localhost:8000/api/carregamentos/${sessionId.value}/stop/`,
        payload
    )
    // cleanup
    localStorage.removeItem('sessionId')
    localStorage.removeItem('sessionClosed')
    sessionId.value = null
    sessionClosed.value = false
    series.value = [0,0,0,0]
  } catch(e) {
    console.error('Erro ao enviar stop ao Django:', e)
  }
}

onBeforeUnmount(() => {
  socket.value?.close()
})
</script>

<style scoped>
button { transition: background-color .2s }
</style>
