<template>
  <div class="p-4">
    <h3 class="text-base font-medium mb-4">Consumos</h3>
    <div class="text-3xl font-bold mb-3">{{ consumption.toFixed(2) }} kWh</div>

    <div
        class="flex items-center text-sm"
        :class="trend > 0 ? 'text-red-600' : 'text-green-600'"
    >
      <div class="mr-1">
        <ChevronUp v-if="trend > 0 && trend <=50" class="w-4 h-4" />
        <ChevronsUp v-if="trend > 50" class="w-4 h-4" />
        <ChevronDown v-if="trend < 0 && trend >= -50" class="w-4 h-4" />
        <ChevronsDown v-if="trend < -50" class="w-4 h-4" />
      </div>
      <span>{{ Math.abs(trend) }}% vs {{ period === 'weekly' ? 'semana anterior' : 'mês anterior' }}</span>
    </div>

    <div class="text-xs text-gray-500">
      Dados de hoje, 2023
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';
import { ChevronUp, ChevronsUp, ChevronDown, ChevronsDown } from 'lucide-vue-next';

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
    default: 'weekly'
  }
});
</script>