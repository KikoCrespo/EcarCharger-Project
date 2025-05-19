<template>
  <div class="p-4">
    <div class="flex justify-between items-center mb-4">
      <h3 class="text-base font-medium">Consumos</h3>
      <div class="text-sm text-orange-500 font-medium cursor-pointer">Este Mês</div>
    </div>
    <div ref="chartRef" class="w-full h-64"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, defineProps } from 'vue';
import ApexCharts from 'apexcharts';

const props = defineProps({
  series: {
    type: Array,
    required: true
  },
  categories: {
    type: Array,
    required: true
  }
});

const chartRef = ref(null);
let chart = null;

function initChart() {
  const options = {
    series: props.series,
    chart: {
      height: 250,
      type: 'line',
      toolbar: {
        show: false
      },
      zoom: {
        enabled: false
      },
      fontFamily: 'Inter, sans-serif'
    },
    dataLabels: {
      enabled: false
    },
    stroke: {
      width: 3,
      curve: 'smooth'
    },
    grid: {
      borderColor: '#f1f1f1',
      row: {
        colors: ['transparent', 'transparent'],
        opacity: 0.5
      }
    },
    xaxis: {
      categories: props.categories,
      labels: {
        style: {
          colors: '#888'
        }
      }
    },
    yaxis: {
      labels: {
        formatter: function(val) {
          return val.toFixed(0);
        },
        style: {
          colors: '#888'
        }
      }
    },
    legend: {
      position: 'bottom',
      horizontalAlign: 'center',
      markers: {
        width: 8,
        height: 8,
        radius: 12
      },
      itemMargin: {
        horizontal: 15
      }
    },
    tooltip: {
      theme: 'light',
      y: {
        formatter: function(val) {
          return val + ' kWh';
        }
      }
    }
  };

  chart = new ApexCharts(chartRef.value, options);
  chart.render();
}

function updateChart() {
  if (chart) {
    chart.updateOptions({
      series: props.series,
      xaxis: {
        categories: props.categories
      }
    });
  }
}

watch(() => props.series, updateChart, { deep: true });
watch(() => props.categories, updateChart);

onMounted(() => {
  initChart();
});
</script>