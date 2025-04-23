import './assets/css/main.css'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'


const app = createApp(App)

app.use(router) // Usa o router antes de montar
app.mount('#app') // Monta so depois de estar tudo pronto 