
// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import DasboardView from '../views/DashboardView.vue';
import ListUsers from '@/views/ListUsers.vue';
import RegistarEntidade from '../views/RegistarEntidadeView.vue'
import SigninView from '@/views/SigninView.vue';
import AddUserView from "@/views/AddUserView.vue";
import MyVehiclesView from "@/views/MyVehiclesView.vue";
import ListAllVechilesView from "@/views/ListAllVechilesView.vue";
import VehicleDetailView from "@/views/VehicleDetailView.vue";
import ProfileUserView from '@/views/ProfileUserView.vue';
import AddVehiclesView from '@/views/AddVehiclesView.vue';
import { compile } from 'vue';
import HomeView from '@/views/HomeView.vue';
import PersonalStatisticsView from '@/views/PersonalStatisticsView.vue';
import RequestVehicleAdminView from '@/views/RequestVehicleAdminView.vue';



const routes = [

  {
    path: '/',
    name:'home',
    component: HomeView,
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
    path: '/utilizadores/perfil',
    name: 'userprofile',
    component: ProfileUserView,
    meta: { layout: 'default' }
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
  {
    path: '/frota/meus-veiculos/detail/:id',
    name: 'vehicledetail',
    component: VehicleDetailView,
    props: true,
    meta: { layout: 'default' }
  },
  {
    path: '/frota/adicionar-veiculo',
    name: 'addvehicles',
    component: AddVehiclesView,
    meta: {layout: 'default' }
  },

  {
    path: '/estatisticas/pessoais',
    name: 'personalstatistics',
    component: PersonalStatisticsView,
    meta: { layout: 'default' }


  {
    path: '/frota/requisicoes',
    name: 'requisitions',
    component: RequestVehicleAdminView,
    meta: {layout: 'default' }

  }
  
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;


