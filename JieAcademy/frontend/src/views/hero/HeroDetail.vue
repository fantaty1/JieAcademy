<template>
  <div class="hero-detail" v-if="hero">
    <SideBar :title="hero.name" :sections="sidebarSections" />

    <main class="detail-main">
      <article class="article">
        <!-- 英雄头 -->
        <header class="article-header">
          <div class="hero-badge">
            <div class="hero-avatar" v-if="hero.avatar">
              <img :src="hero.avatar" :alt="hero.name" />
            </div>
            <div class="hero-avatar placeholder" v-else>{{ hero.name[0] }}</div>
            <div>
              <h1 class="hero-name">{{ hero.name }}</h1>
              <div class="hero-meta">
                <span class="difficulty-label">上手难度</span>
                <span v-for="i in 5" :key="i" class="star" :class="{ active: i <= hero.difficulty }">
                  {{ i <= hero.difficulty ? '★' : '☆' }}
                </span>
              </div>
            </div>
          </div>
        </header>

        <!-- 英雄简介 -->
        <section id="intro" class="doc-section">
          <h2>英雄简介</h2>
          <div v-if="hero.description" class="doc-body" v-html="renderMd(hero.description)"></div>
          <div v-else class="empty-content">暂无简介</div>
        </section>

        <!-- 技能说明 -->
        <section id="skills" class="doc-section">
          <h2>技能说明</h2>
          <div v-if="hero.skills_desc" class="doc-body" v-html="renderMd(hero.skills_desc)"></div>
          <div v-else class="empty-content">暂无内容</div>
        </section>

        <!-- 推荐连招 -->
        <section id="combos" class="doc-section">
          <h2>推荐连招</h2>
          <ComboSection title="基础连招" difficulty="normal" :combos="normalCombos" />
          <ComboSection title="进阶连招" difficulty="advanced" :combos="advancedCombos" />
          <ComboSection title="绝活连招" difficulty="hard" :combos="hardCombos" />
        </section>

        <!-- 应对方式 -->
        <section id="matchups" class="doc-section">
          <h2>英雄应对</h2>
          <div v-if="matchups.length === 0" class="empty-content">暂无内容，敬请期待</div>
          <div v-else class="matchup-list">
            <div v-for="m in matchups" :key="m.id" class="matchup-item">
              <div class="matchup-header">
                <span class="matchup-vs">vs {{ m.opponent_name }}</span>
                <span class="matchup-type" :class="m.matchup_type">{{ matchupLabel(m.matchup_type) }}</span>
              </div>
              <div v-if="m.tips" class="doc-body" v-html="renderMd(m.tips)"></div>
              <VideoButton v-if="m.video_url" :url="m.video_url" />
            </div>
          </div>
        </section>
      </article>
    </main>
  </div>

  <div v-else-if="loading" class="loading-wrapper">
    <el-skeleton :rows="12" animated />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import MarkdownIt from 'markdown-it'
import { getHero, getHeroCombos, getHeroMatchups } from '@/api/heroes'
import SideBar from '@/components/layout/SideBar.vue'
import ComboSection from '@/components/ComboSection.vue'
import VideoButton from '@/components/VideoButton.vue'

const md = new MarkdownIt({ html: false, linkify: true })
const route = useRoute()

const hero = ref(null)
const combos = ref([])
const matchups = ref([])
const loading = ref(true)

const sidebarSections = [
  { id: 'intro', label: '英雄简介' },
  { id: 'skills', label: '技能说明' },
  { id: 'combos', label: '推荐连招' },
  { id: 'matchups', label: '英雄应对' },
]

const normalCombos = computed(() => combos.value.filter(c => c.difficulty === 'normal'))
const advancedCombos = computed(() => combos.value.filter(c => c.difficulty === 'advanced'))
const hardCombos = computed(() => combos.value.filter(c => c.difficulty === 'hard'))

function renderMd(text) {
  return md.render(text || '')
}

function matchupLabel(type) {
  const map = { easy: '简单', even: '均势', hard: '困难' }
  return map[type] || type
}

onMounted(async () => {
  const id = route.params.id
  try {
    const [hRes, cRes, mRes] = await Promise.all([
      getHero(id),
      getHeroCombos(id),
      getHeroMatchups(id)
    ])
    hero.value = hRes
    combos.value = cRes.results || cRes
    matchups.value = mRes.results || mRes
  } catch (e) {
    console.error('加载英雄详情失败', e)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.hero-detail {
  display: flex;
  max-width: 1400px;
  margin: 0 auto;
}

.detail-main {
  flex: 1;
  min-width: 0;
}

.article {
  max-width: 860px;
  margin: 0 auto;
  padding: 40px 48px 80px;
}

.article-header {
  margin-bottom: 40px;
  padding-bottom: 28px;
  border-bottom: 1px solid var(--border-light);
}

.hero-badge {
  display: flex;
  align-items: center;
  gap: 16px;
}

.hero-avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
  background: var(--bg-tertiary);
  border: 2px solid var(--border-light);
}

.hero-avatar.placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26px;
  font-weight: 700;
  color: var(--accent-gold);
  font-family: "Noto Serif SC", serif;
}

.hero-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.hero-name {
  font-size: 30px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: 4px;
  font-family: "Noto Serif SC", serif;
}

.hero-meta {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 4px;
}

.difficulty-label {
  font-size: 13px;
  color: var(--text-muted);
  margin-right: 4px;
}

.star {
  font-size: 14px;
  color: var(--border-default);
}

.star.active {
  color: var(--accent-gold);
}

.doc-section {
  margin-bottom: 48px;
}

.doc-section h2 {
  font-size: 22px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 20px;
  padding-left: 14px;
  border-left: 4px solid var(--accent-gold);
  letter-spacing: 1px;
  font-family: "Noto Serif SC", serif;
}

.empty-content {
  color: var(--text-muted);
  font-size: 14px;
  padding: 32px;
  text-align: center;
  background: var(--bg-secondary);
  border-radius: 8px;
  border: 1px dashed var(--border-default);
}

/* Matchup styles */
.matchup-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.matchup-item {
  background: var(--bg-secondary);
  border: 1px solid var(--border-light);
  border-radius: 10px;
  padding: 24px;
}

.matchup-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.matchup-vs {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.matchup-type {
  padding: 3px 12px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.matchup-type.easy {
  background: rgba(39, 174, 96, 0.1);
  color: var(--diff-normal);
}

.matchup-type.even {
  background: rgba(230, 126, 34, 0.1);
  color: var(--diff-advanced);
}

.matchup-type.hard {
  background: rgba(192, 57, 43, 0.1);
  color: var(--diff-hard);
}

.loading-wrapper {
  max-width: 860px;
  margin: 60px auto;
  padding: 0 48px;
}

@media (max-width: 768px) {
  .article {
    padding: 24px 20px 60px;
  }
  .hero-name {
    font-size: 24px;
  }
}
</style>
