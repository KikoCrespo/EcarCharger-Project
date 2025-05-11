<template>
  <svg
      xmlns="http://www.w3.org/2000/svg"
      xmlns:xlink="http://www.w3.org/1999/xlink"
      :width="size"
      :height="size"
      viewBox="0 0 50 50"
      fill="none"
  >
    <rect fill="none" height="50" width="50" />
    <path
        d="M25,1C11.767,1,1,11.766,1,25c0,13.234,10.767,24,24,24s24-10.766,24-24C49,11.766,38.233,1,25,1z M25,44C14.524,44,6,35.477,6,25  S14.524,6,25,6s18.999,8.523,18.999,19S35.476,44,25,44z"
        :stroke="color"
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-miterlimit="10"
        stroke-width="2.1111"
    />
    <path
        d="M43.444,22c-8,0-11.841-5-18.444-5c-6.613,0-9.944,5-18.444,5 M29,42c0,0,0-6.205,0-8c0-2.684,2.26-5,5-5c1.241,0,9.056,0,9.056,0 M6.556,29c0,0,8.341,0,9.444,0c2.885,0,5,2.23,5,5c0,1.857,0,8,0,8"
        :stroke="color"
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-miterlimit="10"
        stroke-width="2"
    />
    <circle
        cx="25"
        cy="25"
        r="4"
        :stroke="color"
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-miterlimit="10"
        stroke-width="2"
    />
  </svg>
</template>

<script setup>
defineProps({
  color: {
    type: String,
    default: '#000000'
  },
  size: {
    type: [String, Number],
    default: 50
  }
})
</script>
