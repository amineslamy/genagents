<template>
  <main class="dashboard-container" dir="rtl">
    <h1 class="dashboard-title">داشبورد اصلی GenAgents</h1>
    <div class="dashboard-links">
      <router-link to="/create-character" class="dashboard-link active">ساخت شخصیت جدید</router-link>
      <router-link to="/agents" class="dashboard-link">لیست شخصیت‌ها</router-link>
      <span class="dashboard-link disabled">محیط‌ها (به‌زودی)</span>
      <span class="dashboard-link disabled">چت با شخصیت (به‌زودی)</span>
    </div>
    <div class="dashboard-content">
      <!-- اینجا محتوای هر بخش نمایش داده می‌شود -->
    </div>
  </main>
</template>

<script>
export default {
  name: 'Dashboard',
}
</script>

<style scoped>
.dashboard-container {
  max-width: 600px;
  margin: 2rem auto;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 8px #0001;
  padding: 2rem;
  text-align: center;
}
.dashboard-title {
  font-size: 2rem;
  margin-bottom: 2rem;
}
.dashboard-links {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 2rem;
}
.dashboard-link {
  display: inline-block;
  padding: 0.7rem 1.5rem;
  border-radius: 6px;
  font-size: 1.1rem;
  background: #f3f3f3;
  color: #333;
  text-decoration: none;
  transition: background 0.2s;
}
.dashboard-link.active {
  background: #42b983;
  color: #fff;
  font-weight: bold;
}
.dashboard-link.disabled {
  background: #eee;
  color: #aaa;
  cursor: not-allowed;
}
</style>
