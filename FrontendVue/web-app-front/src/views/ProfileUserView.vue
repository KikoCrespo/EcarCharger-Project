<script setup>
import ProfileForm from '@/components/ProfileForm.vue';
import { defineProps } from 'vue';

const props = defineProps({
    user_data: {
        type: Object,
        required: true
    }
});
</script>

<template>
    <div>
        <ProfileForm :user_data="user_data" />
    </div>
</template>