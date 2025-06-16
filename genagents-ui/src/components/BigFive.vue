<script setup>
import { ref, onMounted } from 'vue'

const bigFiveData = ref({})
const bigFiveAnswers = ref({})
const bigFiveScores = ref({})
const bigFiveDescriptions = ref([])

onMounted(async () => {
  const res = await fetch('/bigfive_questions.json')
  bigFiveData.value = await res.json()

  for (const dimension in bigFiveData.value) {
    bigFiveAnswers.value[dimension] = []
  }
})

function updateBigFiveScores() {
  bigFiveDescriptions.value = []
  for (const dimension in bigFiveAnswers.value) {
    const scores = bigFiveAnswers.value[dimension].filter(v => v && v !== '')
    if (scores.length === 0) continue
    const avg = scores.reduce((a, b) => a + b, 0) / scores.length
    bigFiveScores.value[dimension] = Math.round(avg)
    let description = ''
    if (avg >= 4.5) description = `او در ویژگی «${bigFiveData.value[dimension].title}» بسیار بالا است.`
    else if (avg >= 3.5) description = `او در ویژگی «${bigFiveData.value[dimension].title}» نسبتاً بالا است.`
    else if (avg >= 2.5) description = `او در ویژگی «${bigFiveData.value[dimension].title}» در حد متوسط قرار دارد.`
    else if (avg >= 1.5) description = `او در ویژگی «${bigFiveData.value[dimension].title}» نسبتاً پایین است.`
    else description = `او در ویژگی «${bigFiveData.value[dimension].title}» بسیار پایین است.`

    bigFiveDescriptions.value.push(description)
  }
}

defineExpose({
  bigFiveScores,
  bigFiveDescriptions,
  updateBigFiveScores
})
</script>

<template>
  <div dir="rtl" class="p-4 mt-6" style="font-family: Vazirmatn, Tahoma">
    <h2 class="text-lg font-bold mb-4">🧠 پرسشنامه شخصیت (Big Five)</h2>

    <div v-for="(item, key) in bigFiveData" :key="key" class="mb-6">
      <h3 class="font-semibold mb-2">{{ item.title }}</h3>
      <div v-for="(question, idx) in item.questions" :key="idx" class="mb-2">
        <label>{{ question }}</label><br />
        <div class="flex gap-4 mt-1">
          <label v-for="i in 5" :key="i" class="inline-flex items-center">
            <input type="radio" :name="`${key}-${idx}`" :value="i" v-model="bigFiveAnswers[key][idx]" />
            <span class="ml-1">{{ i }}</span>
          </label>
        </div>
      </div>
    </div>

    <button @click="updateBigFiveScores" class="mt-4">📊 مشاهده نتایج و خلاصه</button>

    <div v-if="bigFiveDescriptions.length" class="mt-6">
      <h4 class="font-bold">📝 خلاصه شخصیت شما:</h4>
      <ul>
        <li v-for="d in bigFiveDescriptions" :key="d">✔️ {{ d }}</li>
      </ul>
    </div>
  </div>
</template>
