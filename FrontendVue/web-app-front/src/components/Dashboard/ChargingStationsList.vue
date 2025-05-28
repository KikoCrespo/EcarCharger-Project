<template>
  <div class="bg-white rounded-lg shadow-sm overflow-hidden h-full flex flex-col">
    <h2 class="text-base font-medium p-4 border-b border-gray-200">Postos de carregamento</h2>

    <div class="flex-1 overflow-y-auto divide-y divide-gray-100">
      <div
          v-for="station in stations"
          :key="station.id"
          class="flex items-center p-4 cursor-pointer transition-colors"
          :class="{
          'hover:bg-gray-50': station.status === 'available' && (!selectedStation || selectedStation.id !== station.id),
          'bg-extra-soft-orange border-l-4 border-soft-orange': selectedStation && selectedStation.id === station.id,
          'opacity-60': station.status !== 'available'
        }"
          @click="selectStation(station)"
      >
        <div class="flex-shrink-0 mr-3">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-gray-600">
            <path d="M11 19H7c-1.1 0-2-.9-2-2V7c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2v5"></path>
            <circle cx="16" cy="19" r="2"></circle>
            <path d="M19 19v-6l-3 3"></path>
          </svg>
        </div>
        <div class="flex-1">
          <div class="font-medium">{{ station.name }}</div>
          <div
              class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium mt-1"
              :class="{
              'bg-green-100 text-green-800': station.status === 'available',
              'bg-red-100 text-red-800': station.status === 'in-use',
              'bg-blue-100 text-blue-800': station.status === 'maintenance'
            }"
          >
            {{ getStatusText(station.status) }}
          </div>
        </div>
        <div
            class="w-2 h-2 rounded-full ml-2"
            :class="{
            'bg-green-500': station.status === 'available',
            'bg-red-500': station.status === 'in-use',
            'bg-blue-500': station.status === 'maintenance'
          }"
        ></div>
      </div>
    </div>

    <div class="p-4 border-t border-gray-200 text-xs text-gray-500">
      Selecione um posto disponível para poder efetuar um carregamento
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  stations: {
    type: Array,
    required: true
  },
  selectedStation: {
    type: Object,
    default: null
  }
});

const emit = defineEmits(['select-station']);

function getStatusText(status) {
  switch (status) {
    case 'available':
      return 'Disponível';
    case 'in-use':
      return 'Em uso';
    case 'maintenance':
      return 'Manutenção';
    default:
      return status;
  }
}

function selectStation(station) {
  emit('select-station', station);
}
</script>