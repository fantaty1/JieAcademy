<template>
  <header class="navbar" :class="{ 'scrolled': isScrolled }">
    <div class="navbar-inner">
      <router-link to="/" class="brand">
        <div class="brand-icon-wrapper">
          <span class="brand-icon">剑</span>
        </div>
        <span class="brand-text">劫学院</span>
      </router-link>

      <nav class="nav-menu">
        <router-link to="/weapons" class="nav-link" active-class="active">近战武器</router-link>
        <router-link to="/weapon-tutorials" class="nav-link" active-class="active">武器教学</router-link>
        <router-link to="/heroes" class="nav-link" active-class="active">英雄</router-link>
        <router-link to="/hero-tutorials" class="nav-link" active-class="active">英雄教学</router-link>
      </nav>

      <div class="nav-right">
        <template v-if="userStore.isLoggedIn">
          <el-dropdown trigger="click" @command="handleCommand">
            <span class="user-info">
              <el-avatar :size="36" :src="userStore.userInfo?.avatar || ''" class="user-avatar">
                {{ userStore.userInfo?.nickname?.[0] || userStore.userInfo?.username?.[0] || '用' }}
              </el-avatar>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item disabled>{{ userStore.userInfo?.nickname || userStore.userInfo?.username }}</el-dropdown-item>
                <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
        <template v-else>
          <router-link to="/login" class="login-btn">登录</router-link>
          <router-link to="/register" class="register-btn">注册</router-link>
        </template>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()
const isScrolled = ref(false)

function handleScroll() {
  isScrolled.value = window.scrollY > 20
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})

function handleCommand(command) {
  if (command === 'logout') {
    userStore.logout()
    router.push('/')
  }
}
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 72px;
  background: transparent;
  z-index: 1000;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  border-bottom: 1px solid transparent;
}

.navbar.scrolled {
  background: var(--glass-bg);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-bottom: 1px solid var(--glass-border);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
  height: 64px;
}

.navbar-inner {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 40px;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  group: hover;
}

.brand-icon-wrapper {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: linear-gradient(135deg, var(--accent-gold), #8A6420);
  padding: 2px;
  box-shadow: var(--shadow-sm);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.brand:hover .brand-icon-wrapper {
  transform: translateY(-2px);
  box-shadow: var(--shadow-glow);
}

.brand-icon {
  width: 100%;
  height: 100%;
  background: var(--bg-primary);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: 800;
  color: var(--accent-gold-light);
  font-family: "Noto Serif SC", serif;
}

.brand-text {
  font-size: 22px;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: 4px;
  font-family: "Noto Serif SC", serif;
  text-transform: uppercase;
}

.nav-menu {
  display: flex;
  gap: 8px;
  background: rgba(255,255,255,0.03);
  padding: 6px;
  border-radius: 100px;
  border: 1px solid rgba(255,255,255,0.05);
}

.nav-link {
  padding: 8px 24px;
  border-radius: 100px;
  color: var(--text-secondary);
  font-size: 15px;
  font-weight: 500;
  transition: all 0.3s ease;
  text-decoration: none;
  letter-spacing: 1px;
  position: relative;
  overflow: hidden;
}

.nav-link::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: var(--accent-gold);
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: -1;
  border-radius: 100px;
}

.nav-link:hover {
  color: var(--text-primary);
}

.nav-link:hover::before {
  opacity: 0.1;
}

.nav-link.active {
  color: #000;
  background: var(--accent-gold);
  font-weight: 600;
  box-shadow: 0 0 15px rgba(212, 175, 55, 0.4);
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-info {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 4px;
  border-radius: 50%;
  border: 2px solid transparent;
  transition: all 0.3s ease;
}

.user-info:hover {
  border-color: var(--accent-gold);
  box-shadow: var(--shadow-glow);
}

.user-avatar {
  background: linear-gradient(135deg, var(--accent-gold), #8A6420);
  color: #000;
  font-size: 16px;
  font-weight: 700;
}

.login-btn {
  padding: 8px 24px;
  border-radius: 8px;
  color: var(--text-primary);
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.login-btn:hover {
  color: var(--accent-gold);
}

.register-btn {
  padding: 8px 24px;
  border-radius: 8px;
  background: linear-gradient(135deg, var(--accent-gold), #B8860B);
  color: #000;
  font-size: 14px;
  font-weight: 700;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);
}

.register-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(212, 175, 55, 0.5);
  background: linear-gradient(135deg, var(--accent-gold-light), var(--accent-gold));
  color: #000;
}

@media (max-width: 768px) {
  .navbar-inner {
    padding: 0 20px;
  }
  .nav-menu {
    display: none; /* Can implement mobile menu later */
  }
}
</style>
