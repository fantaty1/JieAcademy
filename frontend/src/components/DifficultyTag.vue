<template>
  <span class="difficulty-tag" :class="difficulty">
    {{ label }}
  </span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  difficulty: { type: String, default: 'normal' }
})

const label = computed(() => {
  const map = { normal: '基础', advanced: '进阶', hard: '绝活' }
  return map[props.difficulty] || props.difficulty
})
</script>

<style scoped>
.difficulty-tag {
  display: inline-block;
  padding: 3px 12px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
  letter-spacing: 1px;
}

.difficulty-tag.normal {
  background: rgba(39, 174, 96, 0.1);
  color: var(--diff-normal);
  border: 1px solid rgba(39, 174, 96, 0.2);
}

.difficulty-tag.advanced {
  background: rgba(230, 126, 34, 0.1);
  color: var(--diff-advanced);
  border: 1px solid rgba(230, 126, 34, 0.2);
}

.difficulty-tag.hard {
  background: rgba(192, 57, 43, 0.1);
  color: var(--diff-hard);
  border: 1px solid rgba(192, 57, 43, 0.2);
}
</style>
