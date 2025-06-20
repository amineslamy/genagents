import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from './components/Dashboard.vue'
import AppCreateCharacter from './components/AppCreateCharacter.vue'
import AgentList from './components/AgentList.vue'

const routes = [
  { path: '/', component: Dashboard, name: 'Dashboard' },
  { path: '/create-character', component: AppCreateCharacter, name: 'CreateCharacter' },
  { path: '/agents', component: AgentList, name: 'AgentList' },
  // مسیرهای دیگر مثل محیط‌ها بعداً اضافه می‌شوند
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
