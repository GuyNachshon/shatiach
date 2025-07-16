<template>
  <span class="base-icon" :style="iconStyle">
    <slot v-if="!name" />
    <component v-else :is="iconComponent" />
  </span>
</template>

<script setup>
import { computed, defineProps } from 'vue'
// Import your SVG icon components here, e.g. import IconSend from './icons/IconSend.vue'
const iconMap = {
  // send: IconSend,
  // plus: IconPlus,
  // ...
}
const props = defineProps({
  name: { type: String, default: '' },
  size: { type: [String, Number], default: 24 },
  color: { type: String, default: 'currentColor' },
})
const iconComponent = computed(() => iconMap[props.name] || null)
const iconStyle = computed(() => ({
  width: typeof props.size === 'number' ? `${props.size}px` : props.size,
  height: typeof props.size === 'number' ? `${props.size}px` : props.size,
  color: `var(--icon-color, ${props.color})`,
  display: 'inline-flex',
  'vertical-align': 'middle',
}))
</script>

<style lang="scss" scoped>
.base-icon {
  line-height: 0;
  svg {
    display: inline-block;
    width: 100%;
    height: 100%;
    fill: currentColor;
  }
}
</style> 