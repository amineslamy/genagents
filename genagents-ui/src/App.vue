<template>
  <main dir="rtl" class="p-4" style="font-family: Vazirmatn, Tahoma">
    <h2 class="text-xl font-bold mb-4">ساخت شخصیت جدید</h2>
    <div class="accordion-form">
      <div class="accordion-section">
        <button class="accordion-header" @click="toggleSection(0)">
          اطلاعات شخصی
        </button>
        <div v-show="activeSection === 0" class="accordion-content">
          <PersonalInfo :form="form" />
        </div>
      </div>
      <div class="accordion-section">
        <button class="accordion-header" @click="toggleSection(1)">
          🧠 پرسشنامه شخصیت (Big Five)
        </button>
        <div v-show="activeSection === 1" class="accordion-content">
          <BigFive ref="bigfive" />
        </div>
      </div>
      <div class="accordion-section">
        <button class="accordion-header" @click="toggleSection(2)">
          📋 پرسشنامه اجتماعی سیاسی (GSS)
        </button>
        <div v-show="activeSection === 2" class="accordion-content">
          <GSS ref="gss" />
        </div>
      </div>
      <div class="accordion-section">
        <button class="accordion-header" @click="toggleSection(3)">
          💰 پرسشنامه اقتصاد رفتاری
        </button>
        <div v-show="activeSection === 3" class="accordion-content">
          <Behavioral ref="behavioral" />
        </div>
      </div>
      <div class="accordion-section">
        <button class="accordion-header" @click="toggleSection(4)">
          جملات کوتاه درباره شخصیت
        </button>
        <div v-show="activeSection === 4" class="accordion-content">
          <label class="font-bold block mb-2">جملات کوتاه درباره شخصیت (هر جمله در یک خط):</label>
          <textarea v-model="form.character_sentences" rows="5" class="input" placeholder="مثال: فردی اجتماعی است&#10;به مطالعه علاقه دارد&#10;..." />
        </div>
      </div>
      <button @click="createAgent" :disabled="isLoading" class="submit-btn mt-6" style="min-width: 160px;">
        <span v-if="isLoading">⏳ در حال ثبت شخصیت...</span>
        <span v-else>📨 ثبت شخصیت</span>
      </button>
      <button v-if="agentId" @click="reflectAgent" class="submit-btn mt-3 bg-green-600">🧠 بازتاب فکری</button>
      <button v-if="successMessage" @click="refreshForm" class="submit-btn mt-3 bg-gray-500">🔄 تازه‌سازی پرسشنامه</button>
      <div v-if="isLoading" class="loading-box mt-4">
        <span class="spinner"></span>
        <span>در حال پردازش، لطفاً صبر کنید...</span>
      </div>
      <div v-if="errorMessage" class="error-box mt-4">{{ errorMessage }}</div>
      <div v-if="successMessage" class="success-box mt-4">{{ successMessage }}</div>
    </div>
  </main>
</template>

<script setup>
import { ref, reactive } from 'vue'
import BigFive from './components/BigFive.vue'
import GSS from './components/GSS.vue'
import Behavioral from './components/Behavioral.vue'
import PersonalInfo from './components/PersonalInfo.vue'

const bigfive = ref(null)
const gss = ref(null)
const behavioral = ref(null)

const form = reactive({
  first_name: '',
  last_name: '',
  age: '',
  occupation: '',
  interests: '',
  tags: [],
  character_sentences: ''
})

const activeSection = ref(null)
const agentId = ref(null)
const isLoading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

function toggleSection(idx) {
  if (activeSection.value === idx) {
    activeSection.value = null
  } else {
    activeSection.value = idx
    setTimeout(() => {
      const section = document.querySelectorAll('.accordion-section')[idx]
      if (section) section.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }, 100)
  }
}

async function createAgent() {
  isLoading.value = true
  errorMessage.value = ''
  successMessage.value = ''
  bigfive.value?.updateBigFiveScores()
  gss.value?.generateSummary()
  behavioral.value?.generateSummary()

  const personalityTraits = [
    ...(bigfive.value?.bigFiveDescriptions || [])
  ];

  const payload = {
    ...form,
    age: Number(form.age),
    interests: form.interests.split(',').map(i => i.trim()),
    tags: form.tags,
    personality_traits: personalityTraits,
    gss_summary: gss.value?.gssSummary || [],
    behavioral_summary: behavioral.value?.behavioralSummary || [],
    character_sentences: form.character_sentences
  }

  try {
    const res = await fetch("http://127.0.0.1:8000/agents/create", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    })
    const data = await res.json()
    if (!res.ok) throw new Error("خطا در ایجاد ایجنت")
    successMessage.value = "✅ ایجنت با موفقیت ثبت شد"
    agentId.value = data.agent_id
    form.first_name = ''
    form.last_name = ''
    form.age = ''
    form.occupation = ''
    form.interests = ''
    form.tags = []
    form.character_sentences = ''
    activeSection.value = null
    bigfive.value?.$forceUpdate?.()
    gss.value?.$forceUpdate?.()
    behavioral.value?.$forceUpdate?.()
  } catch (err) {
    errorMessage.value = '❌ خطا در ثبت شخصیت'
    console.error(err)
  } finally {
    isLoading.value = false
  }
}

async function reflectAgent() {
  if (!agentId.value) return
  const res = await fetch(`http://127.0.0.1:8000/agents/${agentId.value}/reflect`, {
    method: "POST"
  })
  const data = await res.json()
  alert(data.message)
}

function refreshForm() {
  window.location.reload();
}
</script>

<style src="./style.css"></style>

<style>
/* استایل‌های اختصاصی این فایل را اینجا قرار دهید */
</style>
