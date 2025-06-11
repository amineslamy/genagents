<template>
  <div dir="rtl" class="p-4 mt-6" style="font-family: Vazirmatn, Tahoma">
    <h2 class="text-lg font-bold mb-4">💰 پرسشنامه اقتصاد رفتاری</h2>

    <div v-for="(question, index) in behavioralQuestions" :key="index" class="mb-4">
      <p class="mb-1">{{ index + 1 }}. {{ question }}</p>
      <div class="flex flex-wrap gap-4">
        <label v-for="i in 5" :key="i">
          <input type="radio" :name="`bq${index}`" :value="i" v-model="answers[index]" />
          {{ likertLabels[i - 1] }}
        </label>
      </div>
    </div>

    <button @click="generateSummary" class="mt-4 px-4 py-2 bg-green-600 text-white rounded">📊 مشاهده تحلیل</button>

    <div v-if="behavioralSummary.length" class="mt-6">
      <h4 class="font-bold">📝 خلاصه رفتار اقتصادی:</h4>
      <ul>
        <li v-for="s in behavioralSummary" :key="s">✔️ {{ s }}</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const behavioralQuestions = ref([])
const thirdPersonRewrites = ref([])
const answers = ref([])
const behavioralSummary = ref([])

const likertLabels = ['کاملاً مخالفم', 'مخالفم', 'بی‌نظر', 'موافقم', 'کاملاً موافقم']

onMounted(async () => {
  const res = await fetch('/behavioral_questions.json')
  const data = await res.json()
  behavioralQuestions.value = data.behavioral.questions
  answers.value = Array(behavioralQuestions.value.length).fill('')

  // تبدیل جملات به سوم‌شخص برای خلاصه
  thirdPersonRewrites.value = behavioralQuestions.value.map((q, i) => {
    return convertToThirdPerson(q)
  })
})

function convertToThirdPerson(sentence) {
  // جایگزینی ساده برای "می‌دهم"، "می‌کنم"، "دارم" و ...
  return sentence
    .replace('می‌دهم', 'می‌دهد')
    .replace('می‌کنم', 'می‌کند')
    .replace('دارم', 'دارد')
    .replace('می‌گیرم', 'می‌گیرد')
    .replace('هستم', 'است')
    .replace('می‌خواهم', 'می‌خواهد')
    .replace('ترجیح می‌دهم', 'ترجیح می‌دهد')
    .replace('می‌اندیشم', 'می‌اندیشد')
    .replace('می‌توانم', 'می‌تواند')
    .replace('می‌خرم', 'می‌خرد')
    .replace('می‌اندازم', 'می‌اندازد')
    .replace('می‌گذارم', 'می‌گذارد')
    .replace('دارم', 'دارد')
    .replace('پرهیز می‌کنم', 'پرهیز می‌کند')
    .replace('سعی می‌کنم', 'سعی می‌کند')
    .replace('خرج می‌کنم', 'خرج می‌کند')
}

function generateSummary() {
  behavioralSummary.value = []

  for (let i = 0; i < behavioralQuestions.value.length; i++) {
    const score = parseInt(answers.value[i])
    const q = thirdPersonRewrites.value[i]

    if (isNaN(score)) {
      behavioralSummary.value = []
      alert('لطفاً به تمام سوالات اقتصاد رفتاری پاسخ دهید.')
      return
    }

    let prefix = ''
    if (score === 5) prefix = 'او کاملاً موافق است که'
    else if (score === 4) prefix = 'او موافق است که'
    else if (score === 3) prefix = 'او نسبت به این نظر بی‌تفاوت است که'
    else if (score === 2) prefix = 'او مخالف است که'
    else prefix = 'او کاملاً مخالف است که'

    behavioralSummary.value.push(`${prefix} ${q}`)
  }
}

// خروجی در اختیار parent
defineExpose({
  behavioralSummary,
  generateSummary
})
</script>

<style scoped>
label {
  display: inline-block;
  cursor: pointer;
}
</style>
