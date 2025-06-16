<script setup>
import { ref, watch } from 'vue'
const props = defineProps({ form: Object });
const emit = defineEmits(['update:form']);

const tagGroups = {
  مذهبی: ['شیعه', 'سنی', 'بی‌تفاوت مذهبی', 'پایبند به مناسک', 'مذهبی انعطاف‌پذیر', 'رادییکال', 'ضد دین'],
  سیاسی: ['اصولگرا', 'اصلاح‌طلب', 'انقلابی', 'منتقد نظام', 'بی‌تفاوت سیاسی', 'طرفدار نظام', 'مستقل'],
  اجتماعی: ['فردگرا', 'جمع‌گرا', 'خانواده‌محور', 'فعال اجتماعی', 'بی‌تفاوت'],
  اقتصادی: ['دهک 1–3', 'دهک 4–6', 'دهک 7–10', 'شهرهای بزرگ', 'شهرهای کوچک', 'روستا'],
  شخصی: ['مرد', 'زن', 'مجرد', 'متأهل', 'تحصیلات کم', 'تحصیلات متوسط', 'تحصیلات عالی'],
  سفارشی: []
}

// مدیریت انتخاب تگ‌ها به صورت آرایه
const selectedTags = ref([])

// همگام‌سازی selectedTags با props.form.tags
watch(selectedTags, (val) => {
  props.form.tags = val
})

// اگر props.form.tags مقدار داشت، selectedTags را مقداردهی کن
watch(() => props.form.tags, (val) => {
  if (Array.isArray(val)) selectedTags.value = val
  else if (typeof val === 'string') selectedTags.value = val.split(',').map(t => t.trim()).filter(Boolean)
})
</script>

<template>
  <div>
    <h2>📝 اطلاعـات فردی</h2>

    <input
      v-model="props.form.first_name"
      placeholder="نام"
    /><br/>

    <input
      v-model="props.form.last_name"
      placeholder="نام خانوادگی"
    /><br/>

    <input
      v-model.number="props.form.age"
      placeholder="سن"
      type="number"
    /><br/>

    <input
      v-model="props.form.occupation"
      placeholder="شغل"
    /><br/>

    <input
      v-model="props.form.interests"
      placeholder='علایق ( با کاما جدا کنید )'
    /><br/>

    <div v-for="(group, groupName) in tagGroups" :key="groupName" class="mb-4">
      <span class="personalinfo-group-label">{{ groupName }}:</span>
      <div class="flex flex-wrap gap-2 mt-1">
        <label v-for="tag in group" :key="tag">
          <input type="checkbox" :value="tag" v-model="selectedTags" />
          {{ tag }}
        </label>
      </div>
    </div>

  </div>
</template>

<style scoped>
input {
  padding: 0.5rem;
  margin-bottom: 0.5rem;
}
</style>
