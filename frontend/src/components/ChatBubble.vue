<template>
  <div :class="['chat-bubble', sender]">
    <div v-if="avatar" class="chat-bubble-avatar">
      <img :src="avatar" alt="avatar" />
    </div>
    <div class="chat-bubble-content">
      <div class="chat-bubble-message">
        <slot />
      </div>
      <div v-if="time" class="chat-bubble-time">
        <TagChip color="info">{{ time }}</TagChip>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'
import TagChip from './TagChip.vue'
const props = defineProps({
  sender: { type: String, default: 'user' }, // 'user' | 'system' | 'other'
  avatar: { type: String, default: '' },
  time: { type: String, default: '' },
})
</script>

<style lang="scss" scoped>
.chat-bubble {
  display: flex;
  align-items: flex-end;
  margin-bottom: 1.2rem;
  font-family: 'Inter', 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
  &.user {
    flex-direction: row-reverse;
    .chat-bubble-content {
      background: $color-primary;
      color: $text-inverse;
      border-top-left-radius: $radius-lg;
      border-top-right-radius: $radius-lg;
      border-bottom-left-radius: $radius-lg;
      border-bottom-right-radius: $radius-md;
      align-items: flex-end;
    }
  }
  &.system {
    .chat-bubble-content {
      background: $gray-200;
      color: $gray-900;
      border-radius: $radius-lg;
      align-items: flex-start;
    }
  }
  &.other {
    .chat-bubble-content {
      background: $background-muted;
      color: $gray-900;
      border-radius: $radius-lg;
      align-items: flex-start;
    }
  }
}
.chat-bubble-avatar {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: $radius-full;
  overflow: hidden;
  margin: 0 0.75rem;
  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }
}
.chat-bubble-content {
  max-width: 60vw;
  padding: 0.75rem 1.25rem;
  display: flex;
  flex-direction: column;
  box-shadow: $shadow-xs;
  font-size: 1rem;
  word-break: break-word;
}
.chat-bubble-message {
  margin-bottom: 0.3rem;
}
.chat-bubble-time {
  font-size: 0.75rem;
  margin-top: 0.1rem;
  align-self: flex-end;
}
</style> 