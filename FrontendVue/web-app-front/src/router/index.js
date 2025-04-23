
// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import LoginView from '@/views/LoginView.vue'; 
import Home from '../views/HomeView.vue';
import ListUsers from '@/views/ListUsers.vue';
import RegistarEntidade from '../views/RegistarEntidadeView.vue'
import SigninView from '@/views/SigninView.vue';

const routes = [

  {
    path: '/',
    name:'home',
    component: Home,
    meta: { layout: 'default' }
  },
  {
    path: '/login',
    name: 'login',
    component: SigninView,
    meta: { layout: 'login' }
  },
  {
    path: '/entidades/adicionar',
    name: 'registarEntidade',
    component: RegistarEntidade,
    
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


