import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import RegistarEntidade from '../views/RegistarEntidadeView.vue'

const routes = [
    {
        path: '/login',
        name: 'login',
        component: LoginView,
        meta: { layout: 'login' }
    },
    {
        path: '/entidade/adicionar',
        name: 'registarEntidade',
        component: RegistarEntidade,
        meta: { layout: 'default' }
    }
    
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router
