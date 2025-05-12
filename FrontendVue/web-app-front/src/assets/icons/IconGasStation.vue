<template>
  <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 256 256"
      :width="size"
      :height="size"
      fill="none"
  >
    <rect fill="none" height="256" width="256" />
    <path
        d="M56,216V56A16,16,0,0,1,72,40h80a16,16,0,0,1,16,16V216"
        :stroke="color"
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="12"
    />
    <line
        :stroke="color"
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="12"
        x1="32"
        x2="192"
        y1="216"
        y2="216"
    />
    <path
        d="M168,112h24a16,16,0,0,1,16,16v40a16,16,0,0,0,16,16h0a16,16,0,0,0,16-16V86.6a16.1,16.1,0,0,0-4.7-11.3L216,56"
        :stroke="color"
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="12"
    />
    <line
        :stroke="color"
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="12"
        x1="136"
        x2="88"
        y1="112"
        y2="112"
    />
  </svg>
</template>

<script setup>
defineProps({
  color: {
    type: String,
    default: '#000'
  },
  size: {
    type: [String, Number],
    default: 24
  }
})
</script>

