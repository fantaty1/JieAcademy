<template>
  <el-config-provider :locale="zhCn">
    <div class="app-container">
      <NavBar />
      <main class="main-content">
        <router-view />
      </main>
      <PageFooter />
    </div>
  </el-config-provider>
</template>

<script setup>
import { onMounted } from 'vue'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import NavBar from '@/components/layout/NavBar.vue'
import PageFooter from '@/components/layout/PageFooter.vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

onMounted(() => {
  userStore.initFromStorage()
})
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  padding-top: 64px;
}
</style>
