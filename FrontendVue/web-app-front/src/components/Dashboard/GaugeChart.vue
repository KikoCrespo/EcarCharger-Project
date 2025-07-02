<template>
  <div class="bg-white rounded-lg border border-gray-200 shadow-sm">
    <!-- Chart or Date Display -->
    <div v-if="sessionStartTime || autoEndTime" class="p-2 space-y-2">
      <div v-if="sessionStartTime" class="flex items-center gap-2 text-sm text-gray-600 px-3 py-2  rounded-md">
        <svg class="w-4 h-4 flex-shrink-0 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <circle cx="12" cy="12" r="10"></circle>
          <polyline points="12,6 12,12 16,14"></polyline>
        </svg>
        <span>Iniciado: {{ formatDateTimeSecond(sessionStartTime) }}</span>
      </div>
      <div v-if="autoEndTime" class="flex items-center gap-2 text-sm text-gray-600 px-3 py-2 rounded-md">
        <svg class="w-4 h-4 flex-shrink-0 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <circle cx="12" cy="12" r="10"></circle>
          <polyline points="12,6 12,12 16,14"></polyline>
        </svg>
        <span>Finalizado: {{ formatDateTimeSecond(autoEndTime) }}</span>
      </div>
    </div>
    <div class="flex justify-center items-center p-4">
      <div v-if="isConnected && !sessionSummary" class="w-full flex justify-center">
        <apexchart
            type="radialBar"
            height="350"
            :options="chartOptions"
            :series="normalizedSeries"
        />
      </div>
      <div v-else class="flex justify-center items-center min-h-[150px]">
        <div class="p-2.5 mt-1 flex items-center justify-center">
          <img  v-if="electric_car" :src="electric_car" :alt="currentDateTime" class="h-30 w-auto object-couver" />
          <div v-else class="flex items-center gap-3 text-xl font-medium text-gray-700 px-6 py-4 bg-gray-50 rounded-lg border border-gray-200">
            <Clock/>
            <span>{{ currentDateTime }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Session Info -->

    <!-- Session Summary -->
    <div v-if="sessionSummary" class="px-4 pb-4">
      <div class=" border-2 border-extra-soft-orange rounded-lg p-6">
        <h3 class="flex items-center justify-center gap-2 text-base font-semibold text-gray-900 mb-3">
          <BookCheck class="" />
          Resumo do Carregamento
        </h3>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
          <div class="flex justify-between items-center px-3 py-2 bg-white rounded border border-extra-soft-orange">
            <span class="text-xs text-gray-600 font-medium">Duração:</span>
            <span class="text-xs font-semibold text-gray-900">{{ formatDuration(sessionSummary.duration) }}</span>
          </div>
          <div class="flex justify-between items-center px-3 py-2 bg-white rounded border border-extra-soft-orange">
            <span class="text-xs text-gray-600 font-medium">Voltagem média:</span>
            <span class="text-xs font-semibold text-gray-900">{{ sessionSummary.avg_voltage.toFixed(1) }} V</span>
          </div>
          <div class="flex justify-between items-center px-3 py-2 bg-white rounded border border-extra-soft-orange">
            <span class="text-xs text-gray-600 font-medium">Corrente média:</span>
            <span class="text-xs font-semibold text-gray-900">{{ sessionSummary.avg_current.toFixed(2) }} A</span>
          </div>
          <div class="flex justify-between items-center px-3 py-2 bg-white rounded border border-extra-soft-orange">
            <span class="text-xs text-gray-600 font-medium">Potência média:</span>
            <span class="text-xs font-semibold text-gray-900">{{ sessionSummary.avg_power.toFixed(2) }} kW</span>
          </div>
          <div class="flex justify-between items-center px-3 py-2 bg-extra-soft-orange/40 rounded border border-extra-soft-orange sm:col-span-2">
            <span class="text-xs text-gray-900 font-medium">Energia consumida:</span>
            <span class="text-sm font-bold text-gray-900">{{ sessionSummary.energy_consumed.toFixed(2) }} kWh</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="px-4 pb-4">
      <div class="flex justify-center gap-3 flex-wrap">
        <button
            v-if="!sessionId && !sessionClosed"
            @click="emit('start-charging')"
            class="inline-flex items-center rounded-md bg-emerald-400 px-3 py-2 text-sm font-semibold text-white shadow-xs hover:bg-emerald-500 duration-300"
        >
          <Play class="mr-1.5 -ml-0.5 size-5" aria-hidden="true"/>
          Iniciar Carregamento
        </button>

        <button
            v-if="isConnected && sessionId"
            @click="emit('finish-charging')"
            class="inline-flex items-center rounded-md bg-red-400 px-3 py-2 text-sm font-semibold text-white shadow-xs hover:bg-red-500 duration-300"
        >

          <OctagonMinus class="mr-1.5 -ml-0.5 size-5" />
          Terminar Carregamento
        </button>

        <button
            v-if="sessionClosed && !sessionSummary"
            @click="emit('confirm-auto-end')"
            class="flex items-center gap-2 px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg font-medium text-sm transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <polyline points="20,6 9,17 4,12"></polyline>
          </svg>
          Concluir Carregamento
        </button>

        <button
            v-if="sessionSummary"
            @click="emit('reset-session')"
            class="inline-flex items-center rounded-md bg-extra-soft-orange px-3 py-2 text-sm font-semibold text-gray-900 shadow-xs hover:bg-soft-orange duration-300"
        >
          <Repeat2 class="mr-1.5 -ml-0.5 size-5" />
          Novo Carregamento
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import {Clock, Play, OctagonMinus, Repeat2, BookCheck} from 'lucide-vue-next'
import electric_car from '@/assets/img/electric_car.png'


const props = defineProps({
  isConnected: {
    type: Boolean,
    default: false
  },
  sessionId: {
    type: [String, Number],
    default: null
  },
  sessionClosed: {
    type: Boolean,
    default: false
  },
  sessionStartTime: {
    type: String,
    default: null
  },
  sessionSummary: {
    type: Object,
    default: null
  },
  autoEndTime: {
    type: String,
    default: null
  },
  series: {
    type: Array,
    default: () => [0, 0, 0, 0]
  },
  currentDateTime: {
    type: String,
    default: ''
  }
})

const emit = defineEmits([
  'start-charging',
  'finish-charging',
  'confirm-auto-end',
  'reset-session'
])

// Normalize series data to percentages to prevent overlap
const normalizedSeries = computed(() => {
  const maxValues = [250, 50, 100, 60] // Max expected values for V, A, kW, Hz
  return props.series.map((value, index) => {
    const percentage = Math.min((value / maxValues[index]) * 100, 100)
    return Math.round(percentage)
  })
})

const chartOptions = ref({
  chart: {
    height: 350,
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
        fontSize: '14px',
        formatter: function (seriesName, opts) {
          const actualValue = props.series[opts.seriesIndex]
          const units = ['V', 'A', 'kW', 'Hz']
          return `${seriesName}: ${actualValue}${units[opts.seriesIndex]}`
        }
      }
    }
  },
  colors: ['#FFB38E', '#FFCF9D', '#FFB26F', '#DE8F5F'],
  labels: ['Tensão', 'Corrente', 'Potência', 'Frequência'],
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

function formatDateTimeSecond(isoString) {
  if (!isoString) return ''
  const date = new Date(isoString)
  return date.toLocaleString('pt-PT', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

function formatDuration(seconds) {
  if (!seconds) return '0s'
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const remainingSeconds = Math.floor(seconds % 60)

  let result = ''
  if (hours > 0) result += `${hours}h `
  if (minutes > 0) result += `${minutes}m `
  if (remainingSeconds > 0 || result === '') result += `${remainingSeconds}s`

  return result
}
</script>