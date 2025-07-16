<template>
  <div :class="['base-card', { shadow, padded }]" v-bind="$attrs">
    <slot />
  </div>
</template>

<script setup>
import { defineProps } from 'vue'
const props = defineProps({
  shadow: { type: Boolean, default: true },
  padded: { type: Boolean, default: true },
})
</script>

<style lang="scss" scoped>
.base-card {
  background: $background-default;
  border-radius: $radius-lg;
  border: 1px solid $gray-200;
  font-family: 'Inter', 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
  direction: rtl;
  &.shadow {
    box-shadow: $shadow-md;
  }
  &.padded {
    padding: 1.5rem 2rem;
  }
}
</style> 