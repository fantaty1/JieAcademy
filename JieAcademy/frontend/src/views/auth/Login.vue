<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-brand">
        <span class="brand-icon">剑</span>
        <h2 class="auth-title">登录劫学院</h2>
      </div>

      <el-form ref="formRef" :model="form" :rules="rules" label-position="top" size="large">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" class="submit-btn" :loading="loading" @click="handleLogin">
            登录
          </el-button>
        </el-form-item>
      </el-form>

      <p class="auth-footer">
        还没有账号？
        <router-link to="/register" class="link">立即注册</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()
const formRef = ref(null)
const loading = ref(false)

const form = reactive({
  username: '',
  password: ''
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

async function handleLogin() {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  loading.value = true
  try {
    await userStore.login(form.username, form.password)
    ElMessage.success('登录成功')
    router.push('/')
  } catch (e) {
    const msg = e.response?.data?.detail || e.response?.data?.non_field_errors?.[0] || '登录失败'
    ElMessage.error(msg)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  min-height: calc(100vh - 64px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px 24px;
}

.auth-card {
  width: 100%;
  max-width: 400px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-light);
  border-radius: 16px;
  padding: 48px 36px;
  box-shadow: var(--shadow-md);
}

.auth-brand {
  text-align: center;
  margin-bottom: 36px;
}

.brand-icon {
  display: inline-flex;
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, var(--accent-gold), var(--accent-gold-light));
  color: #fff;
  border-radius: 12px;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: 700;
  font-family: "Noto Serif SC", serif;
  margin-bottom: 16px;
}

.auth-title {
  font-size: 22px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: 2px;
}

.submit-btn {
  width: 100%;
  height: 44px;
  font-size: 15px;
  letter-spacing: 2px;
}

.auth-footer {
  text-align: center;
  font-size: 14px;
  color: var(--text-muted);
  margin-top: 20px;
}

.link {
  color: var(--accent-gold);
  text-decoration: none;
  font-weight: 500;
}

.link:hover {
  color: var(--accent-gold-light);
}
</style>
