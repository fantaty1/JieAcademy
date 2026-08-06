<template>
  <a
    v-if="url"
    :href="url"
    target="_blank"
    rel="noopener noreferrer"
    class="video-button"
  >
    <svg class="play-icon" viewBox="0 0 24 24" fill="currentColor" width="16" height="16">
      <path d="M8 5v14l11-7z"/>
    </svg>
    <span>{{ title }}</span>
  </a>
</template>

<script setup>
defineProps({
  url: { type: String, default: '' },
  title: { type: String, default: '点击查看抖音实操教学' }
})
</script>

<style scoped>
.video-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 24px;
  background: var(--bg-secondary);
  color: var(--accent-gold);
  border: 1px solid var(--accent-gold);
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.25s;
  margin-top: 16px;
}

.video-button:hover {
  background: var(--accent-gold);
  color: #fff;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(184, 134, 11, 0.2);
}

.play-icon {
  width: 16px;
  height: 16px;
}
</style>
