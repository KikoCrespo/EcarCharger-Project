import './assets/css/main.css'


import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios';
import VueApexCharts from 'vue3-apexcharts'


const app = createApp(App)

axios.defaults.baseURL = 'http://127.0.0.1:8000/api/'

app.use(router,axios)
app.component('apexchart', VueApexCharts)
app.mount('#app')

