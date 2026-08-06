<template>
  <footer class="page-footer">
    <div class="footer-inner">
      <div class="footer-brand">
        <span class="brand-icon">剑</span>
        <span class="brand-name">劫学院</span>
      </div>
      <p class="footer-disclaimer">
        劫学院为玩家自制非官方教学站点，所有教学视频均跳转抖音平台，版权归原作者所有。
      </p>
      <div class="footer-divider"></div>
      <p class="footer-copyright">© {{ currentYear }} 劫学院 · 永劫无间教学资料库</p>
    </div>
  </footer>
</template>

<script setup>
const currentYear = new Date().getFullYear()
</script>

<style scoped>
.page-footer {
  background: var(--bg-secondary);
  border-top: 1px solid var(--border-default);
  padding: 48px 24px 32px;
  margin-top: 80px;
}

.footer-inner {
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
}

.footer-brand {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-bottom: 16px;
}

.brand-icon {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, var(--accent-gold), var(--accent-gold-light));
  color: #fff;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: 700;
  font-family: "Noto Serif SC", serif;
}

.brand-name {
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: 4px;
  font-family: "Noto Serif SC", serif;
}

.footer-disclaimer {
  font-size: 13px;
  color: var(--text-muted);
  margin-bottom: 20px;
  line-height: 1.8;
}

.footer-divider {
  width: 60px;
  height: 1px;
  background: var(--border-default);
  margin: 0 auto 20px;
}

.footer-copyright {
  font-size: 12px;
  color: var(--text-light);
}
</style>
