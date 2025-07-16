<script setup>
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <div class="app-layout">
    <header class="app-header">
      <h1>Shatiach</h1>
    </header>
    <main class="app-main">
      <router-view />
    </main>
  </div>
</template>

<style lang="scss">
@use './assets/variables.scss' as *;
.app-layout {
  min-height: 100vh;
  direction: rtl;
  font-family: 'Inter', 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
  background: $background-default;
  color: $text-default;
  display: flex;
  flex-direction: column;
}
.app-header {
  padding: 1.5rem 2rem 1rem 2rem;
  background: $background-muted;
  border-bottom: 1px solid $gray-200;
  font-size: 1.5rem;
  font-weight: 700;
  letter-spacing: 0.02em;
}
.app-main {
  flex: 1;
  padding: 2rem;
  display: flex;
  flex-direction: column;
}
</style>
