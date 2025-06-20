import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from './components/Dashboard.vue'
import AppCreateCharacter from './components/AppCreateCharacter.vue'

const routes = [
  { path: '/', component: Dashboard, name: 'Dashboard' },
  { path: '/create-character', component: AppCreateCharacter, name: 'CreateCharacter' },
  // مسیرهای دیگر مثل لیست شخصیت‌ها و محیط‌ها بعداً اضافه می‌شوند
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
