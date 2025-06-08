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

    <button @click="createAgent" class="mt-6 px-4 py-2 bg-blue-600 text-white rounded">📨 ثبت شخصیت</button>
  </main>
</template>

<script setup>
import { ref, reactive } from 'vue'
import BigFive from './components/BigFive.vue'
import GSS from './components/GSS.vue'

const bigfive = ref(null)
const gss = ref(null)

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

async function createAgent() {
  collectTags()
  bigfive.value?.updateBigFiveScores()
  gss.value?.generateSummary()

  const payload = {
    ...form,
    age: Number(form.age),
    interests: form.interests.split(',').map(i => i.trim()),
    tags: allSelectedTags.value,
    personality_traits: [
      ...(bigfive.value?.bigFiveDescriptions || []),
      ...(gss.value?.gssSummary || [])
    ]
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
