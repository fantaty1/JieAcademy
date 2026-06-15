<template>
  <div class="matchup-list-page">
    <div class="page-header">
      <h1 class="page-title">英雄应对</h1>
      <p class="page-desc">查看各英雄之间的应对策略与克制关系</p>
    </div>

    <div class="filter-bar">
      <el-select v-model="selectedHero" placeholder="选择英雄" clearable size="default" style="width: 160px">
        <el-option v-for="h in heroes" :key="h.id" :label="h.name" :value="h.id" />
      </el-select>
      <el-select v-model="selectedType" placeholder="对局类型" clearable size="default" style="width: 140px">
        <el-option label="简单" value="easy" />
        <el-option label="均势" value="even" />
        <el-option label="困难" value="hard" />
      </el-select>
    </div>

    <div v-if="filteredMatchups.length" class="matchup-grid">
      <div v-for="m in filteredMatchups" :key="m.id" class="matchup-card">
        <div class="matchup-header">
          <span class="hero-name">{{ m.hero_name }}</span>
          <span class="vs">VS</span>
          <span class="hero-name">{{ m.opponent_name }}</span>
        </div>
        <div class="matchup-meta">
          <span class="matchup-type" :class="m.matchup_type">{{ matchupLabel(m.matchup_type) }}</span>
        </div>
        <router-link :to="`/heroes/${m.hero}`" class="matchup-link">查看详情 →</router-link>
      </div>
    </div>

    <el-empty v-else-if="!loading" description="暂无应对数据" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getHeroes } from '@/api/heroes'
import { getMatchups } from '@/api/tutorials'

const heroes = ref([])
const matchups = ref([])
const selectedHero = ref('')
const selectedType = ref('')
const loading = ref(true)

const filteredMatchups = computed(() => {
  return matchups.value.filter(m => {
    if (selectedHero.value && m.hero !== selectedHero.value && m.opponent !== selectedHero.value) return false
    if (selectedType.value && m.matchup_type !== selectedType.value) return false
    return true
  })
})

function matchupLabel(type) {
  const map = { easy: '简单', even: '均势', hard: '困难' }
  return map[type] || type
}

onMounted(async () => {
  try {
    const [hRes, mRes] = await Promise.all([getHeroes(), getMatchups()])
    heroes.value = hRes.results || hRes
    matchups.value = mRes.results || mRes
  } catch (e) {
    console.error('加载应对数据失败', e)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.matchup-list-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 48px 24px;
}

.page-header {
  margin-bottom: 36px;
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: 4px;
  margin-bottom: 8px;
  font-family: "Noto Serif SC", serif;
}

.page-desc {
  font-size: 15px;
  color: var(--text-secondary);
}

.filter-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 28px;
  flex-wrap: wrap;
}

.matchup-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.matchup-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border-light);
  border-radius: 10px;
  padding: 24px;
  transition: all 0.2s;
}

.matchup-card:hover {
  border-color: var(--border-hover);
  box-shadow: var(--shadow-sm);
}

.matchup-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin-bottom: 14px;
}

.hero-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.vs {
  font-size: 13px;
  color: var(--text-muted);
  font-weight: 500;
  letter-spacing: 2px;
}

.matchup-meta {
  text-align: center;
  margin-bottom: 14px;
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

.matchup-link {
  display: block;
  text-align: center;
  font-size: 13px;
  color: var(--accent-gold);
  text-decoration: none;
  transition: color 0.2s;
}

.matchup-link:hover {
  color: var(--accent-gold-light);
}

@media (max-width: 768px) {
  .matchup-grid {
    grid-template-columns: 1fr;
  }
}
</style>
