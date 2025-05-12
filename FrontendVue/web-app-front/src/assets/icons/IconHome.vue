<script setup>
defineProps({
  size: {
    type: [String, Number],
    default: 24,
  },
  color: {
    type: String,
    default: 'currentColor',
  },
  className: {
    type: String,
    default: '',
  },
})

</script>

<template>
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" :viewBox="'0 0 24 24'" stroke-width="1.5" :stroke="color" :width="size" :height="size" :class="className" aria-hidden="true" >
    <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12l8.955-8.955a1.125 1.125 0 011.591 0L21.75 12m-17.25-2.25v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875a1.125 1.125 0 011.125-1.125h2.25a1.125 1.125 0 011.125 1.125V21h4.125a1.125 1.125 0 001.125-1.125V9.75M8.25 21h8.25" />
  </svg>
</template>