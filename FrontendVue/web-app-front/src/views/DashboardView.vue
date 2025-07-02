<template>
  <div class="max-w-md mx-auto mt-10 p-6 bg-white rounded shadow">
    <h1 class="text-xl font-bold text-center mb-4">Painel de Carregamento</h1>

    <!-- Debug info (remover em produção) -->
    <div class="text-xs text-gray-400 mb-2">
      Debug: sessionId={{ sessionId }}, isConnected={{ isConnected }}, sessionClosed={{ sessionClosed }}, sessionSummary={{ !!sessionSummary }}
    </div>

    <!-- Gráfico radial -->
    <apexchart
        type="radialBar"
        height="350"
        :options="chartOptions"
        :series="series"
    />

    <!-- Status do carregamento -->
    <div class="mt-4 text-center" v-if="sessionId">
      <p class="text-gray-700">
        <span v-if="isConnected" class="text-green-500 font-semibold">
          Carregamento em andamento
        </span>
        <span v-else-if="sessionClosed" class="text-orange-500 font-semibold">
          Carregamento finalizado automaticamente
        </span>
      </p>
      <p class="text-sm text-gray-500" v-if="sessionStartTime">
        Iniciado: {{ formatDateTime(sessionStartTime) }}
      </p>
      <p class="text-sm text-gray-500" v-if="autoEndTime">
        Finalizado: {{ formatDateTime(autoEndTime) }}
      </p>
    </div>

    <!-- Resumo da sessão -->
    <div v-if="sessionSummary" class="mt-4 p-3 bg-orange rounded">
      <h3 class="font-semibold text-center mb-2">Resumo do Carregamento</h3>
      <div class="grid grid-cols-2 gap-2 text-sm">
        <div>Duração:</div>
        <div>{{ formatDuration(sessionSummary.duration) }}</div>
        <div>Voltagem média:</div>
        <div>{{ sessionSummary.avg_voltage.toFixed(1) }} V</div>
        <div>Corrente média:</div>
        <div>{{ sessionSummary.avg_current.toFixed(1) }} A</div>
        <div>Potência média:</div>
        <div>{{ sessionSummary.avg_power.toFixed(2) }} kW</div>
        <div>Energia consumida:</div>
        <div>{{ sessionSummary.energy_consumed.toFixed(2) }} kWh</div>
      </div>
    </div>

    <!-- Botões conforme estado -->
    <div class="mt-6 flex justify-center gap-4">
      <button
          v-if="!sessionId && !sessionClosed"
          @click="startCharging"
          class="inline-flex items-center rounded-md bg-extra-soft-orange px-3 py-2 text-sm font-semibold text-gray-900 shadow-xs hover:bg-soft-orange duration-300"
      >
        Iniciar Carregamento
      </button>

      <button
          v-if="isConnected && sessionId"
          @click="finishCharging"
          class="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
      >
        Terminar Carregamento
      </button>

      <button
          v-if="sessionClosed && !sessionSummary"
          @click="confirmAutoEnd"
          class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Concluir Carregamento
      </button>

      <button
          v-if="sessionSummary"
          @click="resetSession"
          class="inline-flex items-center rounded-md bg-extra-soft-orange px-3 py-2 text-sm font-semibold text-gray-900 shadow-xs hover:bg-soft-orange duration-300"
      >
        Novo Carregamento
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onBeforeUnmount, onMounted } from 'vue'
import ApexChart from 'vue3-apexcharts'

const isConnected = ref(false)
const sessionId = ref(null)
const sessionClosed = ref(false)
const sessionStartTime = ref(null)
const sessionSummary = ref(null)
const autoEndTime = ref(null)
const socket = ref(null)
const series = ref([0, 0, 0, 0])
const shouldReconnect = ref(true) // Nova flag para controlar reconexão

// IDs de exemplo
const vehicleId = 1
const stationId = 2
const userId = 3

const chartOptions = {
  chart: {
    height: 350,
    type: 'radialBar',
  },
  plotOptions: {
    radialBar: {
      dataLabels: {
        name: {
          fontSize: '22px',
        },
        value: {
          fontSize: '16px',
        },
        total: {
          show: true,
          label: 'Total',
          formatter: function () {
            return '100%'
          }
        }
      }
    }
  },
  labels: ['Voltagem', 'Corrente', 'Potência', 'Frequência'],
  colors: ['#546E7A', '#E91E63', '#FF9800', '#4CAF50'],
}

function formatDateTime(isoString) {
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

// Conecta ou reconecta o socket
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

onMounted(() => {
  // Recuperar sessão existente
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
})

// Inicia nova sessão
function startCharging() {
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
      vehicle_id: vehicleId,
      station_id: stationId,
      user_id: userId
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

// Finalização manual
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
</script>

