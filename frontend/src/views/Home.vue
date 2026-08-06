<template>
  <div class="home">
    <!-- Banner -->
    <section class="hero-banner">
      <div class="banner-content">
        <div class="banner-badge">永劫无间教学资料库</div>
        <h1 class="banner-title">劫学院</h1>
        <p class="banner-desc">全武器 · 全英雄 · 连招攻略 · 实战教学</p>
        <div class="banner-tags">
          <span class="tag">基础连招</span>
          <span class="tag">进阶技巧</span>
          <span class="tag">绝活操作</span>
          <span class="tag">英雄对策</span>
        </div>
      </div>
      <div class="banner-deco">
        <div class="deco-circle c1"></div>
        <div class="deco-circle c2"></div>
      </div>
    </section>

    <!-- 武器 -->
    <section class="section">
      <div class="section-header">
        <div>
          <h2 class="section-title">武器连招</h2>
          <p class="section-desc">选择武器，查看从入门到精通的连招教学</p>
        </div>
        <router-link to="/weapons" class="view-all">查看全部 →</router-link>
      </div>
      <div class="card-grid weapons-grid">
        <WeaponCard v-for="w in weapons" :key="w.id" :weapon="w" />
      </div>
    </section>

    <!-- 英雄 -->
    <section class="section">
      <div class="section-header">
        <div>
          <h2 class="section-title">英雄攻略</h2>
          <p class="section-desc">了解各英雄技能、连招与应对策略</p>
        </div>
        <router-link to="/heroes" class="view-all">查看全部 →</router-link>
      </div>
      <div class="card-grid heroes-grid">
        <HeroCard v-for="h in heroes" :key="h.id" :hero="h" />
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getWeapons } from '@/api/weapons'
import { getHeroes } from '@/api/heroes'
import WeaponCard from '@/components/WeaponCard.vue'
import HeroCard from '@/components/HeroCard.vue'

const weapons = ref([])
const heroes = ref([])

onMounted(async () => {
  try {
    const [wRes, hRes] = await Promise.all([getWeapons(), getHeroes()])
    weapons.value = wRes.results || wRes
    heroes.value = hRes.results || hRes
  } catch (e) {
    console.error('加载首页数据失败', e)
  }
})
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

/* Banner */
.hero-banner {
  position: relative;
  padding: 80px 0 60px;
  text-align: center;
  margin-bottom: 60px;
  overflow: hidden;
}

.banner-content {
  position: relative;
  z-index: 1;
}

.banner-badge {
  display: inline-block;
  padding: 6px 20px;
  background: var(--accent-gold-bg);
  border: 1px solid rgba(184, 134, 11, 0.15);
  border-radius: 20px;
  font-size: 13px;
  color: var(--accent-gold);
  letter-spacing: 2px;
  margin-bottom: 20px;
}

.banner-title {
  font-size: 56px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: 12px;
  margin-bottom: 16px;
  font-family: "Noto Serif SC", serif;
}

.banner-desc {
  font-size: 18px;
  color: var(--text-secondary);
  margin-bottom: 28px;
  letter-spacing: 2px;
}

.banner-tags {
  display: flex;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
}

.tag {
  padding: 8px 20px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-default);
  border-radius: 8px;
  font-size: 13px;
  color: var(--text-secondary);
  letter-spacing: 1px;
}

.banner-deco {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
}

.deco-circle {
  position: absolute;
  border-radius: 50%;
  border: 1px solid var(--border-light);
}

.deco-circle.c1 {
  width: 300px;
  height: 300px;
  top: -100px;
  right: -50px;
  opacity: 0.5;
}

.deco-circle.c2 {
  width: 200px;
  height: 200px;
  bottom: -60px;
  left: -30px;
  opacity: 0.3;
}

/* Sections */
.section {
  margin-bottom: 60px;
}

.section-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  margin-bottom: 28px;
}

.section-title {
  font-size: 22px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: 2px;
  margin-bottom: 6px;
  font-family: "Noto Serif SC", serif;
}

.section-desc {
  font-size: 14px;
  color: var(--text-muted);
}

.view-all {
  font-size: 14px;
  color: var(--text-muted);
  text-decoration: none;
  transition: color 0.2s;
  white-space: nowrap;
}

.view-all:hover {
  color: var(--accent-gold);
}

.card-grid {
  display: grid;
  gap: 16px;
}

.weapons-grid {
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
}

.heroes-grid {
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
}

@media (max-width: 768px) {
  .banner-title {
    font-size: 36px;
    letter-spacing: 6px;
  }
  .banner-desc {
    font-size: 15px;
  }
  .weapons-grid {
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  }
  .heroes-grid {
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  }
}
</style>
