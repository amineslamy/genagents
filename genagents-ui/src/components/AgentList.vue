<template>
  <main class="agent-list-page">
    <h2 class="text-xl font-bold mb-4">لیست شخصیت‌ها</h2>
    <input v-model="search" class="input mb-4" type="text" placeholder="جستجو بر اساس نام یا ویژگی..." />
    <div v-if="isLoading" class="loading-box mt-4">
      <span class="spinner"></span>
      <span>در حال دریافت لیست شخصیت‌ها...</span>
    </div>
    <div v-if="errorMessage" class="error-box mt-4">{{ errorMessage }}</div>
    <ul v-if="filteredAgents.length" class="agent-list">
      <li v-for="agent in filteredAgents" :key="agent.id" @click="selectAgent(agent)" class="agent-item">
        <span>نام کامل: {{ agent.full_name }}</span>
        <span>سن: {{ agent.age }}</span>
        <span>شغل: {{ agent.occupation }}</span>
        <span>علاقه‌مندی‌ها: {{ agent.interests?.join(', ') }}</span>
        <span class="agent-id">ID: {{ agent.id }}</span>
      </li>
    </ul>
    <div v-else-if="!isLoading && !errorMessage" class="mt-4">هیچ شخصیتی یافت نشد.</div>
    <div v-if="selectedAgent" class="selected-agent-box mt-6">
      <h3>شخصیت انتخاب‌شده:</h3>
      <div>نام کامل: {{ selectedAgent.full_name }}</div>
      <div>سن: {{ selectedAgent.age }}</div>
      <div>شغل: {{ selectedAgent.occupation }}</div>
      <div>علاقه‌مندی‌ها: {{ selectedAgent.interests?.join(', ') }}</div>
      <div>ID: {{ selectedAgent.id }}</div>
      <button @click="selectedAgent = null" class="submit-btn mt-2">بستن</button>
    </div>
  </main>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const agents = ref([])
const isLoading = ref(false)
const errorMessage = ref('')
const search = ref('')
const selectedAgent = ref(null)

const filteredAgents = computed(() => {
  if (!search.value) return agents.value
  const s = search.value.toLowerCase()
  return agents.value.filter(a =>
    (a.first_name + ' ' + a.last_name).toLowerCase().includes(s) ||
    (a.tags && a.tags.join(',').toLowerCase().includes(s))
  )
})

function selectAgent(agent) {
  selectedAgent.value = agent
}

async function fetchAgents() {
  isLoading.value = true
  errorMessage.value = ''
  try {
    const res = await fetch('/agents/')
    if (!res.ok) throw new Error('خطا در دریافت لیست شخصیت‌ها')
    const data = await res.json()
    console.log('API agents data:', data)
    // تبدیل داده‌ها به ساختار مورد انتظار
    agents.value = data.map(agent => {
      let first_name = '', last_name = ''
      if (agent.full_name) {
        const parts = agent.full_name.split(' ')
        first_name = parts[0] || ''
        last_name = parts.slice(1).join(' ') || ''
      }
      return {
        ...agent,
        first_name,
        last_name,
        tags: agent.tags || []
      }
    })
    console.log('Parsed agents:', agents.value)
  } catch (err) {
    errorMessage.value = '❌ خطا در دریافت لیست شخصیت‌ها'
  } finally {
    isLoading.value = false
  }
}

onMounted(fetchAgents)
</script>

<style scoped>
.agent-list {
  list-style: none;
  padding: 0;
}
.agent-item {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.2em;
  padding: 0.8em 1.2em;
  margin-bottom: 0.5em;
  background: #fafdff;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
}
.agent-item:hover {
  background: #e3eafc;
}
.agent-id {
  color: #1976d2;
  font-size: 0.95em;
}
.selected-agent-box {
  background: #f5faff;
  border-radius: 8px;
  padding: 1.2em;
  box-shadow: 0 2px 8px #1976d210;
}
</style>
