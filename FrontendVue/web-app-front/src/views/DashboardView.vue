<template>
  <div class="flex w-full">
    <div id="chart">
      <apexchart type="radialBar" height="390" :options="chartOptions" :series="series" />
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

// --- ApexCharts ---
const series = ref([0, 0, 0, 0]) // voltage, current, power, pf
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

// --- WebSocket ---
onMounted(() => {
  const socket = new WebSocket('ws://localhost:8000/ws/sensor/')

  socket.onopen = () => {
    console.log('WebSocket connected')
  }

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data)
    console.log('Received sensor data:', data)

    if (data === null) {
      series.value = [
        parseFloat(0),
        parseFloat(0),
        parseFloat(0),
        parseFloat(0)
      ]
      return
    }

    series.value = [
      parseFloat(data.voltage.toFixed(2)),
      parseFloat(data.current.toFixed(2)),
      parseFloat(data.power.toFixed(2)),
      parseFloat(data.frequency.toFixed(2))
    ]
  }

  socket.onerror = (error) => {
    console.error('WebSocket error:', error)
  }
})

// REF: https://apexcharts.com/vue-chart-demos/radialbar-charts/custom-angle-circle/
</script>


