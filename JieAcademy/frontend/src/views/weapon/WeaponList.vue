<template>
  <div class="page-wrapper">
    <!-- 左侧全局导航栏 -->
    <aside class="global-sidebar">
      <div class="sidebar-header">
        <span class="icon">⚔️</span>
        <span class="title">近战武器大全</span>
      </div>
      <div class="sidebar-content">
        <ul class="nav-list">
          <li 
            v-for="(weapon, index) in weapons" 
            :key="index"
            class="nav-item"
            :class="{ active: currentWeaponId === weapon.id }"
            @click="scrollToWeapon(weapon.id)"
          >
            <span class="nav-text">{{ weapon.name.split(' (')[0] }}</span>
          </li>
        </ul>
      </div>
    </aside>

    <div class="snap-container weapon-list-page">
      <section 
        v-for="(weapon, index) in weapons" 
        :key="weapon.id" 
        :id="'weapon-' + weapon.id"
        class="snap-section weapon-section"
      >
        <!-- 只在导航栏右侧区域铺背景图 -->
        <div
          class="weapon-bg"
          :style="{ backgroundImage: `url(${weapon.image})` }"
        >
          <div class="overlay"></div>
        </div>

        <div class="scroll-indicator" v-if="index < weapons.length - 1">
          <span>下滑查看更多</span>
          <i class="scroll-arrow">↓</i>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const currentWeaponId = ref('changjian')

const scrollToWeapon = (id) => {
  currentWeaponId.value = id
  const el = document.getElementById('weapon-' + id)
  if (el) {
    el.scrollIntoView({ behavior: 'smooth' })
  }
}

const customColors = [
  { color: '#D4AF37', percentage: 100 }
]

const weapons = ref([
  { id: 'changjian',    name: '长剑 (Longsword)',         description: '剑气如虹，招式多变。长剑以其灵动飘逸的剑气攻击，成为最平衡的兵器。',               damage: 70,  speed: 75, range: 80,  image: '/weapons/长剑.png' },
  { id: 'taidao',       name: '太刀 (Katana)',             description: '灵动飘逸，杀机暗藏。太刀以其无与伦比的机动性和极快的出招速度，成为战场上最致命的利刃。', damage: 75,  speed: 90, range: 65,  image: '/weapons/太刀.png' },
  { id: 'kuodao',       name: '阔刀 (Greatsword)',         description: '大开大合，势不可挡。虽然挥舞缓慢，但每一次击中都能带来毁天灭地的爆发伤害，是力量的绝对象征。', damage: 100, speed: 40, range: 85,  image: '/weapons/阔刀.png' },
  { id: 'zhanmadao',    name: '斩马刀 (Zhanmadao)',        description: '马战利器，威力无穷。结合了长柄武器的范围和重型刀剑的威力。',                   damage: 95,  speed: 45, range: 90,  image: '/weapons/战马刀.png' },
  { id: 'changqiang',   name: '长枪 (Spear)',              description: '一寸长一寸强，百兵之王。长枪拥有极佳的攻击距离，在拉扯战中独领风骚。',             damage: 80,  speed: 70, range: 100, image: '/weapons/长枪.png' },
  { id: 'gun',          name: '棍 (Staff)',                description: '横扫千军，密不透风。棍法讲究连绵不绝，在混战中能造成大面积的控制和伤害。',           damage: 65,  speed: 80, range: 85,  image: '/weapons/长棍.png' },
  { id: 'bishou',       name: '匕首 (Dagger)',             description: '瞬息万变，见血封喉。匕首拥有游戏中最快的连招速度和极强的机动性，适合突袭与刺杀。',     damage: 60,  speed: 100, range: 30, image: '/weapons/匕首.png' },
  { id: 'shanzi',       name: '扇子 (Fan)',                description: '风流倜傥，暗器伤人。折扇开合之间，不仅能进行近战打击，还能发动远程突袭。',           damage: 55,  speed: 85, range: 50,  image: '/weapons/扇子.png' },
  { id: 'shuangdao',    name: '双刀 (Dual Blades)',        description: '双刀连斩，快如闪电。双手挥舞的利刃能像暴雨般倾泻在敌人身上。',                   damage: 70,  speed: 95, range: 45,  image: '/weapons/双刀.png' },
  { id: 'shuangji',     name: '双戟 (Dual Halberds)',      description: '攻防兼备，勾斩皆能。奇特的造型赋予了它变化莫测的招式。',                       damage: 85,  speed: 60, range: 60,  image: '/weapons/双戟.png' },
  { id: 'shuangjiegun', name: '双节棍 (Nunchucks)',        description: '刚柔并济，变幻莫测。极具节奏感的连击能让对手防不胜防。',                       damage: 65,  speed: 85, range: 40,  image: '/weapons/双截棍.png' },
  { id: 'hengdao',      name: '横刀 (Hengdao)',            description: '直刃利器，拔刀术惊人。极其讲究出刀瞬间的爆发力。',                           damage: 80,  speed: 85, range: 70,  image: '/weapons/横刀.png' },
  { id: 'quanren',      name: '拳刃 (Katar)',              description: '贴身短打，爆发极高。放弃了防御，将所有力量集中在双拳的突刺上。',                   damage: 85,  speed: 90, range: 20,  image: '/weapons/拳刃.png' },
  { id: 'lianjian',     name: '链剑 (Whip Sword)',         description: '可刚可柔，攻击范围广。展开时如长鞭，收缩时似利剑。',                         damage: 70,  speed: 75, range: 90,  image: '/weapons/链剑.png' },
  { id: 'feidao',       name: '飞刀 (Throwing Knives)',    description: '百步穿杨，例无虚发。极致的远程暗杀武器。',                                 damage: 50,  speed: 95, range: 100, image: '/weapons/飞刀.png' }
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
  background: #ffffff;
  border-right: 1px solid rgba(0, 0, 0, 0.08);
  box-shadow: 2px 0 12px rgba(0, 0, 0, 0.06);
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
.nav-item:hover .nav-text { color: var(--accent-gold); transform: translateX(4px); }
.nav-item.active { background: var(--accent-gold-bg); }
.nav-item.active .nav-text { color: var(--accent-gold); font-weight: 700; }
.nav-item.active::before { content: ''; position: absolute; left: 0; top: 0; height: 100%; width: 4px; background: var(--accent-gold); box-shadow: 0 0 10px rgba(212, 175, 55, 0.5); }

.weapon-list-page {
  flex: 1;
  /* 隐藏整体页面的边距，实现全屏 */
  margin-top: -72px; 
}

.weapon-section {
  position: relative;
  overflow: hidden;
}

/* 只覆盖导航栏右侧的背景图区域 */
.weapon-bg {
  position: absolute;
  top: 0;
  left: 240px; /* 与导航栏同宽，从导航栏右边缘开始 */
  right: 0;
  bottom: 0;
  background-size: contain;
  background-position: center center;
  background-repeat: no-repeat;
  background-attachment: scroll;
}

.overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(5, 8, 15, 0.55) 0%, rgba(5, 8, 15, 0.25) 50%, rgba(5, 8, 15, 0.50) 100%);
  z-index: 1;
}

.content-wrapper {
  position: relative;
  z-index: 2;
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 40px 0 280px; /* 为侧边栏腾出空间 */
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

.weapon-name {
  font-size: 64px;
  font-weight: 900;
  color: var(--text-primary);
  margin-bottom: 20px;
  line-height: 1.1;
  font-family: "Noto Serif SC", serif;
  text-transform: uppercase;
  background: linear-gradient(120deg, var(--text-primary), var(--accent-gold));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 4px 20px rgba(212, 175, 55, 0.2);
}

.weapon-desc {
  font-size: 18px;
  color: var(--text-secondary);
  margin-bottom: 40px;
  line-height: 1.8;
  letter-spacing: 1px;
}

.weapon-stats {
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
  background: linear-gradient(90deg, var(--accent-gold), var(--accent-gold-light));
  box-shadow: 0 0 10px rgba(212, 175, 55, 0.5);
}

.action-btn {
  display: inline-flex;
  align-items: center;
  padding: 16px 40px;
  background: linear-gradient(135deg, var(--accent-gold), #8A6420);
  color: #000;
  font-size: 18px;
  font-weight: 800;
  border-radius: 8px;
  text-decoration: none;
  transition: all 0.3s ease;
  letter-spacing: 2px;
  box-shadow: 0 4px 15px rgba(212, 175, 55, 0.4);
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(212, 175, 55, 0.6);
  background: linear-gradient(135deg, var(--accent-gold-light), var(--accent-gold));
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
  .weapon-name {
    font-size: 40px;
  }
  .content-wrapper.reverse {
    justify-content: flex-start;
  }
}
</style>
