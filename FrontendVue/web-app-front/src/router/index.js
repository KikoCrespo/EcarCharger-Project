
// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/HomeView.vue';
import ListUsers from '@/views/ListUsers.vue';
import RegistarEntidade from '../views/RegistarEntidadeView.vue'
import SigninView from '@/views/SigninView.vue';
import AddUserView from "@/views/AddUserView.vue";
import MyVehiclesView from "@/views/MyVehiclesView.vue";
import ListAllVechilesView from "@/views/ListAllVechilesView.vue";

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
    path: '/utilizadores/listar',
    name: 'listusers',
    component: ListUsers,
    meta: { layout: 'default' }
  },
  {
    path: '/utilizadores/adicionar',
    name: 'adduser',
    component: AddUserView,
    meta: { layout: 'default' }
  },
  {
    path: '/frota/meus-veiculos',
    name: 'myvehicles',
    component: MyVehiclesView,
    meta: { layout: 'default' }
  },
  {
    path: '/frota/consultar',
    name: 'listvehicles',
    component: ListAllVechilesView,
    meta: { layout: 'default' }
  },
  
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;


