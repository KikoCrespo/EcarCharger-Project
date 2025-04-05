// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import SignIn from '../views/SigninView.vue'; 
import Home from '../views/HomeView.vue';

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
  
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
