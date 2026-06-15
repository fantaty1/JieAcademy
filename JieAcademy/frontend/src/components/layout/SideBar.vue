<template>
  <aside class="sidebar" :class="{ collapsed: isCollapsed }">
    <div class="sidebar-header">
      <span class="sidebar-title" v-show="!isCollapsed">{{ title }}</span>
      <button class="collapse-btn" @click="isCollapsed = !isCollapsed">
        {{ isCollapsed ? '展开' : '收起' }}
      </button>
    </div>
    <nav class="sidebar-nav" v-show="!isCollapsed">
      <a
        v-for="item in sections"
        :key="item.id"
        :href="'#' + item.id"
        class="sidebar-link"
        :class="{ active: activeSection === item.id }"
        @click.prevent="scrollTo(item.id)"
      >
        <span class="link-dot"></span>
        {{ item.label }}
      </a>
    </nav>
  </aside>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  title: { type: String, default: '目录' },
  sections: { type: Array, default: () => [] },
})

const isCollapsed = ref(false)
const activeSection = ref('')

function scrollTo(id) {
  const el = document.getElementById(id)
  if (el) {
    const offset = 80
    const top = el.getBoundingClientRect().top + window.scrollY - offset
    window.scrollTo({ top, behavior: 'smooth' })
  }
}

function onScroll() {
  const scrollPos = window.scrollY + 100
  for (let i = props.sections.length - 1; i >= 0; i--) {
    const el = document.getElementById(props.sections[i].id)
    if (el && el.offsetTop <= scrollPos) {
      activeSection.value = props.sections[i].id
      break
    }
  }
}

onMounted(() => {
  window.addEventListener('scroll', onScroll, { passive: true })
  if (props.sections.length) {
    activeSection.value = props.sections[0].id
  }
})

onUnmounted(() => {
  window.removeEventListener('scroll', onScroll)
})
</script>

<style scoped>
.sidebar {
  width: 240px;
  min-width: 240px;
  background: var(--bg-secondary);
  border-right: 1px solid var(--border-default);
  height: calc(100vh - 64px);
  position: sticky;
  top: 64px;
  overflow-y: auto;
  transition: width 0.3s, min-width 0.3s;
}

.sidebar.collapsed {
  width: 48px;
  min-width: 48px;
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 16px;
  border-bottom: 1px solid var(--border-light);
}

.sidebar-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-secondary);
  letter-spacing: 2px;
}

.collapse-btn {
  background: none;
  border: none;
  color: var(--text-muted);
  font-size: 12px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: all 0.2s;
}

.collapse-btn:hover {
  color: var(--accent-gold);
  background: var(--accent-gold-bg);
}

.sidebar-nav {
  padding: 12px 0;
}

.sidebar-link {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 20px;
  font-size: 14px;
  color: var(--text-secondary);
  text-decoration: none;
  transition: all 0.2s;
  border-right: 3px solid transparent;
}

.sidebar-link:hover {
  color: var(--text-primary);
  background: var(--bg-tertiary);
}

.sidebar-link.active {
  color: var(--accent-gold);
  border-right-color: var(--accent-gold);
  background: var(--accent-gold-bg);
  font-weight: 500;
}

.link-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--border-default);
  flex-shrink: 0;
  transition: background 0.2s;
}

.sidebar-link.active .link-dot {
  background: var(--accent-gold);
}

@media (max-width: 768px) {
  .sidebar {
    display: none;
  }
}
</style>
