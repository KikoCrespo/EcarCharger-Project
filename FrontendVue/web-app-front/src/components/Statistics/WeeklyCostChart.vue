<template>
  <div class="p-4">
    <div class="flex justify-between items-center mb-4">
      <h3 class="text-base font-medium">Custos {{ period === 'weekly' ? 'Semanais' : 'Mensais' }}</h3>
      <div class="flex items-center gap-2">
        <div
            v-for="(series, index) in costData"
            :key="index"
            class="flex items-center gap-1"
        >
          <div
              class="w-3 h-3 rounded-full"
              :style="{ backgroundColor: series.color }"
          ></div>
          <span class="text-xs text-gray-600">{{ series.name }}</span>
        </div>
      </div>
    </div>
    <div ref="chartRef" class="w-full h-80"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, defineProps } from 'vue';
import ApexCharts from 'apexcharts';

const props = defineProps({
  period: {
    type: String,
    required: true,
    validator: (value) => ['weekly', 'monthly'].includes(value)
  },
  costData: {
    type: Array,
    required: true
  }
});

const chartRef = ref(null);
let chart = null;

function initChart() {
  const categories = props.period === 'weekly'
      ? ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
      : ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'];

  const options = {
    series: props.costData,
    chart: {
      type: 'bar',
      height: 320,
      toolbar: {
        show: false
      },
      fontFamily: 'Inter, sans-serif'
    },
    plotOptions: {
      bar: {
        horizontal: false,
        columnWidth: '55%',
        borderRadius: 4,
        endingShape: 'rounded'
      },
    },
    dataLabels: {
      enabled: false
    },
    stroke: {
      show: true,
      width: 2,
      colors: ['transparent']
    },
    xaxis: {
      categories: categories,
      labels: {
        style: {
          colors: '#888'
        }
      }
    },
    yaxis: {
      title: {
        text: 'EUR (€)',
        style: {
          color: '#888'
        }
      },
      labels: {
        formatter: function(val) {
          return val.toFixed(2) + '€';
        },
        style: {
          colors: '#888'
        }
      }
    },
    fill: {
      opacity: 1
    },
    tooltip: {
      y: {
        formatter: function(val) {
          return val.toFixed(2) + '€';
        }
      }
    },
    legend: {
      show: false
    },
    grid: {
      borderColor: '#f1f1f1',
      row: {
        colors: ['transparent', 'transparent'],
        opacity: 0.5
      }
    }
  };

  chart = new ApexCharts(chartRef.value, options);
  chart.render();
}

function updateChart() {
  if (chart) {
    const categories = props.period === 'weekly'
        ? ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
        : ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho'];

    chart.updateOptions({
      series: props.costData,
      xaxis: {
        categories: categories
      }
    });
  }
}

watch(() => props.period, updateChart);
watch(() => props.costData, updateChart, { deep: true });

onMounted(() => {
  initChart();
});
</script>