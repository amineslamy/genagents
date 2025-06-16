<template>
  <div dir="rtl" class="p-4 mt-6" style="font-family: Vazirmatn, Tahoma">
    <h2 class="text-lg font-bold mb-4">📋 پرسشنامه اجتماعی سیاسی (GSS)</h2>

    <div v-for="(question, index) in gssQuestions" :key="index" class="mb-4">
      <p class="mb-1">{{ index + 1 }}. {{ question }}</p>
      <div class="flex flex-wrap gap-4">
        <label v-for="i in 5" :key="i">
          <input type="radio" :name="`q${index}`" :value="i" v-model="answers[index]" />
          {{ likertLabels[i - 1] }}
        </label>
      </div>
    </div>

    <button @click="generateSummary" class="mt-4 px-4 py-2 bg-green-600 text-white rounded">📊 مشاهده تحلیل</button>

    <div v-if="gssSummary.length" class="mt-6">
      <h4 class="font-bold">📝 خلاصه دیدگاه‌ها:</h4>
      <ul>
        <li v-for="s in gssSummary" :key="s">✔️ {{ s }}</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const gssQuestions = ref([])
const answers = ref([])
const gssSummary = ref([])

const likertLabels = ['کاملاً مخالفم', 'مخالفم', 'بی‌نظر', 'موافقم', 'کاملاً موافقم']

onMounted(async () => {
  const res = await fetch('/gss_questions.json')
  const data = await res.json()
  gssQuestions.value = data.gss.questions
  answers.value = Array(gssQuestions.value.length).fill('')
})

function generateSummary() {
  gssSummary.value = []
  for (let i = 0; i < gssQuestions.value.length; i++) {
    const score = parseInt(answers.value[i])
    const q = gssQuestions.value[i]

    if (isNaN(score)) continue

    let prefix = ''
    if (score === 5) prefix = 'کاملاً موافق است که'
    else if (score === 4) prefix = 'موافق است که'
    else if (score === 3) prefix = 'نسبت به این نظر بی‌تفاوت است که'
    else if (score === 2) prefix = 'مخالف است که'
    else prefix = 'کاملاً مخالف است که'

    gssSummary.value.push(`او ${prefix} ${q}`)
  }
}

// خروجی در اختیار parent
defineExpose({
  gssSummary,
  generateSummary
})
</script>

<style scoped>
label {
  display: inline-block;
  cursor: pointer;
}
</style>
