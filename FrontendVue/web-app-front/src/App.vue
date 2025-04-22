<script setup>
import { useRoute } from 'vue-router'
import { computed } from 'vue'

import DefaultLayout from '@/layouts/DefaultLayout.vue'
import LoginLayout from '@/layouts/LoginLayout.vue'

const route = useRoute()

const layout = computed(() => {
  switch (route.meta.layout) {
    case 'login':
      return LoginLayout
    default:
      return DefaultLayout
  }
})
</script>

<template>
  <component :is="layout" />
</template>
