<template>
  <main dir="rtl" class="p-4" style="font-family: Vazirmatn, Tahoma">
    <h2 class="text-xl font-bold mb-4">ساخت شخصیت جدید</h2>

    <PersonalInfo :form="form" />

    <BigFive ref="bigfive" />
    <GSS ref="gss" />
    <Behavioral ref="behavioral" />

    <div class="mb-4 mt-6">
      <label class="font-bold block mb-2">جملات کوتاه درباره شخصیت (هر جمله در یک خط):</label>
      <textarea v-model="form.character_sentences" rows="5" class="input" placeholder="مثال: فردی اجتماعی است&#10;به مطالعه علاقه دارد&#10;..." />
    </div>

    <button @click="createAgent" class="mt-6 px-4 py-2 bg-blue-600 text-white rounded">📨 ثبت شخصیت</button>
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

async function createAgent() {
  bigfive.value?.updateBigFiveScores()
  gss.value?.generateSummary()
  behavioral.value?.generateSummary()

  const payload = {
    ...form,
    age: Number(form.age),
    interests: form.interests.split(',').map(i => i.trim()),
    tags: form.tags,
    personality_traits: [
      ...(bigfive.value?.bigFiveDescriptions || []),
      ...(gss.value?.gssSummary || []),
      ...(behavioral.value?.behavioralSummary || [])
    ],
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

    if (!res.ok) throw new Error("خطا در ایجاد ایجنت")
    alert("✅ ایجنت با موفقیت ثبت شد")
  } catch (err) {
    alert("❌ خطا در ثبت شخصیت")
    console.error(err)
  }
}
</script>

<style>
.input {
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 0.3rem 0.6rem;
  width: 100%;
}
</style>
