<template>
  <div class="p-4">
    <div class="flex flex-col md:flex-row items-center justify-between">
      <h3 class="flex text-base font-medium">Histórico de Carregamentos</h3>
      <div class="flex items-center gap-2 sm:ml-4 mt-2 sm:mt-0 whitespace-nowrap">
        <input
            type="text"
            v-model="searchQuery"
            placeholder="Pesquisar..."
            class="px-3 py-1 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
        />
        <select
            v-model="filterStation"
            class="px-3 py-1 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
        >
          <option value="">Todos os postos</option>
          <option v-for="station in uniqueStations" :key="station" :value="station">{{ station }}</option>
        </select>
      </div>
    </div>

    <div class="mt-2 overflow-x-auto">
      <div class="max-h-96 overflow-y-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50 sticky top-0 z-10">
          <tr>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer" @click="sortBy('date')">
              Data
              <span v-if="sortColumn === 'date'" class="ml-1">{{ sortDirection === 'asc' ? '↑' : '↓' }}</span>
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer" @click="sortBy('station')">
              Posto
              <span v-if="sortColumn === 'station'" class="ml-1">{{ sortDirection === 'asc' ? '↑' : '↓' }}</span>
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer" @click="sortBy('vehicle')">
              Veículo
              <span v-if="sortColumn === 'vehicle'" class="ml-1">{{ sortDirection === 'asc' ? '↑' : '↓' }}</span>
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer" @click="sortBy('duration')">
              Duração
              <span v-if="sortColumn === 'duration'" class="ml-1">{{ sortDirection === 'asc' ? '↑' : '↓' }}</span>
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer" @click="sortBy('energy')">
              Energia
              <span v-if="sortColumn === 'energy'" class="ml-1">{{ sortDirection === 'asc' ? '↑' : '↓' }}</span>
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer" @click="sortBy('cost')">
              Custo
              <span v-if="sortColumn === 'cost'" class="ml-1">{{ sortDirection === 'asc' ? '↑' : '↓' }}</span>
            </th>
          </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="charge in sortedAndFilteredHistory" :key="charge.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ formatDate(charge.date) }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ charge.station }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ charge.vehicle }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ charge.duration }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ charge.energy.toFixed(3) }} kWh</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ formatCurrency(charge.cost.toFixed(3)) }}</td>
          </tr>
          <tr v-if="sortedAndFilteredHistory.length === 0">
            <td colspan="6" class="px-6 py-4 text-center text-sm text-gray-500">
              Nenhum registro encontrado.
            </td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="mt-4 flex justify-between items-center text-sm text-gray-600">
      <div>
        Mostrando {{ sortedAndFilteredHistory.length }} de {{ chargingHistory.length }} registros
      </div>
      <div>
        <button
            class="px-3 py-1 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            @click="exportToCSV"
        >
          Exportar CSV
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, defineProps } from 'vue';

const props = defineProps({
  chargingHistory: {
    type: Array,
    required: true
  }
});

// Estado
const searchQuery = ref('');
const filterStation = ref('');
const sortColumn = ref('date');
const sortDirection = ref('desc');

// Computed
const uniqueStations = computed(() => {
  const stations = new Set(props.chargingHistory.map(charge => charge.station));
  return Array.from(stations);
});

const sortedAndFilteredHistory = computed(() => {
  let result = [...props.chargingHistory];

  // Filtrar por pesquisa
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    result = result.filter(charge =>
        charge.vehicle.toLowerCase().includes(query) ||
        charge.station.toLowerCase().includes(query)
    );
  }

  // Filtrar por posto
  if (filterStation.value) {
    result = result.filter(charge => charge.station === filterStation.value);
  }

  // Ordenar
  result.sort((a, b) => {
    let valueA, valueB;

    switch (sortColumn.value) {
      case 'date':
        valueA = new Date(a.date);
        valueB = new Date(b.date);
        break;
      case 'duration':
        // Converter duração para minutos para ordenação
        valueA = convertDurationToMinutes(a.duration);
        valueB = convertDurationToMinutes(b.duration);
        break;
      default:
        valueA = a[sortColumn.value];
        valueB = b[sortColumn.value];
    }

    if (valueA < valueB) return sortDirection.value === 'asc' ? -1 : 1;
    if (valueA > valueB) return sortDirection.value === 'asc' ? 1 : -1;
    return 0;
  });

  return result;
});

// Métodos
function sortBy(column) {
  if (sortColumn.value === column) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc';
  } else {
    sortColumn.value = column;
    sortDirection.value = 'asc';
  }
}

function formatDate(date) {
  const d = new Date(date);
  const day = String(d.getDate()).padStart(2, '0');
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const year = d.getFullYear();
  const hours = String(d.getHours()).padStart(2, '0');
  const minutes = String(d.getMinutes()).padStart(2, '0');

  return `${day}/${month}/${year} ${hours}:${minutes}`;
}

function formatCurrency(value) {
  return new Intl.NumberFormat('pt-PT', {
    style: 'currency',
    currency: 'EUR'
  }).format(value);
}

function convertDurationToMinutes(duration) {
  // Formato esperado: "1h 45m" ou "45m" ou "2h"
  let hours = 0;
  let minutes = 0;

  if (duration.includes('h')) {
    const hoursPart = duration.split('h')[0].trim();
    hours = parseInt(hoursPart, 10);
  }

  if (duration.includes('m')) {
    const minutesPart = duration.split('h').pop().split('m')[0].trim();
    minutes = parseInt(minutesPart, 10);
  }

  return hours * 60 + minutes;
}

function exportToCSV() {
  // Preparar cabeçalhos
  const headers = ['Data', 'Posto', 'Veículo', 'Duração', 'Energia (kWh)', 'Custo (€)'];

  // Preparar linhas
  const rows = sortedAndFilteredHistory.value.map(charge => [
    formatDate(charge.date),
    charge.station,
    charge.vehicle,
    charge.duration,
    charge.energy.toFixed(3),
    charge.cost.toFixed(2)
  ]);


  const csvContent = [
    headers.join(','),
    ...rows.map(row => row.join(','))
  ].join('\n');

  // Criar blob e link para download -  https://stackoverflow.com/questions/58292771/downloading-a-csv-of-file-using-vue-and-js
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.setAttribute('href', url);
  link.setAttribute('download', `historico_carregamentos_${new Date().toISOString().split('T')[0]}.csv`);
  link.style.visibility = 'hidden';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}
</script>