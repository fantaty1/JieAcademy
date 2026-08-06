<template>
  <router-link :to="`/heroes/${hero.id}`" class="hero-card">
    <div class="card-avatar">
      <img v-if="hero.avatar" :src="hero.avatar" :alt="hero.name" />
      <div v-else class="avatar-placeholder">{{ hero.name[0] }}</div>
    </div>
    <h3 class="card-name">{{ hero.name }}</h3>
    <div class="card-stars">
      <span
        v-for="i in 5"
        :key="i"
        class="star"
        :class="{ active: i <= hero.difficulty }"
      >{{ i <= hero.difficulty ? '★' : '☆' }}</span>
    </div>
  </router-link>
</template>

<script setup>
defineProps({
  hero: { type: Object, required: true }
})
</script>

<style scoped>
.hero-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 24px 16px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  text-decoration: none;
  transition: all 0.3s;
}

.hero-card:hover {
  transform: translateY(-4px);
  border-color: var(--border-hover);
  box-shadow: var(--shadow-hover);
}

.card-avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
  background: var(--bg-tertiary);
  border: 2px solid var(--border-light);
}

.card-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: 700;
  color: var(--accent-gold);
  font-family: "Noto Serif SC", serif;
}

.card-name {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: 1px;
}

.card-stars {
  display: flex;
  gap: 2px;
}

.star {
  font-size: 12px;
  color: var(--border-default);
}

.star.active {
  color: var(--accent-gold);
}
</style>
