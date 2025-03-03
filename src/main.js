import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import '@fortawesome/fontawesome-free/css/all.css'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'

Vue.config.productionTip = false

// Axios 기본 설정
axios.defaults.baseURL = process.env.VUE_APP_API_URL || 'http://localhost:5003'
axios.defaults.timeout = 10000 // 10초
axios.defaults.headers.common['Accept'] = 'application/json'

// Axios 인터셉터 설정
axios.interceptors.request.use(config => {
  console.log('API Request:', config.method.toUpperCase(), config.url)
  return config
})

axios.interceptors.response.use(
  response => {
    console.log('API Response:', response.status, response.data)
    return response
  },
  error => {
    console.error('API Error:', error.message)
    if (error.response) {
      console.error('Error Response:', error.response.data)
    }
    return Promise.reject(error)
  }
)

// 전역 에러 핸들러
Vue.config.errorHandler = (err, vm, info) => {
  console.error('Vue Error:', err)
  console.error('Error Info:', info)
}

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')