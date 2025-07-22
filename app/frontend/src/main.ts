import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import '@/assets/main.css'
import { setupAxiosInterceptors } from '@/config/axiosConfig'

const app = createApp(App)

app.use(createPinia())
app.use(router)

// Set up Axios interceptors for global error handling
setupAxiosInterceptors()

app.mount('#app')
