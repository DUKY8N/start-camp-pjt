<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header class="app-header">
    <div class="container header-inner">
      <RouterLink class="logo" to="/">Home</RouterLink>

      <nav class="nav-links">
        <RouterLink to="/board">게시판</RouterLink>
        <RouterLink to="/chatbot">챗봇</RouterLink>
      </nav>
    </div>
  </header>

  <main class="container page-content">
    <RouterView />
  </main>
</template>

<style scoped>
.app-header {
  border-bottom: 1px solid #e5e7eb;
}

.header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 0;
}

.logo {
  font-size: 20px;
  font-weight: 700;
}

.nav-links {
  display: flex;
  gap: 16px;
}

.app-header a {
  color: #111827;
  text-decoration: none;
}

.app-header a.router-link-active {
  color: #42b883;
}

.page-content {
  padding: 24px 0;
}
</style>
