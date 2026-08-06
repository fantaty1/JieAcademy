import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: { title: '首页' }
  },
  {
    path: '/weapons',
    name: 'WeaponList',
    component: () => import('@/views/weapon/WeaponList.vue'),
    meta: { title: '近战武器' }
  },
  {
    path: '/weapon-tutorials/:id?',
    name: 'WeaponTutorial',
    component: () => import('@/views/weapon/WeaponTutorial.vue'),
    meta: { title: '武器教学' }
  },
  {
    path: '/heroes',
    name: 'HeroList',
    component: () => import('@/views/hero/HeroList.vue'),
    meta: { title: '英雄' }
  },
  {
    path: '/hero-tutorials/:id?',
    name: 'HeroTutorial',
    component: () => import('@/views/hero/HeroTutorial.vue'),
    meta: { title: '英雄教学' }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/Login.vue'),
    meta: { title: '登录' }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/auth/Register.vue'),
    meta: { title: '注册' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (to.hash) {
      return { el: to.hash, behavior: 'smooth', top: 70 }
    }
    if (savedPosition) {
      return savedPosition
    }
    return { top: 0 }
  }
})

router.beforeEach((to, from, next) => {
  document.title = `${to.meta.title || ''} - 劫学院`
  next()
})

export default router
