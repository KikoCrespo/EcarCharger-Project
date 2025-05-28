<script setup>
import { ref, onMounted } from 'vue';
import { initFlowbite } from 'flowbite';

const minDate = ref('');

// Funcao para formatar a data no formato dd-mm-yyyy
const getFormattedDate = () => {
  const today = new Date();
  const day = String(today.getDate()).padStart(2, '0');
  const month = String(today.getMonth() + 1).padStart(2, '0');
  const year = today.getFullYear();
  return `${day}-${month}-${year}`;
};

onMounted(() => {
  minDate.value = getFormattedDate();
  initFlowbite();
});


</script>

<template>
  <div id="date-range-picker" date-rangepicker class="flex items-center">
    <div class="relative">
      <div class="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none">
        <svg class="w-4 h-4 text-gray-500 dark:text-gray-400" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
          <path d="M20 4a2 2 0 0 0-2-2h-2V1a1 1 0 0 0-2 0v1h-3V1a1 1 0 0 0-2 0v1H6V1a1 1 0 0 0-2 0v1H2a2 2 0 0 0-2 2v2h20V4ZM0 18a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V8H0v10Zm5-8h10a1 1 0 0 1 0 2H5a1 1 0 0 1 0-2Z"/>
        </svg>
      </div>
      <input id="datepicker-range-start" datepicker datepicker-buttons datepicker-autoselect-today datepicker-format="dd-mm-yyyy" name="start" type="text" class="bg-background-orange border-0 text-gray-400 text-sm rounded-lg focus:ring-extra-soft-orange focus:border-extra-soft-orange block w-full ps-10 p-2.5 dark:bg-background-orange dark:placeholder-gray-400 dark:text-white dark:focus:ring-extra-soft-orange dark:focus:border-extra-soft-orange" placeholder="Data de início">
    </div>
    <span class="mx-4 text-gray-500">até</span>
    <div class="relative">
      <div class="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none">
        <svg class="w-4 h-4 text-gray-500 dark:text-gray-400" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
          <path d="M20 4a2 2 0 0 0-2-2h-2V1a1 1 0 0 0-2 0v1h-3V1a1 1 0 0 0-2 0v1H6V1a1 1 0 0 0-2 0v1H2a2 2 0 0 0-2 2v2h20V4ZM0 18a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V8H0v10Zm5-8h10a1 1 0 0 1 0 2H5a1 1 0 0 1 0-2Z"/>
        </svg>
      </div>
      <!-- O atributo datepicker-min-date é bindado com a data atual -->
      <input id="datepicker-range-end" datepicker datepicker-buttons datepicker-autoselect-today datepicker-format="dd-mm-yyyy" :datepicker-min-date="minDate" name="end" type="text" class="bg-background-orange border-0 text-gray-400 text-sm rounded-lg focus:ring-extra-soft-orange focus:border-extra-soft-orange block w-full ps-10 p-2.5 dark:bg-background-orange dark:placeholder-gray-400 dark:text-white dark:focus:ring-extra-soft-orange dark:focus:border-extra-soft-orange" placeholder="Data de fim">
    </div>
  </div>
</template>
