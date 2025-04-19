// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import SignIn from '../views/SigninView.vue'; 
import Home from '../views/HomeView.vue';
import ListUsers from '@/views/ListUsers.vue';

const routes = [

  {
    path: '/',
    name:'home',
    component: Home

  },
  {
    path: '/signin',
    name: 'signin',
    component: SignIn,
  },
  {
    path: '/users/list',
    name: 'listusers',
    component: ListUsers,
  },
  
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
