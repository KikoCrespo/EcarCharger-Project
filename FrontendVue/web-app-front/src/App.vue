<script>
import LoginForm from '@/components/LoginForm.vue';
import ImageSection from '@/components/LoginImageSection.vue';

export default {
components: {
  LoginForm,
  ImageSection
}
};
</script>

<template>
  <div class="flex items-center justify-center centerComponent" >
    <!-- <div class="flex w-full max-w-4xl bg-white shadow-lg rounded-lg overflow-hidden">-->
      <div class="grid grid-cols-1 sm:grid-cols-3 shadow-2xl bg-white rounded-xl max-w-4xl lg:w-400">
        <div class="col-span-1 sm:col-span-2 ..."><LoginForm/></div>
        <div class="... hidden sm:block bg-soft-orange rounded-r-lg"><ImageSection /></div>
      </div>
  </div>

</template>


