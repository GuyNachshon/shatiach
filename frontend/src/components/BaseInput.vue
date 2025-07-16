<template>
  <div class="base-input-wrapper" :class="{ error, disabled }">
    <span v-if="icon && iconPosition === 'left'" class="input-icon left">
      <BaseIcon :name="icon" :size="20" />
    </span>
    <input
      :type="type"
      :placeholder="placeholder"
      :disabled="disabled"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      class="base-input"
      :aria-invalid="error ? 'true' : 'false'"
      v-bind="$attrs"
    />
    <span v-if="icon && iconPosition === 'right'" class="input-icon right">
      <BaseIcon :name="icon" :size="20" />
    </span>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'
import BaseIcon from './BaseIcon.vue'
const emit = defineEmits(['update:modelValue'])
const props = defineProps({
  modelValue: { type: String, default: '' },
  placeholder: { type: String, default: '' },
  type: { type: String, default: 'text' },
  disabled: { type: Boolean, default: false },
  error: { type: Boolean, default: false },
  icon: { type: String, default: '' },
  iconPosition: { type: String, default: 'left' }, // 'left' | 'right'
})
</script>

<style lang="scss" scoped>
.base-input-wrapper {
  display: flex;
  align-items: center;
  position: relative;
  font-family: 'Inter', 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
  direction: rtl;
  &.error .base-input {
    border-color: $color-danger;
    box-shadow: 0 0 0 2px rgba($color-danger, 0.1);
  }
  &.disabled .base-input {
    background: $gray-100;
    color: $gray-400;
    cursor: not-allowed;
  }
}
.base-input {
  flex: 1;
  padding: 0.5rem 1rem;
  border: 1px solid $gray-300;
  border-radius: $radius-md;
  font-size: 1rem;
  background: $background-default;
  color: $text-default;
  outline: none;
  transition: border 0.15s, box-shadow 0.15s;
  font-family: inherit;
  &:focus {
    border-color: $color-primary;
    box-shadow: 0 0 0 2px rgba($color-primary, 0.12);
  }
  &::placeholder {
    color: $gray-400;
    opacity: 1;
  }
}
.input-icon {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  color: $gray-400;
  &.left {
    right: 1rem;
  }
  &.right {
    left: 1rem;
  }
}
</style> 