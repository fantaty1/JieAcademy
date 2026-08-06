<template>
  <div class="page-wrapper">
    <!-- 左侧全局导航栏 -->
    <aside class="global-sidebar">
      <div class="sidebar-header">
        <span class="icon">🥷</span>
        <span class="title">英雄图鉴大全</span>
      </div>
      <div class="sidebar-content">
        <ul class="nav-list">
          <li 
            v-for="(hero, index) in heroes" 
            :key="index"
            class="nav-item"
            :class="{ active: currentHeroId === hero.id }"
            @click="scrollToHero(hero.id)"
          >
            <span class="nav-text">{{ hero.name.split(' (')[0] }}</span>
          </li>
        </ul>
      </div>
    </aside>

    <div class="snap-container hero-list-page">
      <section 
        v-for="(hero, index) in heroes" 
        :key="hero.id" 
        :id="'hero-' + hero.id"
      class="snap-section hero-section"
      :style="{ backgroundImage: `url(${hero.image})` }"
    >
      <div class="overlay"></div>
      
      <div class="content-wrapper" :class="{ 'reverse': index % 2 !== 0 }">
        <div class="text-content">
          <h1 class="hero-name">{{ hero.name }}</h1>
          <p class="hero-desc">{{ hero.description }}</p>
          <div class="hero-stats">
            <div class="stat">
              <span class="label">机动</span>
              <el-progress :percentage="hero.mobility" :color="customColors" :show-text="false" />
            </div>
            <div class="stat">
              <span class="label">爆发</span>
              <el-progress :percentage="hero.burst" :color="customColors" :show-text="false" />
            </div>
            <div class="stat">
              <span class="label">生存</span>
              <el-progress :percentage="hero.survival" :color="customColors" :show-text="false" />
            </div>
          </div>
          <router-link :to="`/hero-tutorials/${hero.id}`" class="action-btn">
            进入教学 <span class="arrow">→</span>
          </router-link>
        </div>
      </div>
      
      <div class="scroll-indicator" v-if="index < heroes.length - 1">
        <span>下滑查看更多</span>
        <i class="scroll-arrow">↓</i>
      </div>
    </section>
  </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const currentHeroId = ref('jianan')

const scrollToHero = (id) => {
  currentHeroId.value = id
  const el = document.getElementById('hero-' + id)
  if (el) {
    el.scrollIntoView({ behavior: 'smooth' })
  }
}

const customColors = [
  { color: '#00F0FF', percentage: 100 } /* Neon Cyan for heroes to differentiate from gold weapons */
]

const heroes = ref([
  { id: 'jianan', name: '迦南 (Matari)', description: '沙漠中的曼珠沙华，刺客的巅峰。拥有极高的机动性和隐身能力，是偷袭和逃生的专家。', mobility: 100, burst: 90, survival: 40, image: 'https://images.unsplash.com/photo-1542546068979-b6fb1ce4ba60?q=80&w=1920&auto=format&fit=crop' },
  { id: 'yaodaoji', name: '妖刀姬 (Yoto Hime)', description: '带着诅咒之刃的少女。拥有极强的爆发伤害和瞬间斩杀能力。', mobility: 60, burst: 100, survival: 50, image: 'https://images.unsplash.com/photo-1614216390196-8eb59efae414?q=80&w=1920&auto=format&fit=crop' },
  { id: 'jicanghai', name: '季沧海 (Tarka Ji)', description: '烈火如歌，豪情万丈。能驾驭火焰，在人群中穿梭自如，越战越勇。', mobility: 85, burst: 80, survival: 70, image: 'https://images.unsplash.com/photo-1509347528160-9a9e33742cdb?q=80&w=1920&auto=format&fit=crop' },
  { id: 'tianhai', name: '天海 (Tianhai)', description: '云游天下的少林武僧，拥有金刚不坏之身。开启大招后化身为巨大金刚，以压倒性的力量掌控战局。', mobility: 30, burst: 85, survival: 100, image: 'https://images.unsplash.com/photo-1596700875691-382d62153df9?q=80&w=1920&auto=format&fit=crop' },
  { id: 'ninghongye', name: '宁红夜 (Viper Ning)', description: '昆仑圣女，盲剑客。擅长控制和团队封锁，是团战中的绝对核心。', mobility: 50, burst: 70, survival: 60, image: 'https://images.unsplash.com/photo-1588600878108-578307a3cc9d?q=80&w=1920&auto=format&fit=crop' },
  { id: 'temuer', name: '特木尔 (Temulch)', description: '草原的苍狼。能够驾驭风沙，控制战场，是极强的团战控制型英雄。', mobility: 60, burst: 60, survival: 80, image: 'https://images.unsplash.com/photo-1590403370956-620ee6f1a4e2?q=80&w=1920&auto=format&fit=crop' },
  { id: 'hutao', name: '土御门胡桃 (Kurumi)', description: '日轮之花，掌握着治愈之力。团队中不可或缺的支援角色，同时也能通过阵法为队伍提供强大的增益。', mobility: 60, burst: 30, survival: 80, image: 'https://images.unsplash.com/photo-1605806616949-1e87b487cb2a?q=80&w=1920&auto=format&fit=crop' },
  { id: 'yueshan', name: '岳山 (Yueshan)', description: '无极帝国将领。开启大招化身兵马俑，摧枯拉朽，无人能挡。', mobility: 40, burst: 85, survival: 95, image: 'https://images.unsplash.com/photo-1555597673-b21d5c935865?q=80&w=1920&auto=format&fit=crop' },
  { id: 'cuisanniang', name: '崔三娘 (Valda Cui)', description: '纵横四海的龙王。驾驭水流，拥有极强的控制和限制能力。', mobility: 55, burst: 75, survival: 65, image: 'https://images.unsplash.com/photo-1610486334691-872fba1766dd?q=80&w=1920&auto=format&fit=crop' },
  { id: 'wuchen', name: '无尘 (Wuchen)', description: '隐族使者，道法自然。可以通过剑气和阵法保护队友，转移战场。', mobility: 70, burst: 60, survival: 75, image: 'https://images.unsplash.com/photo-1520638023430-845183db08f3?q=80&w=1920&auto=format&fit=crop' },
  { id: 'guqinghan', name: '顾清寒 (Justina Gu)', description: '冰清玉洁的冰雁。利用寒冰真气冻结敌人，拥有极高的爆发和生存能力。', mobility: 75, burst: 85, survival: 70, image: 'https://images.unsplash.com/photo-1589149098258-3e9102cd63d3?q=80&w=1920&auto=format&fit=crop' },
  { id: 'wutianxinzha', name: '武田信忠 (Takeda)', description: '末路狂花，身负妖灵。在战斗中可以夺取敌人的武器，反制一切。', mobility: 65, burst: 90, survival: 65, image: 'https://images.unsplash.com/photo-1542546068979-b6fb1ce4ba60?q=80&w=1920&auto=format&fit=crop' },
  { id: 'yinziping', name: '殷紫萍 (Ziping Yin)', description: '萍踪侠影，妙手仁心。为团队提供持续的恢复和免伤，是团队的坚实后盾。', mobility: 55, burst: 20, survival: 90, image: 'https://images.unsplash.com/photo-1614216390196-8eb59efae414?q=80&w=1920&auto=format&fit=crop' },
  { id: 'shenmiao', name: '沈妙 (Feria Shen)', description: '火器世家的千金。可以召唤机甲进行炮轰，火力压制。', mobility: 80, burst: 80, survival: 85, image: 'https://images.unsplash.com/photo-1509347528160-9a9e33742cdb?q=80&w=1920&auto=format&fit=crop' },
  { id: 'huwei', name: '胡为 (Akos Hu)', description: '狂野不羁的虎将。化身猛虎扑击敌人，拥有极强的单体压制力。', mobility: 85, burst: 85, survival: 60, image: 'https://images.unsplash.com/photo-1596700875691-382d62153df9?q=80&w=1920&auto=format&fit=crop' },
  { id: 'jiyingying', name: '季莹莹 (Zai)', description: '九幽使者。使用锁链将敌人拖入无尽的深渊。', mobility: 70, burst: 90, survival: 50, image: 'https://images.unsplash.com/photo-1588600878108-578307a3cc9d?q=80&w=1920&auto=format&fit=crop' },
  { id: 'yulinglong', name: '玉玲珑 (Tessa)', description: '九尾妖狐的传人。魅惑敌人，在战场上翩翩起舞，杀人于无形。', mobility: 75, burst: 80, survival: 55, image: 'https://images.unsplash.com/photo-1590403370956-620ee6f1a4e2?q=80&w=1920&auto=format&fit=crop' },
  { id: 'hadi', name: '哈迪 (Hadi)', description: '机械天才。利用自制的飞行器在空中翱翔，发动突然袭击。', mobility: 95, burst: 70, survival: 50, image: 'https://images.unsplash.com/photo-1605806616949-1e87b487cb2a?q=80&w=1920&auto=format&fit=crop' },
  { id: 'weiqing', name: '魏轻 (Shayol Wei)', description: '执掌玄武之力的女官。拥有极强的反制和防御能力。', mobility: 50, burst: 65, survival: 90, image: 'https://images.unsplash.com/photo-1555597673-b21d5c935865?q=80&w=1920&auto=format&fit=crop' },
  { id: 'liulian', name: '刘炼 (Lycan)', description: '能够操纵磁力的方士。在战场上利用金属进行攻击和防御。', mobility: 65, burst: 75, survival: 70, image: 'https://images.unsplash.com/photo-1610486334691-872fba1766dd?q=80&w=1920&auto=format&fit=crop' },
  { id: 'zhangqiling', name: '张起灵 (Kylin Zhang)', description: '神秘莫测的寻龙者。身法诡秘，黑金古刀一击致命。', mobility: 85, burst: 95, survival: 60, image: 'https://images.unsplash.com/photo-1520638023430-845183db08f3?q=80&w=1920&auto=format&fit=crop' },
  { id: 'xila', name: '席拉 (Sylvia)', description: '掌握光耀之力的圣女。可以在战场上降下光芒，惩戒邪恶。', mobility: 60, burst: 80, survival: 70, image: 'https://images.unsplash.com/photo-1589149098258-3e9102cd63d3?q=80&w=1920&auto=format&fit=crop' },
  { id: 'lanmeng', name: '蓝梦 (Lan Meng)', description: '织梦者。能够让敌人陷入幻境，无法自拔。', mobility: 70, burst: 65, survival: 65, image: 'https://images.unsplash.com/photo-1542546068979-b6fb1ce4ba60?q=80&w=1920&auto=format&fit=crop' },
  { id: 'ganxuan', name: '甘璇 (Gan Xuan)', description: '机敏灵动的少女。擅长利用暗器和机关陷阱。', mobility: 80, burst: 70, survival: 55, image: 'https://images.unsplash.com/photo-1614216390196-8eb59efae414?q=80&w=1920&auto=format&fit=crop' },
  { id: 'lixunhuan', name: '李寻欢 (Li Xunhuan)', description: '小李飞刀，例无虚发。拥有绝对的远程压制和瞬间秒杀能力。', mobility: 75, burst: 100, survival: 40, image: 'https://images.unsplash.com/photo-1509347528160-9a9e33742cdb?q=80&w=1920&auto=format&fit=crop' },
  { id: 'wanjun', name: '万钧 (Wan Jun)', description: '力拔山兮的勇士。每一次攻击都带有雷霆万钧之势。', mobility: 35, burst: 90, survival: 95, image: 'https://images.unsplash.com/photo-1596700875691-382d62153df9?q=80&w=1920&auto=format&fit=crop' },
  { id: 'wuzhen', name: '巫真 (Wu Zhen)', description: '神秘的萨满。能够沟通灵魂，对敌人施加恶咒。', mobility: 55, burst: 75, survival: 70, image: 'https://images.unsplash.com/photo-1588600878108-578307a3cc9d?q=80&w=1920&auto=format&fit=crop' }
])
</script>

<style scoped>
.page-wrapper {
  display: flex;
  min-height: 100vh;
}

/* 全局左侧高级导航栏 */
.global-sidebar {
  position: fixed;
  top: 72px;
  left: 0;
  width: 240px;
  height: calc(100vh - 72px);
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(8px);
  border-right: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: none;
  z-index: 100;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 24px;
  border-bottom: 1px solid var(--border-light);
  display: flex;
  align-items: center;
  gap: 12px;
}

.sidebar-header .icon { font-size: 20px; }
.sidebar-header .title { font-size: 18px; font-weight: 700; color: var(--text-primary); letter-spacing: 2px; }

.sidebar-content {
  flex: 1;
  overflow-y: auto;
  padding: 16px 0;
  scrollbar-width: none;
}
.sidebar-content::-webkit-scrollbar { display: none; }

.nav-list { list-style: none; padding: 0; margin: 0; }
.nav-item { padding: 12px 24px; cursor: pointer; transition: all 0.3s ease; position: relative; display: flex; align-items: center; }
.nav-text { font-size: 15px; color: var(--text-secondary); font-weight: 500; transition: all 0.3s ease; letter-spacing: 1px; }

.nav-item:hover { background: var(--bg-primary); }
.nav-item:hover .nav-text { color: var(--accent-cyan); transform: translateX(4px); }
.nav-item.active { background: var(--accent-cyan-bg); }
.nav-item.active .nav-text { color: var(--accent-cyan); font-weight: 700; }
.nav-item.active::before { content: ''; position: absolute; left: 0; top: 0; height: 100%; width: 4px; background: var(--accent-cyan); box-shadow: 0 0 10px rgba(0, 139, 139, 0.5); }

.hero-list-page {
  flex: 1;
  margin-top: -72px; 
}

.hero-section {
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 255, 255, 0.5) 50%, rgba(255, 255, 255, 0.8) 100%);
  z-index: 1;
}

.content-wrapper {
  position: relative;
  z-index: 2;
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 40px 0 280px;
  display: flex;
  align-items: center;
}

.content-wrapper.reverse {
  justify-content: flex-end;
}

.text-content {
  width: 50%;
  padding: 40px;
  background: var(--glass-bg);
  backdrop-filter: blur(20px);
  border: 1px solid var(--glass-border);
  border-radius: 20px;
  box-shadow: var(--shadow-lg);
  transform: translateY(0);
  opacity: 0;
  animation: fadeUp 1s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.hero-name {
  font-size: 64px;
  font-weight: 900;
  color: var(--text-primary);
  margin-bottom: 20px;
  line-height: 1.1;
  font-family: "Noto Serif SC", serif;
  text-transform: uppercase;
  background: linear-gradient(120deg, var(--text-primary), var(--accent-cyan));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 4px 20px rgba(0, 240, 255, 0.2);
}

.hero-desc {
  font-size: 18px;
  color: var(--text-secondary);
  margin-bottom: 40px;
  line-height: 1.8;
  letter-spacing: 1px;
}

.hero-stats {
  margin-bottom: 40px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.stat {
  display: flex;
  align-items: center;
  gap: 16px;
}

.label {
  width: 60px;
  color: var(--text-light);
  font-weight: 600;
  font-size: 14px;
  letter-spacing: 2px;
}

.stat :deep(.el-progress) {
  flex: 1;
}

.stat :deep(.el-progress-bar__outer) {
  background-color: rgba(255, 255, 255, 0.1) !important;
  border-radius: 0;
  height: 6px !important;
}

.stat :deep(.el-progress-bar__inner) {
  border-radius: 0;
  background: linear-gradient(90deg, var(--accent-cyan), #00A3FF);
  box-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
}

.action-btn {
  display: inline-flex;
  align-items: center;
  padding: 16px 40px;
  background: linear-gradient(135deg, var(--accent-cyan), #00A3FF);
  color: #000;
  font-size: 18px;
  font-weight: 800;
  border-radius: 8px;
  text-decoration: none;
  transition: all 0.3s ease;
  letter-spacing: 2px;
  box-shadow: 0 4px 15px rgba(0, 240, 255, 0.4);
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 240, 255, 0.6);
  background: linear-gradient(135deg, #00FFFF, var(--accent-cyan));
}

.action-btn .arrow {
  margin-left: 8px;
  transition: transform 0.3s ease;
}

.action-btn:hover .arrow {
  transform: translateX(5px);
}

.scroll-indicator {
  position: absolute;
  bottom: 40px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 3;
  display: flex;
  flex-direction: column;
  align-items: center;
  color: var(--text-secondary);
  font-size: 12px;
  letter-spacing: 4px;
  opacity: 0.7;
  animation: bounce 2s infinite ease-in-out;
}

.scroll-arrow {
  margin-top: 8px;
  font-style: normal;
  font-size: 20px;
}

@keyframes fadeUp {
  0% {
    opacity: 0;
    transform: translateY(40px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes bounce {
  0%, 100% {
    transform: translate(-50%, 0);
  }
  50% {
    transform: translate(-50%, 10px);
  }
}

@media (max-width: 1024px) {
  .global-sidebar { width: 200px; }
  .content-wrapper { padding: 0 40px 0 240px; }
  .text-content {
    width: 80%;
  }
}

@media (max-width: 768px) {
  .global-sidebar { display: none; }
  .content-wrapper { padding: 0 24px; }
  .text-content {
    width: 100%;
    padding: 24px;
  }
  .hero-name {
    font-size: 40px;
  }
  .content-wrapper.reverse {
    justify-content: flex-start;
  }
}
</style>
