<template>
  <span class="loader-spinner" :style="{ width: sizePx, height: sizePx }" role="status" aria-live="polite">
    <svg viewBox="0 0 40 40" class="spinner-svg">
      <circle class="spinner-bg" cx="20" cy="20" r="16" fill="none" stroke-width="4" />
      <circle class="spinner-fg" cx="20" cy="20" r="16" fill="none" stroke-width="4" />
    </svg>
    <span class="visually-hidden">Loading...</span>
  </span>
</template>

<script setup>
import { defineProps, computed } from 'vue'
const props = defineProps({
  size: { type: [String, Number], default: 32 },
})
const sizePx = computed(() => typeof props.size === 'number' ? `${props.size}px` : props.size)
</script>

<style lang="scss" scoped>
.loader-spinner {
  display: inline-block;
  vertical-align: middle;
  font-family: 'Inter', 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
}
.spinner-svg {
  width: 100%;
  height: 100%;
  animation: spinner-rotate 1s linear infinite;
}
.spinner-bg {
  stroke: $gray-200;
}
.spinner-fg {
  stroke: $color-primary;
  stroke-linecap: round;
  stroke-dasharray: 80;
  stroke-dashoffset: 60;
  animation: spinner-dash 1s ease-in-out infinite;
}
@keyframes spinner-rotate {
  100% { transform: rotate(360deg); }
}
@keyframes spinner-dash {
  0% { stroke-dashoffset: 80; }
  50% { stroke-dashoffset: 20; }
  100% { stroke-dashoffset: 80; }
}
.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0,0,0,0);
  border: 0;
}
</style> 