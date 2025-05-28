<template>
  <div class="p-4">
    <h3 class="text-base font-medium mb-4">Consumos</h3>
    <div class="text-3xl font-bold mb-3">{{ consumption }} kWh</div>

    <div
        class="flex items-center text-sm mb-2"
        :class="{ 'text-red-600': trend > 0, 'text-green-600': trend < 0 }"
    >
      <div class="mr-1">
        <svg v-if="trend < 0" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="7 13 12 18 17 13"></polyline>
          <polyline points="7 6 12 11 17 6"></polyline>
        </svg>
        <svg v-else xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="17 11 12 6 7 11"></polyline>
          <polyline points="17 18 12 13 7 18"></polyline>
        </svg>
      </div>
      <span>{{ Math.abs(trend) }}% vs {{ period }}</span>
    </div>

    <div class="text-xs text-gray-500">
      Dados de hoje, 2023
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

defineProps({
  consumption: {
    type: Number,
    required: true
  },
  trend: {
    type: Number,
    required: true
  },
  period: {
    type: String,
    default: 'last week'
  }
});
</script>