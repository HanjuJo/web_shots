import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import '@fortawesome/fontawesome-free/css/all.min.css'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import 'dayjs/locale/zh-cn'

// Configure dayjs
dayjs.extend(relativeTime)
dayjs.locale('zh-cn')

// Configure axios
axios.defaults.baseURL = process.env.VUE_APP_API_URL || 'http://localhost:5003'
axios.defaults.timeout = 10000
axios.defaults.headers.common['Accept'] = 'application/json'

// Axios interceptors
axios.interceptors.request.use(config => {
  const token = store.state.auth.token
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  console.log('API Request:', config.method.toUpperCase(), config.url)
  return config
})

axios.interceptors.response.use(
  response => {
    console.log('API Response:', response.status)
    return response
  },
  error => {
    console.error('API Error:', error.message)
    if (error.response) {
      console.error('Error Response:', error.response.data)
      if (error.response.status === 401) {
        store.dispatch('auth/logout')
        router.push('/auth')
      }
    }
    return Promise.reject(error)
  }
)

const app = createApp(App)

// Global properties
app.config.globalProperties.$axios = axios
app.config.globalProperties.$dayjs = dayjs

// Error handler
app.config.errorHandler = (err, vm, info) => {
  console.error('Vue Error:', err)
  console.error('Error Info:', info)
}

app.use(router)
app.use(store)

app.mount('#app')