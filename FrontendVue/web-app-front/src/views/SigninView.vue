<script setup>
import LoginForm from '@/components/LoginForm.vue';
import ImageSection from '@/components/LoginImageSection.vue';
</script>
<template>
      <div class="flex items-center justify-center centerComponent" >
      <div class="flex shadow-2xl bg-white rounded-xl max-w-4xl lg:w-400">
        <div class="col-span-1 sm:col-span-2 lg:w-2/4 ..."><LoginForm/></div>
        <div class="... hidden lg:block bg-soft-orange lg:w-2/4 rounded-r-lg"><ImageSection /></div>
      </div>
  </div>

</template>