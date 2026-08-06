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
            v-for="(weapon, index) in allWeapons" 
            :key="index"
            class="nav-item"
            :class="{ active: currentWeaponId === weapon.id }"
            @click="selectWeapon(weapon.id)"
          >
            <span class="nav-text">{{ weapon.name.split(' (')[0] }}</span>
          </li>
        </ul>
      </div>
    </aside>

    <!-- 右侧内容区 -->
    <div class="tutorial-page">
      <div class="tutorial-header">
        <div class="header-content">
          <h1>{{ tutorialData.title }}</h1>
          <p class="subtitle">{{ tutorialData.subtitle }}</p>
          <div class="meta">
            <span class="author">作者: {{ tutorialData.author }}</span>
            <span class="date">更新时间: {{ tutorialData.date }}</span>
            <span class="difficulty">难度: <el-rate v-model="tutorialData.difficulty" disabled text-color="#D4AF37" /></span>
          </div>
        </div>
      </div>
      
      <div class="tutorial-container">
        <!-- 内容锚点目录 -->
        <div class="sidebar">
          <div class="nav-tree">
            <h3>目录</h3>
            <ul>
              <li><a href="#intro">一、 武器简介</a></li>
              <li><a href="#combos">二、 连招大全</a></li>
              <li><a href="#advanced">三、 进阶技巧</a></li>
              <li><a href="#matchups">四、 实战应对</a></li>
              
            </ul>
            <button class="premium-publish-btn" @click="openDialog()">
              <span class="btn-icon">✨</span>
              <span class="btn-text">发布我的教学</span>
              <div class="btn-glow"></div>
            </button>
          </div>
        </div>
        
        <div class="content doc-body">
          <h2 id="intro">一、 武器简介</h2>
          <div class="markdown-body" style="background: transparent; color: inherit; padding: 0;" v-html="md.render(tutorialData.intro)"></div>
          <h2 id="combos">二、 连招大全</h2>
          <p style="line-height: 1.8; color: var(--text-secondary); margin-bottom: 20px;">
            熟练掌握连招能大幅提升永劫无间实战上限，衔接流畅的连招可以在短时间内集中打出高额伤害，抓住对手受击僵直空档持续压制，不给对方振刀、闪避脱身的机会。实战里连招还能灵活衔接平 A、技能与钩索，适配不同武器特性，遇到近战缠斗时稳定压低敌方血量，拉扯过程中借助连招变换进攻节奏，打乱对手预判，提高斩杀线！
          </p>
          
          <div class="premium-cta-block">
            <span class="cta-icon">✦</span>
            <span class="cta-text">欢迎各位高高手分享连招吧</span>
            <span class="cta-icon">✦</span>
          </div>
          
          <div class="ugc-combos" v-if="comboContributions.length > 0" style="margin-top: 30px;">
            <h3 style="color: #8E9EAB; border-bottom: 1px dashed var(--border-default); padding-bottom: 10px;">🌟 玩家连招分享</h3>
            <div v-for="item in comboContributions" :key="item.id" class="contribution-card">
              <div class="card-header">
                <div class="user-info">
                  <div class="avatar-placeholder">👤</div>
                  <span class="username">{{ item.author_name || '热心玩家' }}</span>
                  <span class="time" style="margin-left:10px;">{{ new Date(item.created_at).toLocaleDateString() }}</span>
                </div>
                <div class="actions" v-if="userStore.userInfo && userStore.userInfo.id === item.author_id">
                  <el-button size="small" type="primary" plain @click="openDialog(item)">编辑</el-button>
                  <el-button size="small" type="danger" plain @click="handleDelete(item.id)">删除</el-button>
                </div>
              </div>
              <div class="card-content markdown-body" v-html="md.render(item.content)"></div>
            </div>
          </div>
          
          <h2 id="advanced">三、 进阶技巧</h2>
          <div v-if="tutorialData.advanced" class="markdown-body" style="background: transparent; color: inherit; padding: 0;" v-html="md.render(tutorialData.advanced)"></div>
          <template v-else>
            <blockquote>
              “高级玩家与普通玩家的区别在于对时机的把握和身法的运用。”
            </blockquote>
            <p>在熟练掌握基础连招后，你需要学习如何利用身法（如滑步、钩锁）来取消后摇，从而打出更加流畅和难以防范的攻击。</p>
          </template>
          
          <h2 id="matchups">四、 实战应对</h2>
          <div v-if="tutorialData.matchups" class="markdown-body" style="background: transparent; color: inherit; padding: 0;" v-html="md.render(tutorialData.matchups)"></div>
          <template v-else>
            <p>面对不同武器时，你需要采取不同的策略：</p>
            <ul>
              <li><strong>对战长剑：</strong> 注意其剑气的释放时机，多利用滑步躲避。</li>
              <li><strong>对战阔刀：</strong> 阔刀拥有磐石架势，不要盲目攻击，可以尝试使用蓄力骗对方出招。</li>
            </ul>
          </template>
          <div class="ugc-insights" v-if="insightContributions.length > 0" style="margin-top: 30px;">
            <h3 style="color: #8E9EAB; border-bottom: 1px dashed var(--border-default); padding-bottom: 10px;">💡 玩家实战感悟</h3>
            <div v-for="item in insightContributions" :key="item.id" class="contribution-card">
              <div class="card-header">
                <div class="user-info">
                  <div class="avatar-placeholder">👤</div>
                  <span class="username">{{ item.author_name || '热心玩家' }}</span>
                  <span class="time" style="margin-left:10px;">{{ new Date(item.created_at).toLocaleDateString() }}</span>
                </div>
                <div class="actions" v-if="userStore.userInfo && userStore.userInfo.id === item.author_id">
                  <el-button size="small" type="primary" plain @click="openDialog(item)">编辑</el-button>
                  <el-button size="small" type="danger" plain @click="handleDelete(item.id)">删除</el-button>
                </div>
              </div>
              <div class="card-content markdown-body" v-html="md.render(item.content)"></div>
            </div>
          </div>

        </div>
      </div>
    </div>

    <!-- 发布心得弹窗 -->
    <el-dialog v-model="dialogVisible" :title="isEditing ? '修改教学内容' : '发布我的教学'" width="650px" custom-class="glass-dialog">
      <el-form :model="form" label-width="100px">
        <el-form-item label="分类">
          <el-radio-group v-model="form.category" :disabled="isEditing">
            <el-radio label="combo">连招分享</el-radio>
            <el-radio label="insight">实战感悟</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <template v-if="form.category === 'combo' && !isEditing">
          <el-form-item label="连招名称" required>
            <el-input v-model="form.comboName" placeholder="例如：太刀民工连" />
          </el-form-item>
          <el-form-item label="具体连招" required>
            <el-input v-model="form.comboDetails" type="textarea" :rows="3" placeholder="例如：左键 -> 右键蓄力 -> 升龙..." />
          </el-form-item>
          <el-form-item label="注意点">
            <el-input v-model="form.comboNotes" type="textarea" :rows="2" placeholder="这套连招容易被什么克制？起手需要注意什么？" />
          </el-form-item>
          <el-form-item label="教学视频" style="margin-bottom: 10px;">
            <el-input v-model="form.videoUrl" placeholder="选填，输入B站或抖音链接..." />
          </el-form-item>
          <el-form-item label="视频作者ID" v-if="form.videoUrl" style="margin-bottom: 20px;">
            <el-input v-model="form.videoAuthorId" placeholder="选填，输入短视频作者ID..." />
          </el-form-item>
        </template>
        <template v-else>
          <el-form-item label="内容" required>
            <el-input v-model="form.content" type="textarea" :rows="10" placeholder="请在这里输入...（支持 Markdown 格式）" />
          </el-form-item>
        </template>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm" :loading="submitting">{{ isEditing ? '保存修改' : '发布' }}</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getContributions, createContribution, updateContribution, deleteContribution } from '@/api/tutorials'
import { useUserStore } from '@/stores/user'
import { ElMessage, ElMessageBox } from 'element-plus'
import MarkdownIt from 'markdown-it'
const md = new MarkdownIt({ html: true, breaks: true, linkify: true })

const route = useRoute()
const router = useRouter()


const allWeapons = [
  { id: 'changjian', name: '长剑' },
  { id: 'taidao', name: '太刀' },
  { id: 'kuodao', name: '阔刀' },
  { id: 'zhanmadao', name: '斩马刀' },
  { id: 'changqiang', name: '长枪' },
  { id: 'gun', name: '棍' },
  { id: 'bishou', name: '匕首' },
  { id: 'shanzi', name: '扇子' },
  { id: 'shuangdao', name: '双刀' },
  { id: 'shuangji', name: '双戟' },
  { id: 'shuangjiegun', name: '双节棍' },
  { id: 'hengdao', name: '横刀' },
  { id: 'quanren', name: '拳刃' },
  { id: 'lianjian', name: '链剑' },
  { id: 'feidao', name: '飞刀' }
]

const currentWeaponId = ref('')

const defaultData = {
  title: '近战武器进阶教学',
  subtitle: '掌握核心技巧，制霸聚窟洲',
  author: '劫学院导师',
  date: '2026-06-05',
  difficulty: 3,
  intro: '本教程将带你深入了解这把武器的核心机制，助你在实战中游刃有余。',
  image: 'https://images.unsplash.com/photo-1589149098258-3e9102cd63d3?q=80&w=1200&auto=format&fit=crop'
}

const tutorialData = ref({ ...defaultData })

const updateData = (id) => {
  currentWeaponId.value = id
  window.scrollTo({ top: 0, behavior: 'smooth' })
  
if (id === 'changjian') {
    tutorialData.value = {
      title: '长剑进阶教学：深度解析',
      subtitle: '掌握核心技巧，制霸聚窟洲',
      author: '劫学院首席导师',
      date: '2026-06-05',
      difficulty: 4,
      intro: '长剑在《永劫无间》中被誉为“百兵之君”，是一把兼具机动性、灵活性与拉扯能力的轻型近战武器。它拥有独特的剑气机制，蓄力攻击能够释放出中远距离的剑气波，这使得长剑在拉扯和消耗战中占据绝对优势。虽然其单次普攻伤害不如阔刀和斩马刀，但凭借极快的出招速度、优秀的平A粘人能力以及独特的剑气压制，长剑成为了许多顶尖高手的上分利器，非常适合喜欢身法博弈和中距离拉扯的玩家。',
      advanced: '长剑的核心在于“距离把控”与“剑气博弈”，想要进阶成为长剑高手，必须掌握以下几点核心技巧：\n\n**1. 剑气距离的极限把控**\n长剑的右键/左键蓄力剑气有着相当优秀的攻击距离。进阶玩家绝不会在贴脸时轻易释放剑气，因为那极易被对手振刀。最佳的剑气释放距离是“刚好处于对手普攻范围之外，但剑气又能精确命中的中距离”。在这个距离下，即便对手成功振刀，反弹的剑气也有极大概率无法命中你，而你却可以通过滑步闪避轻松化解，从而立于不败之地。\n\n**2. 蓄力转振刀与骗振博弈**\n因为长剑剑气极易被针对，所以“骗振”是必修课。当你蓄力看到对手身上冒出红光准备振刀时，可以选择“蓄力转振刀”（蓄力中直接按振刀键），或者使用“C”（下蹲）或“Shift”（闪避）打断蓄力，随后接上左键普攻抓对手的振刀后摇。最高端的长剑玩家，往往整场战斗释放的剑气屈指可数，全靠蓄力威慑来骗取对手的失误。\n\n**3. BS（滑步）身法的结合**\n长剑的平A动作轻灵，配合闪避（Shift）可以打出非常流畅的“A-Shift-A”追击连段。在实战中，利用短闪避重置普攻后摇，不仅能持续黏住试图后撤的敌人，还能在攻击间隔中随时观察对方的动作，保持自身的灵活性。掌握“太极步”般的灵动身法，是长剑玩家跨越瓶颈的关键。',
      matchups: '**1. 面对重型武器（阔刀、斩马刀）**\n重型武器拥有霸体磐石机制，长剑的普攻极易触发对方的磐石。因此，打阔刀时切忌无脑平A。应对策略是：保持中远距离，利用右键蓄力剑气进行消耗。如果不得不近身，多使用“蓄力骗磐石”的技巧。当你蓄力时，阔刀大概率也会蓄力磐石，此时你可以利用闪避拉开身位，或者抓住其蓄力释放的瞬间进行振刀。一定要发挥长剑的机动性优势，不和重型武器拼刀，贯彻“敌进我退，敌退我剑气”的方针。\n\n**2. 面对高机动武器（匕首、太刀）**\n太刀和匕首的近战贴身爆发极高，且拥有优秀的突进能力。面对太刀时，要注意其百裂斩的释放时机，长剑的剑气起手略慢，容易被太刀的滑步普攻打断，因此要注重普攻的拼刀和后撤步的运用。面对匕首的“闪步”机制，长剑不要轻易交出蓄力，因为匕首闪步自带无敌帧且能迅速反打。最佳策略是利用普通攻击去卡匕首的闪步落点，或者在预判到对方要金霸体突进时，提前拉开距离并准备振刀。\n\n**3. 长剑内战**\n长剑内战是极其考验基本功的“太极推手”。双方都在互相试探对方的剑气与振刀时机。内战的要点在于“后发制人”。不要轻易第一个释放剑气，多用蓄力转闪避去骗出对方的剑气，然后利用自己手里捏着的蓄力抓对方的后摇。此外，精确的“振剑气”基本功也是内战的分水岭，如果你能做到百分百看清并振掉对手的中距离剑气，那么内战就已经赢了一半。'
    } } else if (id === 'taidao') {
    tutorialData.value = {
      title: '太刀进阶教学：深度解析',
      subtitle: '掌握核心技巧，制霸聚窟洲',
      author: '劫学院首席导师',
      date: '2026-06-05',
      difficulty: 4,
      intro: '太刀是《永劫无间》中最具操作感和连招美感的近战武器，以其极快的攻击频率、极其灵活的滑步机制和爆发极高的“百裂斩”闻名。它拥有全武器中最优秀的近身压制力和抓破绽能力，能够在瞬间打出高额伤害。太刀的精髓在于灵动飘逸，非常适合喜欢贴身肉搏、追求极致身法与连招连贯性的玩家，是公认的“上限极高”的兵器。',
      advanced: '太刀的核心在于“黏人”与“百裂斩的命中”，想要进阶成为太刀高手，必须掌握以下几点核心技巧：\n\n**1. 百裂斩的蓄力博弈与惊雷一闪**\n太刀的灵魂技能是蓄力释放的“百裂斩”。进阶玩家绝不会轻易将百裂斩完全释放，因为它的前摇动作极其明显，极易被对手振刀。最佳策略是利用“滑步蓄力”保持压迫感，当对手忍不住捏蓝或者后撤时，再释放百裂斩。百裂斩命中后，可以接左键或右键释放“惊雷一闪”进行追击，这是一套爆发极高的连段。学会利用下蹲（C）或闪避（Shift）打断蓄力来骗出对手的振刀，是太刀的必修课。\n\n**2. 滑步（Shift）与普攻的无缝衔接**\n太刀拥有全游戏最优秀的滑步普攻动作。利用短闪避（Shift）重置普攻的后摇，可以打出如狂风骤雨般的连续攻击。在实战中，“左键-短闪-左键”或者“右键-短闪-右键”的循环能够牢牢地黏住试图逃跑的敌人。在滑步的过程中，你随时可以根据对手的反应选择继续普攻、开始蓄力或者是转为振刀。这种进退自如的机动性是太刀最大的优势。\n\n**3. 升龙连招的极致应用**\n太刀拥有非常稳定且伤害可观的升龙连招（C+右键）。在普攻命中造成对手硬直后，迅速接上升龙，在空中可以接普通攻击，落地后再接蓄力压起身。熟练掌握太刀的浮空连段，可以将一次普通的普攻命中转化为巨大的血量优势。顶尖太刀玩家的连招就如同行云流水，让对手一旦露出破绽就难以落地。',
      matchups: '**1. 面对长武器（长枪、长剑）**\n长枪和长剑的攻击距离远胜于太刀。在面对它们时，太刀切忌直线冲锋，这会被长武器的普攻或剑气轻松拦截。应对策略是：利用太刀的滑步优势进行侧向移动（S型走位），寻找对方攻击的后摇间隙切入。一旦成功近身，就要利用太刀极快的普攻频率进行压制，不给对手拉开距离喘息的机会。面对长剑的剑气，利用短闪避的无敌帧躲避并迅速拉近身位是关键。\n\n**2. 面对重型武器（阔刀、斩马刀）**\n阔刀和斩马刀的磐石机制是太刀普攻的克星。如果太刀无脑平A，极易触发对方的磐石并遭到毁灭性的反击。打重武器时，必须学会“点到为止”。普攻一下立刻滑步拉开，或者使用蓄力去逼迫对方也进入蓄力状态，然后进行振刀博弈。利用太刀灵活的身法去“骗”阔刀出招，抓住其笨重缓慢的攻击后摇进行输出，切忌站桩对砍。\n\n**3. 太刀内战**\n太刀内战是纯粹的反应与身法比拼，也被称为“滑步大赏”。内战的核心在于谁能先手抓到对方的普攻后摇。不要随意使用升龙或百裂斩，因为一旦被躲开，你将面临致命的连招。多使用短闪避和右键普攻进行试探，利用太刀的“惊雷一闪”进行远距离抓人。内战中，谁的耐心更好、谁的骗振技巧更逼真，谁就能掌握主动权。'
    } } else if (id === 'kuodao') {
    tutorialData.value = {
      title: '阔刀进阶教学：深度解析',
      subtitle: '掌握核心技巧，制霸聚窟洲',
      author: '劫学院首席导师',
      date: '2026-06-05',
      difficulty: 4,
      intro: '阔刀在《永劫无间》中是霸道与力量的代名词，作为重型近战武器，它拥有全游戏最顶级的单次爆发伤害。其独有的“磐石架势”机制，使得阔刀在与敌人拼刀时能够吸收伤害并迅速转化为极具毁灭性的反击。阔刀的攻击范围广、压制力强，非常适合喜欢刚猛打法、善于心理博弈以及在团战中承担伤害和收割残局的玩家。',
      advanced: '阔刀的核心在于“磐石博弈”与“反击节奏”，想要进阶成为阔刀高手，必须掌握以下几点核心技巧：\n\n**1. 磐石架势的精妙运用**\n阔刀的精髓全在“磐石”二字。当你的普攻或蓄力与敌人的攻击相撞时，阔刀不会被打断，而是会进入“磐石架势”抵挡伤害。进阶玩家绝不会盲目出刀，而是利用磐石去接敌人的普攻。在触发磐石后，你可以选择立刻释放左键或右键打出伤害极高的反击，也可以选择按住蓄力键继续蓄力，甚至在磐石后瞬间转为闪避或振刀。掌握磐石后的多变变招，让对手无法猜测你的下一步动作，是阔刀的核心。\n\n**2. 蓄力步伐与压迫感**\n阔刀的蓄力可以在移动中进行（蓄力滑步），并且阔刀的右键满蓄力（雷霆之怒）拥有极其恐怖的伤害和范围。在实战中，阔刀玩家经常会捏着右键蓄力向敌人缓慢逼近。这种“捏蓝”的压迫感会让对手产生极大的心理压力，迫使对手交出闪避或者试图振刀。一旦对手乱了阵脚，阔刀就可以释放蓄力一击致命，或者在对手试图振刀时利用下蹲取消蓄力，反抓对手破绽。\n\n**3. 升龙与左键的节奏把控**\n虽然阔刀显得笨重，但它同样拥有实用的连招。阔刀的左键普攻范围非常大，第二段左键带有蓝霸体，可以有效压制喜欢滑步的敌人。此外，阔刀的升龙（C+右键）判定非常强，在团战中或者拼刀间隙打出升龙，不仅能控制敌人，还能为队友创造极佳的输出环境。进阶玩家会精准把握左键普攻的节奏，利用出其不意的升龙打断对手的节奏。',
      matchups: '**1. 面对轻型武器（太刀、长剑、匕首）**\n轻型武器以快打慢，非常喜欢利用滑步和高频普攻来消耗阔刀。面对他们，阔刀最强大的武器就是磐石。你可以主动出击，利用普攻去“撞”他们的普攻触发磐石。一旦触发磐石，千万不要每次都秒放反击，因为高端太刀或匕首玩家在普攻后会立刻接振刀。你可以多尝试磐石后按住蓄力，等对方振刀动作结束后再释放，或者磐石后直接向后闪避拉开距离，重新寻找蓄力压制的机会。\n\n**2. 面对长枪与斩马刀**\n长枪的“龙王破”和斩马刀的“刃马连刃”对阔刀威胁极大。面对长枪时，要注意其精准的远距离戳刺，尽量利用地形掩体或者阔刀的大范围横劈（左键）来封堵长枪的走位。由于阔刀的磐石会被长枪的哪吒闹海多次判定打破，所以拼刀时要格外谨慎。面对斩马刀时，双方都有磐石机制，这往往会演变成“磐石对对碰”。在重武器内战中，谁先忍不住释放磐石反击，谁就容易被对方振刀。多用蹲伏或闪避取消磐石，比拼心理素质。\n\n**3. 阔刀内战**\n阔刀内战是纯粹的“心理博弈战”。双方对拼左键会无限触发磐石（叮叮当当的打铁声）。在内战中，千万不要无脑狂点鼠标左键，因为一旦对方突然停手并按出振刀，你就会被振得满盘皆输。内战的诀窍在于“破局”：在连续磐石两到三次后，突然利用闪避（Shift）拉开身位打断拼刀节奏，然后趁对方还在习惯性点击鼠标时，打出蓄力或者升龙。冷静的头脑是阔刀内战获胜的唯一法则。'
    } } else if (id === 'zhanmadao') {
    tutorialData.value = {
      title: '斩马刀进阶教学：深度解析',
      subtitle: '掌握核心技巧，制霸聚窟洲',
      author: '劫学院首席导师',
      date: '2026-06-05',
      difficulty: 4,
      intro: '斩马刀作为重型武器中的“长兵器”，融合了阔刀的霸道与长枪的攻击距离。它保留了阔刀引以为傲的“磐石架势”，同时引入了独特的乘骑姿态（刃马连刃）。斩马刀的攻击范围极广，尤其在追击和团战中能够发挥巨大的破坏力。相比于阔刀，它的打法更加灵活多变，既能像重武器一样硬碰硬，又能利用独特的位移机制进行拉扯，是兼顾了力量与技巧的强力兵器。',
      advanced: '斩马刀的核心在于“刃马连刃的运用”与“中距离拉扯”，进阶成为斩马刀高手需要掌握以下技巧：\n\n**1. 刃马连刃（乘马）的精准释放**\n斩马刀右键蓄力满段后可以进入“刃马连刃”状态（犹如骑在战马上冲锋）。这个状态下不仅拥有极快的移动速度，还具有极强的霸体和高频的连续伤害。进阶玩家会利用这个技能在团战中进行高效的切割战场，或者在单挑时利用其超远的位移距离追击残血敌人。需要注意的是，刃马连刃虽然强，但依然可以被振刀，因此在冲锋时要时刻观察敌方的动作，学会利用跳跃或闪避提前取消冲锋状态，骗出敌方的振刀。\n\n**2. 磐石与长柄优势的结合**\n斩马刀同样拥有磐石机制，但其优势在于攻击距离更长。在实战中，你可以利用斩马刀的长柄优势，在较远的距离用左键去“摸”对手，即便被对方的攻击判定到，也能安全地进入磐石架势。触发磐石后，斩马刀的磐石反击范围非常大，能够轻易命中试图侧向滑步的敌人。学会利用距离优势白嫖磐石，是斩马刀玩家的必修课。\n\n**3. 柄击与控制连招**\n斩马刀在蓄力状态下，利用下蹲或跳跃取消蓄力后，接上普攻可以打出出其不意的“柄击”。柄击虽然伤害不高，但出招极快且带有强硬直效果，非常适合用来打断敌方的节奏或作为连招的起手。在柄击命中后，可以迅速接上升龙（C+右键）将敌人挑飞，从而打出一套完整的浮空连段，弥补了重型武器在精细连招上的不足。',
      matchups: '**1. 面对高频轻武器（太刀、双刀）**\n双刀和太刀这类高频武器非常喜欢近身缠斗。斩马刀应对他们的最佳策略是保持距离，利用右键长蓄力的威慑力限制对方的走位。如果对方强行近身，果断利用磐石机制去接对方的普攻。由于斩马刀的磐石反击判定范围极大，轻武器很难通过简单的滑步躲开。但要注意对方蓄力转振刀的技巧，在磐石触发后，可以多捏一会儿蓄力，或者直接转刃马连刃强行拉开距离。\n\n**2. 面对长武器（长剑、长枪）**\n斩马刀在面对长枪时，距离优势不复存在。长枪的哪吒闹海能够克制磐石，因此拼刀时需谨慎。尽量利用左键的宽广横扫范围去压制长枪的直线戳刺。面对长剑时，要小心对方的剑气消耗。斩马刀的刃马连刃可以很好地越过剑气的攻击范围迅速近身，但在冲锋时要注意长剑可能会直接原地振刀。此时可以在冲锋到一半时利用跳跃取消，落地直接普攻抓破绽。\n\n**3. 斩马刀与阔刀的重装对决**\n斩马刀打阔刀，可以说是“长斧打短锤”。斩马刀一定要发挥自己攻击距离更远、机动性更强的优势。尽量避免与阔刀在狭小的地形站桩互拼磐石。你可以利用刃马连刃进行拉扯消耗，打完一套就跑。如果被迫拼刀触发磐石，斩马刀可以利用磐石后的闪避迅速拉开距离，然后再利用长柄的普攻去白嫖阔刀。记住，不要和阔刀比爆发，要比拉扯。'
    } } else if (id === 'changqiang') {
    tutorialData.value = {
      title: '长枪进阶教学：深度解析',
      subtitle: '掌握核心技巧，制霸聚窟洲',
      author: '劫学院首席导师',
      date: '2026-06-05',
      difficulty: 4,
      intro: '长枪在《永劫无间》中被称为“百兵之王”，以其极其优异的攻击距离和令人防不胜防的“哪吒闹海”闻名。作为一把长柄近战武器，长枪的普攻范围远超太刀和长剑，能够在安全的距离对敌人进行牵制。其招牌的“龙王破”与“哪吒闹海”连段不仅拥有极高的伤害，还附带长时间的金霸体控制效果，是团战绞肉和单挑博弈的顶级兵器。',
      advanced: '长枪的核心在于“枪尖的距离把控”与“龙王破的精准释放”，进阶长枪高手必须掌握以下技巧：\n\n**1. 卡精准距离的“戳刺”**\n长枪的左键普攻是直线戳刺，虽然横向判定较窄，但纵向距离极远。进阶玩家会完美把控这个“极限距离”，在这个距离上，你的枪尖能打到对手，而对手的太刀或匕首完全够不到你。利用滑步配合左键（滑步A），不断地在安全距离骚扰和削减对手的血量，让对手在无法还手的情况下陷入急躁，是长枪的基础必修课。\n\n**2. 龙王破与哪吒闹海的博弈**\n长枪左键或右键蓄力到第二段的瞬间释放，会触发突进技能“龙王破”，命中后狂点左键即可触发“哪吒闹海”（大范围金霸体挥舞）。但这个绝招前摇明显，极易被振刀。进阶玩家绝不会轻易打出龙王破，而是利用“捏蓝”给对手压力，当对手试图振刀时，下蹲取消蓄力并接升龙。或者故意蓄力过头（放弃龙王破判定），打出普通的重击来骗取对手的振刀。\n\n**3. 双环漏与大风车的运用**\n除了龙王破，长枪的普攻连段中还隐藏着“双环漏”这样的技巧。长枪的普攻第三段是蓝霸体的大风车，很多玩家习惯性去振长枪的第三段。进阶玩家会在普攻两段后，故意停顿一下（利用闪避或下蹲重置），然后再打出普攻，或者直接转为蓄力。打破常规的攻击节奏，让对手的振刀彻底失效，是长枪压制力的体现。',
      matchups: '**1. 面对短兵器（匕首、太刀）**\n长枪打短兵器拥有天然的“手长”优势。面对太刀和匕首，最核心的原则就是“保持距离，禁止贴贴”。利用长枪的左键戳刺去卡对面的身位。如果被匕首闪步或者太刀滑步贴身，不要慌张，可以利用长枪优秀的右键横扫（范围广）去拦截对方的身法，或者直接向后闪避拉开距离。切忌在被贴身时强行蓄力龙王破，那等同于给对方送振刀。\n\n**2. 面对重武器（阔刀、斩马刀）**\n重武器的磐石机制非常克制普攻。但长枪有一把绝佳的钥匙——“哪吒闹海”。哪吒闹海的多段金霸体攻击能够直接瓦解重武器的磐石架势。因此，打阔刀时，要想方设法利用龙王破起手。你可以利用地形掩体卡视角蓄力，或者在阔刀蓄力释放的后摇间隙打出龙王破。如果未能触发哪吒闹海，千万不要和阔刀拼平A，立刻滑步后撤寻找下一次机会。\n\n**3. 长枪内战**\n长枪内战是一场“刺客之间的对决”，谁先露出破绽谁就输。内战中，双方都在卡左键的极限距离，试图白嫖对方的血量。内战的要点在于对“龙王破”时机的预判。如果对方喜欢捏蓝，你可以勇敢地贴身去振刀；如果对方喜欢滑步平A，你就利用右键的横扫去抓他的滑步落点。在长枪内战中，谁的耐心更好、谁能更精准地把握那“一寸长”的优势，谁就能笑到最后。'
    } } else if (id === 'gun') {
    tutorialData.value = {
      title: '棍进阶教学：深度解析',
      subtitle: '掌握核心技巧，制霸聚窟洲',
      author: '劫学院首席导师',
      date: '2026-06-05',
      difficulty: 4,
      intro: '棍在《永劫无间》中是一把极具特色的长柄武器，号称“百兵之首”。与长枪的直线戳刺不同，棍的攻击动作大开大合，以横扫和范围打击为主。它独有的“定海神针”和“乱点天宫”连段赋予了棍极强的团战控制能力和华丽的视觉表现。棍的普攻范围非常大，尤其适合在复杂的团战中进行AOE输出和拆火，是一把兼顾了防守反击与群攻压制的强力兵器。',
      advanced: '棍的核心在于“精准的变招”与“乱点天宫的释放时机”，想要玩好这把武器，必须掌握以下技巧：\n\n**1. 蓄力步伐与破空式**\n棍的蓄力不仅可以在移动中进行，而且满蓄力释放的“破空式”拥有极其夸张的攻击范围。进阶玩家经常利用蓄力滑步来逼近敌人，利用破空式的超大范围去压制喜欢到处乱跳的敌人（如匕首、太刀玩家）。即便对手试图闪避，也很难逃出破空式的笼罩范围。学会利用破空式去卡对手的身位，是棍的入门必修。\n\n**2. 精准转“乱点天宫”的博弈**\n棍的灵魂绝技是“乱点天宫”。触发方式是在第二段普攻或特定连段后，抓准金光闪烁的瞬间点击普攻。这个技能不仅带有极强的吸附效果，还能在空中打出爆炸伤害并免疫部分控制。然而，由于前摇较为固定，对手很容易预判振刀。因此，进阶玩家会故意“断节奏”，比如第一段普攻后突然下蹲取消，或者在可以触发乱点天宫的瞬间转为滑步，骗出对手的振刀后再进行抓取。\n\n**3. 升龙连招的灵活性**\n棍的升龙（C+右键）判定非常广。在普攻命中敌人后，迅速接上升龙可以将敌人高高挑起。棍的浮空连段相对简单且稳定，在空中可以接多次普攻，落地后再利用长柄的优势压对方的起身。熟练掌握这套连招，可以让你在单挑中不虚任何短兵器。',
      matchups: '**1. 面对短兵器（匕首、双刀）**\n短兵器的核心是贴身爆发，而棍的核心是范围控制。面对短兵器时，一定要发挥棍的“手长”和“面广”的优势。多使用左键或右键的横扫去限制对方的身法。如果对方试图强行滑步贴脸，直接开启破空式蓄力，巨大的攻击范围能让他们有来无回。切忌在被贴脸后慌乱出刀，利用闪避拉开距离，重新回到棍的舒适攻击半径才是王道。\n\n**2. 面对重武器（阔刀、斩马刀）**\n重武器的磐石机制依然是所有轻中型武器的梦魇。但棍有一个得天独厚的优势——多段判定的乱点天宫。乱点天宫的金霸体多段攻击可以直接瓦解阔刀的磐石。因此，在打重武器时，要想方设法安全地打出乱点天宫。你可以利用右键蓄力的距离优势去试探，一旦骗出对方的磐石反击并躲过，立刻抓住其后摇强行启动乱点天宫。\n\n**3. 棍内战**\n棍的内战是一场“大风车”的对决。由于双方的攻击范围都很大，很容易出现互相“刮痧”的局面。内战的核心在于对“乱点天宫”释放时机的把握。谁能更稳地按出金光判定的乱点天宫，谁就能掌握主动权。此外，内战中多使用蓄力转振刀的技巧，因为大家都会下意识地去蓄力破空式，抓准时机振掉对方的满蓄力，是破局的关键。'
    } } else if (id === 'bishou') {
    tutorialData.value = {
      title: '匕首进阶教学：深度解析',
      subtitle: '掌握核心技巧，制霸聚窟洲',
      author: '劫学院首席导师',
      date: '2026-06-05',
      difficulty: 4,
      intro: '匕首是《永劫无间》中机动性最高、最灵动的刺客型近战武器。它独创了“闪步”机制，在攻击后进行闪避可以触发带有无敌帧的金霸体滑步，这让匕首拥有了极其恐怖的拉扯能力和反打能力。虽然匕首的攻击距离极短，但凭借鬼魅般的身法和极快的出手速度，它成为了高端局中让许多玩家头疼的“狗皮膏药”。如果你喜欢极限操作和刀尖起舞的感觉，匕首绝对是你的不二之选。',
      advanced: '匕首的核心完全建立在“闪步”之上，没有闪步的匕首就是一堆废铁。进阶必须掌握以下技巧：\n\n**1. 闪步的无缝衔接与“鬼影迷踪”**\n匕首在任何普攻之后按下闪避键（Shift）都会触发独特的“闪步”。闪步自带一小段无敌帧，并且是以金霸体状态位移，这使得匕首可以无视绝大多数的普通攻击。进阶玩家会将“普攻-闪步-普攻-闪步”练成本能，在实战中就像泥鳅一样让对手根本抓不到落点。熟练掌握闪步的方向控制，可以瞬间绕到敌人背后打出致命的“背刺”效果。\n\n**2. 荆轲献匕与鬼刃暗扎的博弈**\n匕首在闪步之后如果立刻接左键，会触发“荆轲献匕”（快速突进直刺），接右键则是蓄力攻击“鬼刃暗扎”。荆轲献匕是匕首追击和抢先手的重要手段，但容易被对方预判振刀。因此，进阶玩家会利用闪步后的短暂停顿来观察对手反应：如果对手试图振刀，就稍微延迟出刀或者转为鬼刃暗扎蓄力；如果对手后撤，则果断荆轲献匕追击。\n\n**3. 升龙连招的滞空压制**\n匕首的升龙连招是全武器中最华丽且伤害最高的之一。利用普攻或荆轲献匕打出硬直后，迅速接上升龙。匕首在空中的连击段数很多，并且可以配合钩锁打出极其复杂的浮空无限连段（俗称“百裂匕”）。掌握这套高难度的连段，是匕首玩家区别于普通玩家的标志。',
      matchups: '**1. 面对长武器（长枪、斩马刀、棍）**\n长武器是匕首的天敌，对方往往会在安全距离外用普攻或蓄力卡你的走位，让你根本无法近身。应对策略是：绝不能直线使用荆轲献匕冲锋，必须利用闪步的无敌帧，以“Z字形”或侧向绕圈的方式逐渐逼近。你可以故意空挥一刀然后接闪步，利用闪步的金霸体硬顶着长武器的普攻强行切入内圈。一旦成功贴身，匕首的超快攻速就会让长武器毫无还手之力。\n\n**2. 面对重型武器（阔刀）**\n阔刀的磐石机制对匕首威胁极大，因为匕首的连击频率太高，很容易帮阔刀叠满磐石。应对阔刀的秘诀在于“骗”与“绕后”。多使用单次普攻去试探阔刀，触发磐石后立刻使用闪步拉开或者直接闪步绕到阔刀的身后。阔刀的磐石反击虽然范围大，但转向较为笨拙，利用闪步的灵活性将阔刀玩弄于股掌之间。\n\n**3. 匕首内战**\n匕首内战被称为“猴戏”。双方都在疯狂地闪步，画面极度混乱。内战的核心在于“抓落点”和“比拼耐心”。不要试图用荆轲献匕去硬顶对方的闪步，因为闪步是金霸体，你会吃亏。多用右键蓄力（鬼刃暗扎）去等待对方闪步结束的后摇，或者在预判到对方要使用荆轲献匕时果断振刀。在内战中，谁先按捺不住频繁出刀，谁就会暴露出破绽。'
    } } else if (id === 'shanzi') {
    tutorialData.value = {
      title: '扇子进阶教学：深度解析',
      subtitle: '掌握核心技巧，制霸聚窟洲',
      author: '劫学院首席导师',
      date: '2026-06-05',
      difficulty: 4,
      intro: '扇子是《永劫无间》中极具东方美学的轻型武器。它与匕首同源，但在招式上融入了柔美的舞姿与凌厉的旋风。扇子不仅拥有类似匕首的灵活闪步机制，还具备独特的“扇风”机制（左键蓄力可以释放远程风压）。这种可远可近、刚柔并济的特性，使得扇子在单挑博弈中拥有极其多变的套路，是一把将优雅与致命完美结合的武器，深受身法型玩家的喜爱。',
      advanced: '扇子的核心在于“远近结合”与“闪步变招”，进阶高手必须掌握以下技巧：\n\n**1. 蓄力风压的远程牵制**\n扇子的左键蓄力能够打出一道沿直线飞行的风压，这使得它成为了轻武器中罕见的具备远程消耗能力的兵器。进阶玩家会在接战前，利用滑步蓄力不断释放风压来试探对手和削减血量。风压的存在让对手不得不频繁闪避或试图振刀，从而打乱对方的节奏。更重要的是，风压可以用来打断对手的打药、修树或者救援动作，战略意义极大。\n\n**2. 闪步与“扇舞”的无缝衔接**\n扇子同样继承了匕首的“攻击后接闪避触发金霸体闪步”的机制。但扇子在闪步后的反击动作（扇舞）范围更广，且带有优雅的旋转判定。在实战中，利用普攻-闪步-普攻的循环可以牢牢黏住对手。与匕首的直刺不同，扇子的闪步反击更适合用来应对试图侧向绕后的敌人。利用闪步的无敌帧躲避关键伤害，然后利用扇舞的大范围判定进行反打，是扇子的核心博弈手段。\n\n**3. 独特的浮空控制与连招**\n扇子的升龙（C+右键）有着非常独特的动作模组，能够将敌人击飞并在空中造成多段打击。配合扇子的专属魂玉，甚至可以在空中实现长时间的滞空压制。进阶玩家会在普攻抓到破绽后，迅速接上升龙，并在空中穿插左键普攻和右键下劈，落地后再迅速接上一个左键蓄力风压压起身，形成一套伤害拉满且极具观赏性的完美连段。',
      matchups: '**1. 面对重型武器（阔刀、斩马刀）**\n扇子打重武器的核心思路是“风筝”。千万不要试图用扇子去和阔刀拼平A，那无异于以卵击石。充分利用左键蓄力风压的远程优势，在安全的距离不断消耗阔刀的血量。如果阔刀试图逼近，就利用闪步的高机动性向侧后方拉扯。只有在明确骗出了阔刀的磐石反击，或者阔刀蓄力释放处于后摇硬直时，才利用闪步突进打一套升龙连招，打完立刻再次拉开距离。\n\n**2. 面对突进型轻武器（太刀、双刀）**\n太刀和双刀非常喜欢利用高移速强行近身。面对这类武器，扇子的风压威慑力尤为重要。你可以故意捏着左键蓄力，迫使对方不敢轻易滑步向前。如果对方强行突脸，利用闪步的金霸体去顶掉对方的第一波普攻伤害，然后迅速转为扇舞反击。在与这类武器近身缠斗时，胜负往往取决于谁的闪步时机抓得更准，谁能更早地利用升龙把对方挑飞。\n\n**3. 扇子内战（及与匕首的对决）**\n扇子内战或打匕首时，画面往往是双方在互相闪步。由于大家都有金霸体闪步，普攻很难直接打出硬直。内战的关键在于“预判对方的闪步落点”。不要盲目出刀，可以多尝试在对方闪步刚结束的瞬间，利用风压进行精准打击。或者在近身博弈中，多使用下蹲取消普攻的技巧，骗出对方的闪步反击，然后抓其后摇进行输出。谁更冷静，谁就能赢下这场“舞者”的对决。'
    } } else if (id === 'shuangdao') {
    tutorialData.value = {
      title: '双刀进阶教学：深度解析',
      subtitle: '掌握核心技巧，制霸聚窟洲',
      author: '劫学院首席导师',
      date: '2026-06-05',
      difficulty: 4,
      intro: '双刀在《永劫无间》中是“高频输出”与“连绵不绝”的代名词。作为双持武器，它拥有全游戏最密集的攻击频率和极快的移动速度。双刀的招式如暴风骤雨，一旦让其近身并抓到破绽，它能在极短的时间内打出令人窒息的连续伤害。其独有的“剪水”和“惊鸿步”机制，赋予了双刀极强的追击和粘人能力，非常适合喜欢极致进攻、以快打慢的狂热型玩家。',
      advanced: '双刀的核心在于“极致的贴身压制”与“高频普攻的节奏变幻”，进阶成为双刀高手必须掌握以下技巧：\n\n**1. 普攻的高频压制与变招**\n双刀的左键和右键普攻段数极多，且出招极快。进阶玩家不会死板地把一套普攻打完，因为双刀的最后一段普攻通常是蓝霸体，极易被对手振刀。最佳策略是利用“A-A-闪避-A-A”或者“A-A-下蹲-A-A”的循环，通过取消攻击后摇，将普攻无限衔接下去。这种高频且无间断的攻击会让对手陷入极大的心理恐慌，迫使对方胡乱交出闪避或尝试盲目振刀，从而暴露出巨大的破绽。\n\n**2. 右键蓄力的追击与博弈**\n双刀的右键满蓄力拥有极远的突进距离，是追击残血和开团起手的神技。但其冲刺动作较长，如果对手有防备，非常容易被振刀。进阶玩家会利用滑步保持蓄力状态（捏蓝），像幽灵一样在对手周围游荡。通过故意向对手侧边或者身后的空地释放蓄力，来骗取对手的振刀动作，然后利用双刀的高机动性迅速折返回来，接上普攻或者升龙进行输出。\n\n**3. 浮空连段的伤害最大化**\n双刀的升龙（C+右键）挑飞高度非常适合进行空中连击。在升龙击飞敌人后，双刀可以在空中打出极其华丽的多次交叉斩击（空中左键或右键）。配合特定的魂玉，双刀的空中连招甚至可以将满甲的敌人直接打残。掌握这套浮空连招的时机和按键节奏，是双刀从“刮痧师傅”蜕变为“夺命刺客”的关键步骤。',
      matchups: '**1. 面对长武器（长枪、斩马刀）**\n手短是双刀致命的弱点。面对长枪和斩马刀，绝不能在开阔地带直线冲锋。必须利用地形、树木或者建筑作为掩体，利用双刀的高移速进行迂回。在对方挥空或者释放蓄力后摇的瞬间，利用右键蓄力突进或者滑步迅速贴身。只要一旦进入双刀的攻击半径，就要毫无保留地倾泻所有的普攻连段，用极其密集的攻击压制住长武器的出手空间。\n\n**2. 面对重武器（阔刀）**\n阔刀的磐石机制天克双刀的高频普攻，如果你用双刀对着阔刀一顿乱砍，往往会瞬间暴毙。打阔刀时，双刀必须收起狂暴的进攻欲望，转为“麻雀战术”。利用单次普攻去试探，一旦听到磐石触发的“叮”声，立刻利用短闪避向后或向侧边拉开极远距离。利用双刀机动性高的优势，不断去骗阔刀的反击。当阔刀失去耐心挥空时，再上前打一套小爆发，切忌贪刀。\n\n**3. 双刀内战**\n双刀内战是比拼手速和网速的“绞肉机”战场。双方贴身互砍时，往往是在拼谁的霸体等级更高或者谁的血量更厚。在内战中，脱颖而出的关键在于“防守反击”。不要主动去拼左键，可以尝试利用下蹲（C）规避对方的上段攻击，或者在对方连招的间隙果断释放升龙将其挑飞。谁能先将对手打入浮空状态，谁就能在这场狂风暴雨般的内战中取得绝对的胜利。'
    } } else if (id === 'shuangji') {
    tutorialData.value = {
      title: '双戟进阶教学：深度解析',
      subtitle: '掌握核心技巧，制霸聚窟洲',
      author: '劫学院首席导师',
      date: '2026-06-05',
      difficulty: 4,
      intro: '双戟是《永劫无间》中极其霸道且充满力量感的双持重型武器。它融合了双刀的高频连击特色与阔刀的厚重打击感。双戟的普攻范围适中，但每一击都带有沉闷的破甲感。其标志性的“蛟龙出海”连段（如同直升机般的旋转打击）不仅拥有极强的视觉冲击力，还能在团战中造成极其恐怖的AOE伤害和控制效果。对于喜欢冲锋陷阵、以暴力美学碾压对手的玩家来说，双戟是一把不可多得的神兵。',
      advanced: '双戟的核心在于“霸体压制”与“蛟龙出海的释放时机”，进阶成为双戟高手必须掌握以下技巧：\n\n**1. 普攻的霸体衔接与压制**\n双戟的普攻看似笨重，但其招式之间的衔接非常紧密，且带有较强的硬直效果。进阶玩家会利用双戟左键和右键的交替攻击，打乱对手的振刀节奏。双戟的普攻第三段往往是范围极大的蓝霸体攻击，在实战中，你可以故意放慢前两段普攻的节奏，引诱对手试图反击，然后再用第三段的蓝霸体将其击飞。利用滑步重置普攻，保持持续的压迫感，是双戟的基础。\n\n**2. “蛟龙出海”的恐怖威慑力**\n“蛟龙出海”是双戟的灵魂技能（蓄力释放后的特殊连段）。这个技能一旦成功释放，双戟玩家将化身旋转的绞肉机，对周围敌人造成毁灭性打击且极难被打断。然而，它的前摇动作非常明显。进阶玩家绝不会在面对面时生硬地释放蛟龙出海。最佳策略是在团战混乱时从侧翼或视野盲区切入释放；或者在单挑时，利用“捏蓝”逼迫对手后撤，利用地形拐角卡视野释放，让对手防不胜防。\n\n**3. 蓄力骗振与升龙的反打**\n因为蛟龙出海太过耀眼，所有对手在面对双戟时都会死死捏着振刀键。进阶玩家必须精通“骗振”技巧。在蓄力光芒亮起时，瞬间利用下蹲（C）或跳跃取消蓄力，看着对手傻傻地打出振刀动作，然后你只需走上前去，用一个结实的升龙（C+右键）将其挑飞，接上一套结实的空中连段。双戟的升龙判定非常强硬，是化解对手防御的最佳手段。',
      matchups: '**1. 面对灵活轻武器（匕首、扇子、太刀）**\n轻武器非常喜欢利用高机动性来戏耍双戟这种略显沉重的武器。面对他们，双戟绝不能被牵着鼻子走，到处追着对方砍。你的策略应该是“以静制动”。利用双戟普攻范围较大的优势，封堵对方滑步的落点。当对方试图贴身时，果断捏住蓝霸体蓄力。轻武器在面对双戟的蓝霸体时往往会选择后撤，这时你可以大胆地转为普攻压制，或者利用地形强行释放蛟龙出海进行范围洗礼。\n\n**2. 面对重型兵器（阔刀、斩马刀）**\n这简直是火星撞地球的较量。双戟在面对阔刀的磐石时，千万不要试图用多段普攻去硬刚，那会导致你被磐石反击瞬间融化。打重武器时，一定要多用蓄力攻击去试探。你可以利用双戟蓄力滑步的机动性，去骗出阔刀的磐石。一旦阔刀反击挥空，立刻抓住其巨大的后摇，用升龙将其击飞。在这场重装对决中，谁能更好地控制自己的攻击欲望，谁就能站到最后。\n\n**3. 双戟内战**\n双戟内战是纯粹的绞肉战。双方都在寻找释放蛟龙出海的机会。内战的核心原则是：“谁先转起来，谁就赢了一半”。但在高端局内战中，大家往往都在互相骗振。多使用左键第一段普攻进行试探，如果命中，立刻接升龙打一套稳定伤害；如果被挡，立刻闪避拉开。千万不要在内战中轻易释放第三段蓝霸体普攻，因为对手对双戟的招式再熟悉不过，极易被精准振刀。保持冷静，抓稳后摇是关键。'
    } } else if (id === 'shuangjiegun') {
    tutorialData.value = {
      title: '双节棍进阶教学：深度解析',
      subtitle: '掌握核心技巧，制霸聚窟洲',
      author: '劫学院首席导师',
      date: '2026-06-05',
      difficulty: 4,
      intro: '双节棍是《永劫无间》中攻守兼备的轻型武器典范，被玩家戏称为“龙哥的专属武器”。它拥有独特的“龙虎功”机制：在承受伤害或成功振刀/格挡后，会积攒“龙虎功”层数。消耗龙虎功可以释放出带有强力霸体和高额伤害的特殊反击技能（如龙虎乱舞）。双节棍不仅拥有不俗的近战高频打击感，其强大的防守反击机制更让它成为了高手对决中容错率极高的“单挑神器”。',
      advanced: '双节棍的核心在于“龙虎功的积攒与释放”以及“横栏的精准运用”，进阶必须掌握以下技巧：\n\n**1. “横栏”机制的防守反击**\n双节棍在蓄力过程中被敌方普攻命中，会触发特殊的“横栏”效果，完美格挡本次伤害并增加一层龙虎功。进阶玩家极少用双节棍主动去疯狂平A，而是喜欢“捏蓝”等待对手进攻。一旦触发横栏，可以迅速利用龙虎功打出带有金霸体的右键反击，瞬间扭转战局。学会在拼刀时故意露出破绽，引诱对方攻击你的蓄力架势，是双节棍进阶的第一步。\n\n**2. 龙虎乱舞的毁灭性打击**\n在拥有两层以上龙虎功时，释放“龙虎乱舞”（特殊的蓄力连段）能打出极其华丽且伤害爆表的连续攻击。更重要的是，释放过程中带有极强的霸体和减伤效果。进阶玩家会把龙虎乱舞当作底牌，在团战混乱时或单挑对方试图拼刀时释放。需要注意的是，龙虎乱舞虽然强，但也可以被闪避躲开，因此最好在对方交过闪避或者处于硬直状态下释放，确保伤害拉满。\n\n**3. 灵活的升龙与滑步追击**\n双节棍虽然主打防守反击，但它的追击能力同样不弱。左键普攻后配合闪步可以打出非常流畅的连击。在利用横栏或普攻打出对手硬直后，迅速接上升龙（C+右键）挑飞敌人。双节棍在空中的判定非常优秀，落地后还可以立刻接上蓄力压制。灵活运用滑步和升龙，不给对手喘息的机会，才能将防守反击积累的优势转化为胜势。',
      matchups: '**1. 面对狂暴型轻武器（双刀、太刀）**\n太刀和双刀非常喜欢利用高频普攻压制对手。这恰恰是双节棍最喜欢的节奏。面对他们，你只需要安静地捏住蓝霸体蓄力。他们的高频普攻会疯狂触发你的“横栏”，让你在瞬间积攒满龙虎功。一旦横栏触发，不要犹豫，直接释放龙虎功反击，金霸体判定会直接碾压他们的脆皮身板。面对轻武器，双节棍就是一座无法逾越的叹息之墙。\n\n**2. 面对重型武器（阔刀、斩马刀）**\n阔刀的单发伤害极高，且拥有磐石机制。双节棍打阔刀需要格外小心，因为横栏只能格挡普攻，如果被阔刀的蓄力或磐石反击打中，依然会受到重创。应对策略是：多利用滑步骗出阔刀的蓄力，或者利用左键普攻去“摸”阔刀，触发其磐石后立刻滑步拉开。在积攒了龙虎功后，利用龙虎乱舞的多段金霸体去硬顶阔刀的磐石，但要注意见好就收，不要贪伤害。\n\n**3. 双节棍内战**\n双节棍内战被戏称为“太极推手局”。双方都在捏着蓝霸体试图触发对方的横栏。在这种情况下，谁先动手普攻，谁就容易被对方反击。内战的核心是打破僵局：你可以利用短闪避骗取对方释放蓄力，然后抓其后摇；或者利用升龙去打断对方的捏蓝状态（因为捏蓝不免疫挑飞）。在内战中，对局往往极其漫长，谁能憋得住气，谁就能抓住那转瞬即逝的破绽。'
    } } else if (id === 'hengdao') {
    tutorialData.value = {
      title: '横刀进阶教学：深度解析',
      subtitle: '掌握核心技巧，制霸聚窟洲',
      author: '劫学院首席导师',
      date: '2026-06-05',
      difficulty: 4,
      intro: '横刀是《永劫无间》中一把兼具长剑的优雅与太刀的凌厉的全新轻型武器。它拥有独特的“曲步”机制和极具压制力的直线突刺技能。横刀的普攻节奏感极强，且攻击距离比太刀略长，在近身缠斗中拥有极大的优势。其独有的点刺和拔刀斩不仅动作华丽，还能在瞬间打出高额的爆发伤害。对于追求极致进攻节奏和华丽连招的玩家来说，横刀无疑是一把充满魅力的兵器。',
      advanced: '横刀的核心在于“曲步的运用”与“极快的变招”，进阶横刀高手必须掌握以下技巧：\n\n**1. 曲步（特殊闪避）的灵活运用**\n横刀拥有独特的位移机制——曲步。在普攻或特定招式后，可以通过方向键加闪避键触发带有特殊无敌帧的曲步。进阶玩家会利用曲步在战场上如同鬼魅般穿梭，既可以用来躲避敌方的蓄力攻击，也能在躲避后瞬间拉近距离打出反击。将普通的“A-闪-A”升级为“A-曲步-突刺”，是横刀玩家拉开段位差距的核心基本功。\n\n**2. 拔刀斩的蓄力博弈**\n横刀的蓄力攻击（拔刀斩）拥有极快的出刀速度和不俗的突进距离。与其他武器明显的蓄力前摇不同，横刀的拔刀斩动作非常隐蔽，极难被对手反应振刀。进阶玩家会充分利用这一点，频繁使用“捏蓝”来给对手施加压力。当对手因为紧张而提前交出闪避或者试图振刀时，果断释放拔刀斩进行致命打击。同时，利用下蹲取消蓄力抓破绽，也是横刀博弈的常用手段。\n\n**3. 精准的点刺与升龙连段**\n横刀的左键普攻包含极具威胁的“点刺”动作，不仅距离远，而且带有强硬直效果。在点刺命中敌人后，迅速接上升龙（C+右键）可以稳定将敌人挑飞。由于横刀的空中攻击动作非常利落，在浮空状态下可以轻松接上多次普攻，落地后再利用曲步压迫对手的起身空间。熟练掌握这套连招，能让横刀在单挑中无往不利。',
      matchups: '**1. 面对长武器（长枪、长剑）**\n长武器的攻击距离是横刀的最大障碍。面对长枪和长剑，横刀必须利用自身出色的机动性。切忌直线冲锋，要多利用曲步进行侧向位移，避开长枪的戳刺和长剑的剑气。横刀的拔刀斩突进距离非常可观，在成功躲避对方的攻击后，可以利用拔刀斩瞬间切入内圈。一旦贴身，横刀极快的普攻节奏就能彻底压制住长武器的发挥。\n\n**2. 面对重武器（阔刀、斩马刀）**\n重武器的磐石机制非常克制轻武器的普攻。横刀在打阔刀时，绝不能贪刀。你可以利用长距离的“点刺”去试探阔刀，触发磐石后立刻利用曲步向侧后方拉开距离，让阔刀的反击挥空。多使用蓄力攻击逼迫阔刀也进入蓄力状态，然后进行振刀博弈或者下蹲抓后摇。利用横刀灵活的身法将笨重的重武器“放风筝”，是获胜的关键。\n\n**3. 横刀与太刀的巅峰对决**\n横刀和太刀同属高机动爆发型武器，两者的对决往往在电光火石之间。横刀的优势在于略长一寸的攻击距离和隐蔽的拔刀斩。在对决中，多利用左键的点刺去卡太刀的滑步落点。当太刀试图使用百裂斩时，你可以利用曲步瞬间滑到其侧面进行反打。两者的博弈核心在于谁的反应更快、谁的骗振技巧更高明。保持冷静，抓住太刀滑步的僵直期，是横刀取胜的秘诀。'
    } } else if (id === 'quanren') {
    tutorialData.value = {
      title: '拳刃进阶教学：深度解析',
      subtitle: '掌握核心技巧，制霸聚窟洲',
      author: '劫学院首席导师',
      date: '2026-06-05',
      difficulty: 4,
      intro: '拳刃是《永劫无间》中攻击距离最短，但近身压制力最为恐怖的武器。作为纯粹的近战搏杀兵器，拳刃拥有极快的攻击频率、强悍的贴身黏人能力以及独特的“弹反”机制。虽然它的攻击范围仅限于周身寸许，但一旦让拳刃玩家贴近，其狂风暴雨般的组合拳能在瞬间将敌人撕裂。拳刃非常适合喜欢极限走位、追求拳拳到肉打击感以及擅长近身肉搏的狂热玩家。',
      advanced: '拳刃的核心在于“极限贴身”与“连招节奏”，想要成为拳刃大师，必须掌握以下几点：\n\n**1. 极致的滑步黏人技巧**\n由于拳刃的手极短，如何贴近敌人并保持贴身是最大的难题。进阶拳刃玩家将“A-短闪-A”的滑步机制练到了化境。利用短闪避的无敌帧不仅可以躲避伤害，还能迅速重置普攻后摇并拉近身位。在实战中，拳刃玩家就如同牛皮糖一样，一旦咬住对手，就会利用不断地滑步普攻封锁对手的所有退路，让试图后撤的敌人痛不欲生。\n\n**2. 蓄力“虎扑”的精准释放**\n拳刃的右键蓄力（虎扑）拥有非常优秀的突进距离和吸附效果，是拳刃弥补手短劣势的神技。进阶玩家会利用滑步捏蓝（保持蓄力状态），在距离对手几个身位的地方不断徘徊施加压力。当对手交出闪避或者释放技能后摇时，瞬间释放虎扑切入。虎扑命中后，可以直接接上普攻连段或升龙，是拳刃最核心的起手方式之一。\n\n**3. 升龙与空中连段的暴力美学**\n拳刃的升龙（C+右键）动作极快，判定极强。在利用普攻打出对手硬直后，迅速升龙挑飞。拳刃在空中的连击感极其爆棚，可以打出多次极快节奏的拳击。配合钩锁，高端拳刃玩家甚至能在空中将对手连击至死。掌握拳刃的浮空连招，不仅能打出爆炸伤害，更能给对手带来极大的心理震慑。',
      matchups: '**1. 面对长武器（长枪、斩马刀）**\n这是拳刃最头疼的对局。长枪和斩马刀会在十万八千里外就开始消耗你。打长武器，绝不能在开阔地带直线冲锋。必须利用钩锁、地形掩体不断进行迂回。多利用闪避的无敌帧躲过对方的远距离试探。一旦对方攻击挥空，立刻使用右键蓄力“虎扑”强行突进。记住，只要能贴身，拳刃的极快攻速就会让长武器变成烧火棍，绝对不能给对方拉开距离的机会。\n\n**2. 面对重型兵器（阔刀）**\n拳刃的高频普攻极易触发阔刀的磐石。面对阔刀，拳刃必须一反常态，不能无脑疯狂输出。利用单次普攻去试探阔刀，触发磐石后，利用拳刃极快的收招速度和闪步向侧后方拉开，骗出阔刀的反击。当阔刀反击结束后，再利用虎扑或者滑步上去打一套小连招。把这场战斗变成“猫鼠游戏”，利用机动性戏耍笨重的阔刀。\n\n**3. 拳刃内战或面对匕首**\n这绝对是全游戏节奏最快的近战厮杀。双方都在疯狂地闪步和出拳。内战的核心在于“防守反击”和“抓后摇”。不要主动去拼第一拳，多利用闪步的无敌帧去顶掉对方的攻击，然后在对方攻击落空的瞬间进行反打。面对匕首时，要格外小心匕首的闪步金霸体。拳刃可以利用蓄力虎扑去顶匕首的荆轲献匕，或者多用下蹲和升龙去反制匕首的贴身突刺。谁的手速更快、心理更稳，谁就能赢下这场贴身肉搏。'
    } } else if (id === 'lianjian') {
    tutorialData.value = {
      title: '链剑进阶教学：深度解析',
      subtitle: '掌握核心技巧，制霸聚窟洲',
      author: '劫学院首席导师',
      date: '2026-06-05',
      difficulty: 4,
      intro: '链剑是《永劫无间》中极具特色与变幻莫测的轻型武器。它平时如同一把普通长剑，但在特定招式或蓄力时，剑刃会如同长鞭一样分裂伸长，赋予它极其夸张的攻击范围。链剑兼具了近战的灵活与中远距离的诡异抽击，其独有的“缠绕”和“鞭挞”机制让对手在距离把控上极度头疼。这把武器非常适合喜欢出其不意、善于利用多变攻击距离进行拉扯和消耗的战术型玩家。',
      advanced: '链剑的核心在于“形态切换”与“中远距离拉扯”，进阶链剑高手必须掌握以下技巧：\n\n**1. 鞭态攻击的极限拉扯**\n链剑的蓄力攻击会将武器甩出，化为长鞭进行大范围的抽击。进阶玩家深知，链剑在近身肉搏中并不占优势，因此他们极力避免贴脸拼刀。最佳策略是在中远距离不断利用右键蓄力进行试探和消耗。这种攻击距离比太刀和长剑的普攻都要远，对手很难靠近。即使对手试图振刀，只要距离把控得当，振刀反击也无法命中你。利用“长鞭”形态疯狂“放风筝”，是链剑的核心打法。\n\n**2. 缠绕控制与骗振博弈**\n链剑的某些特定连段带有“缠绕”效果，能在短时间内限制敌人的行动。但链剑的蓄力动作较为明显，容易被有经验的对手振刀。因此，进阶玩家会频繁使用“捏蓝”技巧。蓄力后故意不释放，利用闪避或下蹲取消，骗出对手的振刀动作。当对手振刀挥空陷入硬直时，立刻释放蓄力鞭挞，或者迅速滑步上前进行普攻连段。虚虚实实，让对手无法捉摸你的出招时机。\n\n**3. 空中压制与机动性**\n链剑在空中的攻击动作同样拥有不错的范围判定。在利用普攻或升龙（C+右键）将敌人挑飞后，链剑可以在空中进行多次横扫抽击，不仅伤害可观，还能有效防止对手快速落地反击。此外，链剑的平A后摇较小，配合闪避（Shift）依然可以保持不错的机动性。在面对多人混战时，利用链剑的大范围横扫进行AOE输出和快速脱离战场，是必备的生存技能。',
      matchups: '**1. 面对贴身短兵器（匕首、双刀、拳刃）**\n短兵器是链剑最危险的敌人。一旦被他们贴身，链剑的优势将荡然无存。面对匕首和双刀，链剑必须坚决贯彻“不近身”的原则。利用右键长距离蓄力不断逼退对手。如果对手利用闪步强行突脸，不要试图用普攻去拼刀，立刻利用向后的闪避拉开距离。利用链剑蓄力横扫的超大范围，去拦截对方突进的必经之路，让对方在冲锋的路上就付出惨痛代价。\n\n**2. 面对重型武器（阔刀、斩马刀）**\n重武器的磐石机制对链剑的高频鞭挞有一定的克制作用。在面对阔刀时，链剑千万不要在中近距离无脑释放多段攻击，这极易引发阔刀的磐石反击。应对策略是：把控在阔刀普攻够不到的“极限距离”，用蓄力单次抽击去消耗阔刀。即使触发了磐石，只要距离够远，阔刀的反击也打不到你。耐心拉扯，用“水滴石穿”的战术慢慢磨死笨重的重型武器。\n\n**3. 链剑内战或面对长枪**\n链剑内战就是比拼谁的“距离感”更好。双方都在用鞭态互相抽击，谁能精准卡在对方攻击范围的边缘进行输出，谁就能占据优势。多利用下蹲和侧向滑步规避对方的蓄力。面对同为长武器的长枪时，链剑要小心长枪的直线“龙王破”。链剑的横扫很难打断长枪的突进，因此在长枪蓄力时，最好选择闪避躲开其锋芒，然后抓住长枪出招后的僵直，用鞭挞进行狠狠的反击。'
    } } else if (id === 'feidao') {
    tutorialData.value = {
      title: '飞刀进阶教学：深度解析',
      subtitle: '掌握核心技巧，制霸聚窟洲',
      author: '劫学院首席导师',
      date: '2026-06-05',
      difficulty: 4,
      intro: '虽然飞刀在《永劫无间》中通常作为远程暗器存在，但在高端局中，它却被开发出了极具威胁的“近战辅助”甚至主战打法。飞刀拥有极快的出手速度、极短的攻击后摇以及连续投掷的压制力。它不仅能在中远距离进行极其烦人的消耗，更能在近战拼刀的间隙，利用瞬间的投掷打断敌人的蓄力或补足致命的伤害。对于身法极其灵活、喜欢将距离把控做到极致的“暗杀型”玩家来说，飞刀是不可或缺的夺命利器。',
      advanced: '将飞刀作为主战或核心辅助武器，核心在于“见缝插针”与“距离的极限拉扯”，必须掌握以下技巧：\n\n**1. 瞬发飞刀与打断机制**\n飞刀最大的优势在于其几乎为零的起手前摇。在近战博弈中，当双方都处于试探阶段或者对手试图蓄力（捏蓝）时，进阶玩家会瞬间切出飞刀进行一次快速投掷（左键）。这发飞刀往往能出其不意地打断对手的蓄力节奏，甚至造成微小的硬直。利用这种“瞬发暗器”不断骚扰，会让对手的心理防线彻底崩溃，从而暴露出巨大的走位破绽。\n\n**2. 钩锁与飞刀的“空对地”压制**\n飞刀配合钩锁能打出极其恶心的“制空权”战术。进阶玩家会利用树木、房顶等高点，或者在空中使用钩锁滞空的过程中，向地面的敌人连续投掷飞刀。由于飞刀没有明显的弹道下坠，这种“空对地”的打击极其精准。当地面敌人试图反击或使用飞索拉近距离时，往往会因为不断被飞刀命中而陷入硬直，最终被活活耗死在冲锋的路上。\n\n**3. 蓄力飞刀的精准狙击**\n飞刀不仅能连发，还能进行蓄力（右键）。满蓄力的飞刀不仅伤害极高，且弹道速度极快，犹如狙击枪一般。在团战边缘或者追击残血敌人时，蓄力飞刀是收割人头的神技。进阶玩家会预判敌人的走位方向，提前拉满蓄力，在敌人交出闪避或者跳跃落地的一瞬间松开鼠标，实现一击必杀。掌握蓄力飞刀的提前量预判，是暗器高手的必修课。',
      matchups: '**1. 作为“飞刀客”面对近战突脸（太刀、双刀）**\n当你主打飞刀拉扯时，最怕的就是被太刀或双刀这种高机动武器贴身。一旦被近身，飞刀毫无还手之力。应对策略是：绝不贪伤害，永远留一个闪避的精力。在对方滑步逼近的过程中，一边后撤一边用瞬发飞刀射击。如果对方使用钩锁突进，立刻在空中用飞刀将其打断。必须利用复杂的地形（如房屋、高低差）不断绕圈子，把对方“放风筝”放死。如果实在被贴身，立刻切出近战武器进行防守反击，切忌在近身状态下继续扔飞刀。\n\n**2. 面对敌方远程武器（弓箭、鸟铳）**\n飞刀的射程不如弓箭和鸟铳，在远距离对枪中处于绝对劣势。面对长枪短炮，千万不要站在原地和他们对射。你必须利用钩锁和掩体迅速拉近距离。当进入中距离（飞刀的最佳射程）时，利用飞刀极快的连发速度压制对方。对方蓄力射箭需要时间，而你可以利用连续的短闪避配合飞刀连射，打断他们的蓄力节奏，逼迫他们切出近战武器。\n\n**3. 飞刀辅助近战的极致博弈**\n在最高端的局中，飞刀往往与太刀或长剑配合使用。在近战拼刀时，如果你预判到对方要振刀，你可以假装蓄力，然后瞬间取消并切出飞刀“biu”地射一发，这不仅能骗出对方的振刀动作，还能白嫖伤害。或者在对方残血试图钩锁逃跑时，瞬间切出飞刀将其从空中击落。将飞刀与近战武器无缝切换，做到“远近结合、虚实相生”，才是永劫无间兵器谱的最高境界。'
    } } else {
    const weaponInfo = allWeapons.find(w => w.id === id) || { name: '武器' }
    tutorialData.value = {
      ...defaultData,
      title: `${weaponInfo.name}进阶教学：全面解析`,
      intro: `${weaponInfo.name}在战场上有着独特的定位，合理利用其招式可以克制诸多对手。`
    }
  }
}

const selectWeapon = (id) => {
  router.push(`/weapon-tutorials/${id}`)
}

const userStore = useUserStore()
const dialogVisible = ref(false)
const isEditing = ref(false)
const editId = ref(null)
const form = ref({ category: 'combo', content: '', comboName: '', comboDetails: '', comboNotes: '', videoUrl: '', videoAuthorId: '' })
const submitting = ref(false)
const contributions = ref([])

const comboContributions = computed(() => contributions.value.filter(c => c.category === 'combo'))
const insightContributions = computed(() => contributions.value.filter(c => c.category === 'insight'))

const fetchContributions = async () => {
  try {
    const res = await getContributions({ target_id: currentWeaponId.value, target_type: 'weapon' })
    // Axios usually returns data in res.data, depending on interceptor
    contributions.value = res.results || res.data || res || []
  } catch (err) {
    console.error('Failed to fetch contributions', err)
  }
}

const openDialog = (item = null) => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录后再发布教学！')
    router.push('/login')
    return
  }
  if (item && item.id) {
    isEditing.value = true
    editId.value = item.id
    form.value.category = item.category
    form.value.content = item.content
  } else {
    isEditing.value = false
    editId.value = null
    form.value = { category: 'combo', content: '', comboName: '', comboDetails: '', comboNotes: '', videoUrl: '', videoAuthorId: '' }
  }
  dialogVisible.value = true
}

const handleDelete = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除这条教学分享吗？', '提示', { type: 'warning' })
    await deleteContribution(id)
    ElMessage.success('删除成功')
    fetchContributions()
  } catch (err) {
    if (err !== 'cancel') ElMessage.error('删除失败')
  }
}

const submitForm = async () => {
  let finalContent = ''
  if (form.value.category === 'combo' && !isEditing.value) {
    if (!form.value.comboName.trim() || !form.value.comboDetails.trim()) {
      ElMessage.error('连招名称和详情不能为空')
      return
    }
    finalContent = `### 🌪️ ${form.value.comboName}\n\n**📜 具体连招：**\n<div style="margin:10px 0; padding:15px; background:rgba(255,255,255,0.05); border-left:4px solid #8E9EAB; border-radius:4px; line-height:1.8;">${form.value.comboDetails.replace(/\n/g, '<br>')}</div>\n`
    if (form.value.comboNotes && form.value.comboNotes.trim()) {
      finalContent += `**💡 注意点：**\n<div style="margin:10px 0; padding:15px; background:rgba(255,255,255,0.05); border-left:4px solid #A3B1C6; border-radius:4px; line-height:1.8;">${form.value.comboNotes.replace(/\n/g, '<br>')}</div>\n`
    }
    if (form.value.videoUrl && form.value.videoUrl.trim()) {
      finalContent += `<div style="margin-top: 15px;"><a href="${form.value.videoUrl}" target="_blank" style="display:inline-block; padding:10px 20px; background:#8E9EAB; color:#fff; border-radius:6px; text-decoration:none; font-weight:bold; box-shadow:0 2px 4px rgba(0,0,0,0.2); transition:all 0.3s;">🎬 点击前往观看教学视频</a></div>\n`
      if (form.value.videoAuthorId && form.value.videoAuthorId.trim()) {
        finalContent += `<div style="margin-top: 8px; color: var(--text-secondary); font-size: 0.9em;">由 ${form.value.videoAuthorId} 分享</div>\n`
      }
    }
  } else {
    if (!form.value.content.trim()) {
      ElMessage.error('内容不能为空')
      return
    }
    finalContent = form.value.content
  }

  submitting.value = true
  try {
    if (isEditing.value) {
       await updateContribution(editId.value, { category: form.value.category, content: finalContent })
    } else {
       await createContribution({
         target_id: currentWeaponId.value,
         target_type: 'weapon',
         category: form.value.category,
         content: finalContent
       })
    }
    ElMessage.success(isEditing.value ? '修改成功！' : '发布成功！')
    dialogVisible.value = false
    fetchContributions()
  } catch (err) {
    ElMessage.error(isEditing.value ? '修改失败' : '发布失败')
  } finally {
    submitting.value = false
  }
}

watch(() => route.params.id, (newId) => {
  updateData(newId || 'taidao')
  fetchContributions()
})

onMounted(() => {
  const initialId = route.params.id || 'taidao'
  updateData(initialId)
  fetchContributions()
})
</script>

<style scoped>
.page-wrapper {
  display: flex;
  min-height: 100vh;
}

/* 全局左侧高级导航栏 */
.global-sidebar {
  position: fixed;
  top: 72px; /* Navbar height */
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

.sidebar-header .icon {
  font-size: 20px;
}

.sidebar-header .title {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: 2px;
}

.sidebar-content {
  flex: 1;
  overflow-y: auto;
  padding: 16px 0;
  /* 隐藏丑陋的原生滚动条 */
  scrollbar-width: none; /* Firefox */
}
.sidebar-content::-webkit-scrollbar {
  display: none; /* Chrome, Safari */
}

.nav-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-item {
  padding: 12px 24px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  display: flex;
  align-items: center;
}

.nav-text {
  font-size: 15px;
  color: var(--text-secondary);
  font-weight: 500;
  transition: all 0.3s ease;
  letter-spacing: 1px;
}

.nav-item:hover {
  background: var(--bg-primary);
}

.nav-item:hover .nav-text {
  color: var(--accent-gold);
  transform: translateX(4px);
}

/* 激活状态 */
.nav-item.active {
  background: var(--accent-gold-bg);
}

.nav-item.active .nav-text {
  color: var(--accent-gold);
  font-weight: 700;
}

.nav-item.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  width: 4px;
  background: var(--accent-gold);
  box-shadow: 0 0 10px rgba(184, 134, 11, 0.5);
}

/* 右侧内容区适配 */
.tutorial-page {
  flex: 1;
  padding-bottom: 80px;
  margin-top: -72px; /* Pull up under navbar */
}

.tutorial-header {
  height: 400px;
  background: var(--bg-tertiary);
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid var(--border-default);
  padding-top: 72px;
  padding-left: 240px; /* Offset for sidebar to center text in remaining space */
}

.header-content {
  text-align: center;
  max-width: 800px;
  padding: 0 20px;
  animation: fadeIn 1s ease;
}

.header-content h1 {
  font-size: 48px;
  font-weight: 900;
  color: var(--text-primary);
  margin-bottom: 16px;
  font-family: "Noto Serif SC", serif;
  background: linear-gradient(120deg, var(--text-primary), var(--accent-gold));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.subtitle {
  font-size: 20px;
  color: var(--text-secondary);
  margin-bottom: 32px;
  letter-spacing: 2px;
}

.meta {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 24px;
  color: var(--text-muted);
  font-size: 14px;
}

.difficulty {
  display: flex;
  align-items: center;
  gap: 8px;
}

.tutorial-container {
  width: 100%;
  max-width: 1600px; /* Increase max width for larger document area */
  margin: 60px 0 0 0; /* Left align instead of center */
  padding-left: 300px; /* Fixed 60px gap from the 240px global sidebar */
  padding-right: 60px;
  display: flex;
  gap: 40px; /* Reduce gap between TOC and content */
}

.sidebar {
  width: 240px; /* 缩小目录栏 */
  flex-shrink: 0;
}

.nav-tree {
  position: sticky;
  top: 100px;
  background: var(--glass-bg);
  backdrop-filter: blur(10px);
  border: 1px solid var(--border-light);
  padding: 24px;
  border-radius: 12px;
}

.nav-tree h3 {
  font-size: 18px;
  color: var(--text-primary);
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--border-default);
}

.nav-tree ul {
  list-style: none;
  padding: 0;
}

.nav-tree li {
  margin-bottom: 12px;
}

.nav-tree a {
  color: var(--text-secondary);
  font-size: 15px;
  transition: all 0.2s;
  display: block;
}

.nav-tree a:hover {
  color: var(--accent-gold);
  transform: translateX(4px);
}

.content {
  flex: 1;
  min-width: 0;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 1024px) {
  .global-sidebar {
    width: 200px;
  }
  .tutorial-header {
    padding-left: 200px;
  }
  .tutorial-container {
    padding-left: 240px;
    flex-direction: column;
  }
  .sidebar {
    width: 100%;
  }
  .nav-tree {
    position: static;
  }
}

@media (max-width: 768px) {
  .global-sidebar {
    display: none; /* Hide global sidebar on mobile for now */
  }
  .tutorial-header {
    padding-left: 0;
  }
  .header-content h1 {
    font-size: 32px;
  }
  .tutorial-container {
    padding: 0 20px;
  }
}

/* UGC 版块样式 */
.community-section {
  margin-top: 40px;
  border-top: 2px dashed var(--border-default);
  padding-top: 40px;
}

.community-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  background: var(--bg-secondary);
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}

.primary-btn {
  background: var(--accent-gold);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.primary-btn:hover {
  background: var(--accent-gold-light);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px var(--accent-gold-bg);
}

.premium-publish-btn {
  margin-top: 20px;
  width: 100%;
  position: relative;
  padding: 16px 24px;
  background: rgba(40, 44, 52, 0.8);
  border: 1px solid rgba(142, 158, 171, 0.3);
  border-radius: 12px;
  color: #E0E5EC;
  font-size: 16px;
  font-weight: bold;
  letter-spacing: 2px;
  cursor: pointer;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(8px);
}

.premium-publish-btn:hover {
  transform: translateY(-2px);
  border-color: rgba(142, 158, 171, 0.8);
  box-shadow: 0 8px 25px rgba(142, 158, 171, 0.25);
  color: #fff;
}

.btn-glow {
  position: absolute;
  top: 0;
  left: -100%;
  width: 50%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(142, 158, 171, 0.3), transparent);
  transform: skewX(-20deg);
  transition: all 0.6s ease;
}

.premium-publish-btn:hover .btn-glow {
  left: 200%;
}

.premium-cta-block {
  background: transparent;
  padding: 20px 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
  margin-bottom: 30px;
  position: relative;
}

.premium-cta-block::before,
.premium-cta-block::after {
  content: '';
  height: 1px;
  flex: 1;
  background: linear-gradient(90deg, transparent, rgba(142, 158, 171, 0.5), transparent);
}

.cta-icon {
  color: #8E9EAB;
  font-size: 1.2em;
  opacity: 0.8;
}

.cta-text {
  font-family: 'Georgia', 'Times New Roman', serif;
  color: #8E9EAB;
  font-size: 1.3em;
  font-weight: 400;
  letter-spacing: 4px;
  text-shadow: 0 2px 10px rgba(142, 158, 171, 0.2);
}

.empty-state {
  text-align: center;
  padding: 60px 0;
  color: var(--text-light);
  background: var(--bg-secondary);
  border-radius: 12px;
}

.contribution-card {
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02);
  transition: all 0.3s;
}

.contribution-card:hover {
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.06);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border-light);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar-placeholder {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--bg-tertiary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.username {
  font-weight: bold;
  color: var(--text-primary);
}

.meta-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.category-tag {
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 12px;
  font-weight: bold;
}

.category-tag.combo {
  background: rgba(220, 20, 60, 0.1);
  color: crimson;
}

.category-tag.insight {
  background: var(--accent-gold-bg);
  color: var(--accent-gold);
}

.time {
  color: var(--text-light);
  font-size: 13px;
}

.card-content {
  color: var(--text-secondary);
  line-height: 1.8;
  white-space: pre-wrap;
}
</style>
