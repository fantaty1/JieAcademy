import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as loginApi, register as registerApi, getProfile } from '@/api/auth'

export const useUserStore = defineStore('user', () => {
  const token = ref(null)
  const refreshToken = ref(null)
  const userInfo = ref(null)

  const isLoggedIn = computed(() => !!token.value)
  const isAdmin = computed(() => userInfo.value?.is_admin || false)

  function initFromStorage() {
    const storedToken = localStorage.getItem('access_token')
    const storedRefresh = localStorage.getItem('refresh_token')
    if (storedToken) {
      token.value = storedToken
      refreshToken.value = storedRefresh
      fetchProfile()
    }
  }

  async function login(username, password) {
    const res = await loginApi({ username, password })
    setTokens(res.tokens.access, res.tokens.refresh)
    userInfo.value = res.user
    return res
  }

  async function register(data) {
    const res = await registerApi(data)
    setTokens(res.tokens.access, res.tokens.refresh)
    userInfo.value = res.user
    return res
  }

  async function fetchProfile() {
    try {
      const res = await getProfile()
      userInfo.value = res
    } catch (e) {
      logout()
    }
  }

  function setTokens(access, refresh) {
    token.value = access
    refreshToken.value = refresh
    localStorage.setItem('access_token', access)
    localStorage.setItem('refresh_token', refresh)
  }

  function logout() {
    token.value = null
    refreshToken.value = null
    userInfo.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  return {
    token, refreshToken, userInfo,
    isLoggedIn, isAdmin,
    initFromStorage, login, register, fetchProfile, logout
  }
})
