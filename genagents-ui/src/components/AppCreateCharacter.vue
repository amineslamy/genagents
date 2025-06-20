<template>
  <main dir="rtl" class="p-4" style="font-family: Vazirmatn, Tahoma">
    <h2 class="text-xl font-bold mb-4">ساخت شخصیت جدید</h2>

    <div class="mb-4">
      <label>نام:</label>
      <input v-model="form.first_name" class="input" type="text" />
    </div>
    <div class="mb-4">
      <label>نام خانوادگی:</label>
      <input v-model="form.last_name" class="input" type="text" />
    </div>
    <div class="mb-4">
      <label>سن:</label>
      <input v-model="form.age" class="input" type="number" />
    </div>
    <div class="mb-4">
      <label>شغل:</label>
      <input v-model="form.occupation" class="input" type="text" />
    </div>
    <div class="mb-4">
      <label>علاقه‌مندی‌ها (با ویرگول جدا کنید):</label>
      <input v-model="form.interests" class="input" type="text" />
    </div>

    <h3 class="font-bold mt-6 mb-2">🏷️ تگ‌های شخصیت</h3>
    <div v-for="(group, groupName) in tagGroups" :key="groupName" class="mb-4">
      <label class="font-semibold">{{ groupName }}:</label>
      <div class="flex flex-wrap gap-2 mt-1">
        <label v-for="tag in group" :key="tag">
          <input type="checkbox" :value="tag" v-model="selectedTags[groupName]" />
          {{ tag }}
        </label>
      </div>
    </div>

    <BigFive ref="bigfive" />
    <GSS ref="gss" />
    <Behavioral ref="behavioral" />

    <button @click="createAgent" :disabled="isLoading" class="mt-6 px-4 py-2 bg-blue-600 text-white rounded">
      <span v-if="isLoading" class="spinner"></span>
      <span v-if="!isLoading">📨 ثبت شخصیت</span>
      <span v-else>در حال ثبت...</span>
    </button>
    <div v-if="isLoading" class="loading-box mt-4">
      <span class="spinner"></span>
      <span>در حال پردازش، لطفاً صبر کنید...</span>
    </div>
    <div v-if="errorMessage" class="error-box mt-4">{{ errorMessage }}</div>
    <div v-if="successMessage" class="success-box mt-4">{{ successMessage }}</div>
  </main>
</template>

<script setup>
import { ref, reactive } from 'vue'
import BigFive from './BigFive.vue'
import GSS from './GSS.vue'
import Behavioral from './Behavioral.vue'

const bigfive = ref(null)
const gss = ref(null)
const behavioral = ref(null)

const form = reactive({
  first_name: '',
  last_name: '',
  age: '',
  occupation: '',
  interests: ''
})

const tagGroups = {
  مذهبی: ['شیعه', 'سنی', 'بی‌تفاوت مذهبی', 'پایبند به مناسک', 'مذهبی انعطاف‌پذیر', 'رادیکال', 'ضد دین'],
  سیاسی: ['اصولگرا', 'اصلاح‌طلب', 'انقلابی', 'منتقد نظام', 'بی‌تفاوت سیاسی', 'طرفدار نظام', 'مستقل'],
  اجتماعی: ['فردگرا', 'جمع‌گرا', 'خانواده‌محور', 'فعال اجتماعی', 'بی‌تفاوت'],
  اقتصادی: ['دهک 1–3', 'دهک 4–6', 'دهک 7–10', 'شهرهای بزرگ', 'شهرهای کوچک', 'روستا'],
  شخصی: ['مرد', 'زن', 'مجرد', 'متأهل', 'تحصیلات کم', 'تحصیلات متوسط', 'تحصیلات عالی'],
  سفارشی: []
}

const selectedTags = reactive({})
for (const key in tagGroups) selectedTags[key] = []

function collectTags() {
  allSelectedTags.value = Object.values(selectedTags).flat()
}

const allSelectedTags = ref([])
const isLoading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

async function createAgent() {
  collectTags()
  bigfive.value?.updateBigFiveScores()
  gss.value?.generateSummary()
  behavioral.value?.generateSummary()
  isLoading.value = true
  errorMessage.value = ''
  successMessage.value = ''
  const payload = {
    ...form,
    age: Number(form.age),
    interests: form.interests.split(',').map(i => i.trim()),
    tags: allSelectedTags.value,
    personality_traits: [
      ...(bigfive.value?.bigFiveDescriptions || []),
      ...(gss.value?.gssSummary || []),
      ...(behavioral.value?.behavioralSummary || [])
    ],
    gss_summary: gss.value?.gssSummary || [],
    behavioral_summary: behavioral.value?.behavioralSummary || []
  }
  try {
    const res = await fetch("/agents/create", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    })
    if (!res.ok) throw new Error("خطا در ایجاد ایجنت")
    successMessage.value = "✅ ایجنت با موفقیت ثبت شد"
  } catch (err) {
    errorMessage.value = "❌ خطا در ثبت شخصیت"
    console.error(err)
  } finally {
    isLoading.value = false
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
.spinner {
  border: 2px solid #f3f3f3;
  border-top: 2px solid #42b983;
  border-radius: 50%;
  width: 16px;
  height: 16px;
  display: inline-block;
  margin-left: 8px;
  animation: spin 1s linear infinite;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
.loading-box {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #f3f3f3;
  border-radius: 6px;
  padding: 0.7rem 1.2rem;
  margin-top: 1rem;
}
.success-box {
  background: #e6ffed;
  color: #1a7f37;
  border: 1px solid #42b983;
  border-radius: 6px;
  padding: 0.7rem 1.2rem;
  margin-top: 1rem;
}
.error-box {
  background: #ffeaea;
  color: #b71c1c;
  border: 1px solid #e57373;
  border-radius: 6px;
  padding: 0.7rem 1.2rem;
  margin-top: 1rem;
}
</style>
