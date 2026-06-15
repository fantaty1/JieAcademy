<template>
  <div class="combo-section">
    <h3 class="section-title">
      <DifficultyTag :difficulty="difficulty" />
      <span>{{ title }}</span>
    </h3>
    <div v-if="combos.length === 0" class="empty-tip">暂无内容，敬请期待</div>
    <div v-else class="combo-list">
      <div v-for="combo in combos" :key="combo.id" class="combo-item">
        <div class="combo-header">
          <h4 class="combo-title">{{ combo.title }}</h4>
          <DifficultyTag :difficulty="combo.difficulty" />
        </div>
        <div v-if="combo.content" class="combo-content doc-body" v-html="renderMd(combo.content)"></div>
        <VideoButton
          v-if="combo.video_url"
          :url="combo.video_url"
          :title="combo.video_title || '点击查看抖音实操教学'"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import MarkdownIt from 'markdown-it'
import DifficultyTag from './DifficultyTag.vue'
import VideoButton from './VideoButton.vue'

const md = new MarkdownIt({ html: false, linkify: true })

defineProps({
  title: { type: String, required: true },
  difficulty: { type: String, default: 'normal' },
  combos: { type: Array, default: () => [] }
})

function renderMd(text) {
  return md.render(text || '')
}
</script>

<style scoped>
.combo-section {
  margin-bottom: 40px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--border-light);
  letter-spacing: 1px;
}

.empty-tip {
  color: var(--text-muted);
  font-size: 14px;
  padding: 24px 0;
  text-align: center;
  background: var(--bg-secondary);
  border-radius: 8px;
  border: 1px dashed var(--border-default);
}

.combo-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.combo-item {
  background: var(--bg-secondary);
  border: 1px solid var(--border-light);
  border-radius: 10px;
  padding: 24px;
  transition: box-shadow 0.2s;
}

.combo-item:hover {
  box-shadow: var(--shadow-sm);
}

.combo-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.combo-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.combo-content {
  font-size: 15px;
  line-height: 1.8;
}
</style>
