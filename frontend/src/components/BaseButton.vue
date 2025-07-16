<template>
  <button
    :class="['base-btn', variant, { disabled }]"
    :type="type"
    :disabled="disabled"
    v-bind="$attrs"
  >
    <slot />
  </button>
</template>

<script setup>
import { defineProps } from 'vue'
const props = defineProps({
  type: { type: String, default: 'button' },
  variant: { type: String, default: 'primary' }, // 'primary' | 'secondary' | 'icon'
  disabled: { type: Boolean, default: false },
})
</script>

<style lang="scss" scoped>
.base-btn {
  font-family: 'Inter', 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
  border: none;
  outline: none;
  cursor: pointer;
  padding: 0.5rem 1.5rem;
  border-radius: $radius-md;
  font-size: 1rem;
  font-weight: 600;
  transition: background 0.15s, color 0.15s, box-shadow 0.15s;
  box-shadow: $shadow-xs;
  background: $color-primary;
  color: $text-inverse;
  &:hover:not(.disabled) {
    background: $color-primary-dark;
  }
  &.disabled {
    opacity: 0.6;
    cursor: not-allowed;
    pointer-events: none;
  }
  &.secondary {
    background: $background-muted;
    color: $color-primary;
    border: 1px solid $color-primary;
    &:hover:not(.disabled) {
      background: $color-primary;
      color: $text-inverse;
    }
  }
  &.icon {
    padding: 0.5rem;
    width: 2.5rem;
    height: 2.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    background: transparent;
    color: $color-primary;
    border: none;
    box-shadow: none;
    &:hover:not(.disabled) {
      background: $background-muted;
    }
  }
}
</style> 