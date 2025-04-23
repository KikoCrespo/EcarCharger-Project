<script setup>
import NavBar from '@/components/NavBar.vue';
import SideBar from '@/components/SideBar.vue';
import Footer from '@/components/Footer.vue';
import { defineProps } from 'vue';

const props = defineProps({
    user_data: {
        type:Object,
        required: true
    }
});


</script>


<template>

<div class="flex h-full">
    <SideBar :user_data="user_data" class="hidden sm:flex"/>
    <NavBar :user_data="user_data" class=""/>
   
</div>

</template>
