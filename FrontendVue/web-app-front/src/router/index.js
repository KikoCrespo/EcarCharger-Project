
// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import LoginView from '@/views/LoginView.vue'; 
import Home from '../views/HomeView.vue';
import ListUsers from '@/views/ListUsers.vue';
import RegistarEntidade from '../views/RegistarEntidadeView.vue'

const routes = [

  {
    path: '/',
    name:'home',
    component: Home

  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { layout: 'login' }
  },
  {
    path: '/entidades/adicionar',
    name: 'registarEntidade',
    component: RegistarEntidade,
    meta: { layout: 'default' }
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


