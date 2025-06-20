<template>
  <!-- این فایل به عنوان shell اصلی پروژه برای داشبورد و SPA استفاده خواهد شد -->
  <header class="main-header">
    <router-link to="/" class="dashboard-link">🏠 بازگشت به داشبورد GenAgents</router-link>
  </header>
  <router-view />
</template>

<script setup>
// فقط روتینگ و شل اصلی پروژه
</script>

<style src="./style.css"></style>

<style>
.main-header {
  width: 100%;
  background: #1976d2;
  padding: 1em 0;
  text-align: center;
  margin-bottom: 2em;
}
.dashboard-link {
  color: #fff;
  font-size: 1.1em;
  font-weight: bold;
  text-decoration: none;
  transition: color 0.2s;
}
.dashboard-link:hover {
  color: #bbdefb;
}
</style>
