<template>
  <div class="bg-white rounded-lg shadow-sm overflow-hidden h-full flex flex-col">
    <h2 class="text-base font-medium p-4 border-b border-gray-200">Postos de carregamento</h2>

    <div class="flex-1 overflow-y-auto divide-y divide-gray-100">
      <div
          v-for="station in stations"
          :key="station.id"
          class="flex items-center p-4 cursor-pointer transition-colors"
          :class="{
          'hover:bg-gray-50': station.status === true && (!selectedStation || selectedStation.id !== station.id),
          'bg-extra-soft-orange border-l-4 border-soft-orange': selectedStation && selectedStation.id === station.id,
          'opacity-60': station.status !== true
        }"
          @click="selectStation(station)"
      >
        <div class="flex-shrink-0 mr-3">
          <FuelIcon/>
        </div>
        <div class="flex-1">
          <div class="font-medium">{{ station.address }}</div>
          <div
              class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium mt-1"
              :class="{
              'bg-green-100 text-green-800': station.status === true,
              'bg-red-100 text-red-800': station.status === false
            }"
          >
            {{ getStatusText(station.status) }}
          </div>
        </div>
        <div
            class="w-2 h-2 rounded-full ml-2"
            :class="{
            'bg-green-500': station.status === true,
            'bg-red-500': station.status === false
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
import { FuelIcon } from 'lucide-vue-next';

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
    case true:
      return 'Disponível';
    case false:
      return 'Em uso';
    default:
      return status;
  }
}

function selectStation(station) {
  emit('select-station', station);
}
</script>