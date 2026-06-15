<template>
  <router-link :to="`/weapons/${weapon.id}`" class="weapon-card">
    <div class="card-icon">
      <img v-if="weapon.icon" :src="weapon.icon" :alt="weapon.name" />
      <div v-else class="icon-placeholder">{{ weapon.name[0] }}</div>
    </div>
    <h3 class="card-name">{{ weapon.name }}</h3>
  </router-link>
</template>

<script setup>
defineProps({
  weapon: { type: Object, required: true }
})
</script>

<style scoped>
.weapon-card {
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

.weapon-card:hover {
  transform: translateY(-4px);
  border-color: var(--border-hover);
  box-shadow: var(--shadow-hover);
}

.card-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  overflow: hidden;
  flex-shrink: 0;
  background: var(--bg-tertiary);
}

.card-icon img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.icon-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
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
</style>
