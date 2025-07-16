<template>
  <span :class="['tag-chip', color]" v-bind="$attrs">
    <slot />
  </span>
</template>

<script setup>
import { defineProps } from 'vue'
const props = defineProps({
  color: { type: String, default: 'default' }, // default | success | warning | danger | info
})
</script>

<style lang="scss" scoped>
.tag-chip {
  display: inline-block;
  padding: 0.15em 0.75em;
  border-radius: $radius-full;
  font-size: 0.85rem;
  font-weight: 500;
  font-family: 'Inter', 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
  background: $gray-100;
  color: $gray-700;
  border: 1px solid $gray-200;
  vertical-align: middle;
  line-height: 1.6;
  &.success {
    background: $color-success;
    color: $text-inverse;
    border: none;
  }
  &.warning {
    background: $color-warning;
    color: $gray-900;
    border: none;
  }
  &.danger {
    background: $color-danger;
    color: $text-inverse;
    border: none;
  }
  &.info {
    background: $color-info;
    color: $text-inverse;
    border: none;
  }
}
</style> 