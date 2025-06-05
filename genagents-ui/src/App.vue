<template>
  <main dir="rtl" style="font-family: Vazirmatn, Tahoma; max-width: 800px; margin: auto; padding: 2rem;">
    <h1 style="font-size: 1.5rem; font-weight: bold; margin-bottom: 1rem;">🧠 ساخت شخصیت جدید</h1>

    <!-- فرم اطلاعات پایه -->
    <form @submit.prevent="createAgent" style="display: grid; gap: 0.75rem;">
      <input v-model="form.first_name" placeholder="نام" required />
      <input v-model="form.last_name" placeholder="نام خانوادگی" required />
      <input v-model="form.age" placeholder="سن" type="number" required />
      <input v-model="form.occupation" placeholder="شغل" />
      <input v-model="form.interests" placeholder="علایق (با کاما جدا کنید)" />
    </form>

    <!-- بخش انتخاب تگ‌ها -->
    <h2 style="margin-top: 2rem;">🏷️ انتخاب برچسب‌ها (تگ‌ها)</h2>
    <div v-for="(options, category) in tags" :key="category" style="margin-top: 1rem;">
      <h3 style="font-weight: bold;">{{ getCategoryLabel(category) }}</h3>
      <div style="display: flex; flex-wrap: wrap; gap: 1rem;">
        <label v-for="tag in options" :key="tag">
          <input type="checkbox" :value="tag" v-model="selectedTags[category]" />
          {{ tag }}
        </label>
      </div>
    </div>

    <!-- تگ سفارشی -->
    <div style="margin-top: 1rem;">
      <input v-model="customTag" placeholder="تگ دلخواه را وارد کنید..." />
      <button @click="addCustomTag" style="margin-right: 0.5rem;">➕ افزودن تگ دلخواه</button>
    </div>

    <!-- نمایش تگ‌های انتخاب‌شده -->
    <div v-if="allSelectedTags.length" style="margin-top: 1rem;">
      <strong>تگ‌های انتخاب‌شده:</strong>
      <span v-for="t in allSelectedTags" :key="t" style="margin-left: 0.5rem;">{{ t }}</span>
    </div>

    <button @click="createAgent" style="margin-top: 2rem; padding: 0.5rem 1rem;">📨 ثبت شخصیت</button>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const form = ref({
  first_name: '',
  last_name: '',
  age: '',
  occupation: '',
  interests: ''
})

const tags = ref({})
const selectedTags = ref({})
const customTag = ref('')
const allSelectedTags = ref([])

onMounted(async () => {
  const res = await fetch('/tags.json')
  tags.value = await res.json()

  for (const category in tags.value) {
    selectedTags.value[category] = []
  }
})

function addCustomTag() {
  if (customTag.value.trim()) {
    selectedTags.value.custom_tags.push(customTag.value.trim())
    customTag.value = ''
  }
  collectTags()
}

function collectTags() {
  allSelectedTags.value = Object.values(selectedTags.value).flat()
}

function getCategoryLabel(key) {
  const labels = {
    religion: "گرایش دینی",
    religiosity: "سبک دینداری",
    politics: "گرایش سیاسی",
    social: "ویژگی اجتماعی",
    economic_class: "طبقه اقتصادی",
    living_area: "محل زندگی",
    personal: "ویژگی‌های شخصی",
    custom_tags: "تگ‌های دلخواه"
  }
  return labels[key] || key
}

async function createAgent() {
  collectTags()

  const payload = {
    ...form.value,
    age: Number(form.value.age),
    interests: form.value.interests.split(',').map(i => i.trim()),
    tags: allSelectedTags.value
  }

  const res = await fetch('http://127.0.0.1:8000/agents/create', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })

  if (res.ok) {
    alert('✅ شخصیت با موفقیت ساخته شد!')
    form.value = { first_name: '', last_name: '', age: '', occupation: '', interests: '' }
    allSelectedTags.value = []
  } else {
    alert('❌ خطا در ثبت شخصیت')
  }
}
</script>
