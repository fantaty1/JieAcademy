<template>
  <div class="weapon-detail" v-if="weapon">
    <SideBar :title="weapon.name" :sections="sidebarSections" />

    <main class="detail-main">
      <article class="article">
        <!-- 武器头 -->
        <header class="article-header">
          <div class="weapon-badge">
            <span class="weapon-icon" v-if="weapon.icon">
              <img :src="weapon.icon" :alt="weapon.name" />
            </span>
            <span class="weapon-icon placeholder" v-else>{{ weapon.name[0] }}</span>
            <div>
              <h1 class="weapon-name">{{ weapon.name }}</h1>
            </div>
          </div>
        </header>

        <!-- 武器简介 -->
        <section id="intro" class="doc-section">
          <h2>武器简介</h2>
          <div v-if="weapon.description" class="doc-body" v-html="renderMd(weapon.description)"></div>
          <div v-else class="empty-content">暂无简介</div>
        </section>

        <!-- 基础连招 -->
        <section id="combos-normal" class="doc-section">
          <ComboSection title="基础连招" difficulty="normal" :combos="normalCombos" />
        </section>

        <!-- 进阶连招 -->
        <section id="combos-advanced" class="doc-section">
          <ComboSection title="进阶连招" difficulty="advanced" :combos="advancedCombos" />
        </section>

        <!-- 困难连招 -->
        <section id="combos-hard" class="doc-section">
          <ComboSection title="绝活连招" difficulty="hard" :combos="hardCombos" />
        </section>

        <!-- 实战思路 -->
        <section id="battle-tips" class="doc-section">
          <h2>实战思路</h2>
          <div class="empty-content">暂无内容，敬请期待</div>
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
import { getWeapon, getWeaponCombos } from '@/api/weapons'
import SideBar from '@/components/layout/SideBar.vue'
import ComboSection from '@/components/ComboSection.vue'

const md = new MarkdownIt({ html: false, linkify: true })
const route = useRoute()

const weapon = ref(null)
const combos = ref([])
const loading = ref(true)

const sidebarSections = [
  { id: 'intro', label: '武器简介' },
  { id: 'combos-normal', label: '基础连招' },
  { id: 'combos-advanced', label: '进阶连招' },
  { id: 'combos-hard', label: '绝活连招' },
  { id: 'battle-tips', label: '实战思路' },
]

const normalCombos = computed(() => combos.value.filter(c => c.difficulty === 'normal'))
const advancedCombos = computed(() => combos.value.filter(c => c.difficulty === 'advanced'))
const hardCombos = computed(() => combos.value.filter(c => c.difficulty === 'hard'))

function renderMd(text) {
  return md.render(text || '')
}

onMounted(async () => {
  const id = route.params.id
  try {
    const [wRes, cRes] = await Promise.all([
      getWeapon(id),
      getWeaponCombos(id)
    ])
    weapon.value = wRes
    combos.value = cRes.results || cRes
  } catch (e) {
    console.error('加载武器详情失败', e)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.weapon-detail {
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

.weapon-badge {
  display: flex;
  align-items: center;
  gap: 16px;
}

.weapon-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  overflow: hidden;
  flex-shrink: 0;
  background: var(--bg-tertiary);
}

.weapon-icon.placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: 700;
  color: var(--accent-gold);
  font-family: "Noto Serif SC", serif;
}

.weapon-icon img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.weapon-name {
  font-size: 30px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: 4px;
  font-family: "Noto Serif SC", serif;
}

.weapon-type {
  font-size: 14px;
  color: var(--text-muted);
  margin-top: 2px;
  display: block;
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

.loading-wrapper {
  max-width: 860px;
  margin: 60px auto;
  padding: 0 48px;
}

@media (max-width: 768px) {
  .article {
    padding: 24px 20px 60px;
  }
  .weapon-name {
    font-size: 24px;
  }
}
</style>
