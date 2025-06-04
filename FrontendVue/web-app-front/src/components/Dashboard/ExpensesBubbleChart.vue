<template>
  <div class="p-4">
    <h3 class="text-base font-medium mb-1">Rating de gastos</h3>
    <p class="text-xs text-gray-500 mb-4">Apresentação dos 3 meses com mais gastos em consumo</p>
    <div ref="chartRef" class="w-full h-72"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, defineProps } from 'vue';
import ApexCharts from 'apexcharts';

const props = defineProps({
  expenses: {
    type: Array,
    required: true
  }
});

const chartRef = ref(null);
let chart = null;

function initChart() {
  // Preparar dados para o gráfico
  const series = [{
    name: 'Gastos',
    data: props.expenses.map(item => ({
      x: item.month,
      y: item.value,
      z: calculateBubbleSize(item.value),
      fillColor: item.color
    }))
  }];

  const options = {
    series: series,
    chart: {
      height: 350,
      type: 'bubble',
      toolbar: {
        show: false
      },
      fontFamily: 'Inter, sans-serif'
    },
    dataLabels: {
      enabled: false
    },
    fill: {
      opacity: 0.8,
      type: 'solid'
    },
    title: {
      show: false
    },
    xaxis: {
      tickAmount: 12,
      type: 'category',
      labels: {
        style: {
          colors: '#888'
        }
      }
    },
    yaxis: {
      labels: {
        formatter: function(val) {
          return val.toFixed(2) + '€';
        },
        style: {
          colors: '#888'
        }
      }
    },
    tooltip: {
      theme: 'light',
      y: {
        formatter: function(val) {
          return val.toFixed(2) + '€';
        }
      }
    },
    legend: {
      show: false
    }
  };

  chart = new ApexCharts(chartRef.value, options);
  chart.render();
}

function calculateBubbleSize(value) {
  // Calcular tamanho da bolha com base no valor
  // Valores maiores = bolhas maiores
  return value / 2;
}

function updateChart() {
  if (chart) {
    const series = [{
      name: 'Gastos',
      data: props.expenses.map(item => ({
        x: item.month,
        y: item.value,
        z: calculateBubbleSize(item.value),
        fillColor: item.color
      }))
    }];

    chart.updateSeries(series);
  }
}

watch(() => props.expenses, updateChart, { deep: true });

onMounted(() => {
  console.log('Dados de despesas recebidos:', props.expenses);
  initChart();
});
</script>