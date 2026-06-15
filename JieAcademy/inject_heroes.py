import os
import random

base_dir = r"e:\My_project\JieAcademy"
vue_path = os.path.join(base_dir, r"frontend\src\views\hero\HeroTutorial.vue")

top_heroes = {
    'jianan': ('迦南', '刺客', '高机动、隐身暗杀、极强逃生能力'),
    'yaodaoji': ('妖刀姬', '战士', '极高爆发、大招斩击、近战压制'),
    'jicanghai': ('季沧海', '战士', '无限连招、火球消耗、极高移速'),
    'tianhai': ('天海', '坦克', '金钟罩防御、化身大佛、团战核心'),
    'ninghongye': ('宁红夜', '控制', '群体眩晕、禁疗封技能、先手开团'),
    'temuer': ('特木尔', '控制', '风沙护体、群体减速控制、分割战场'),
    'hutao': ('土御门胡桃', '辅助', '单体连线治疗、群体净化回复、团队保障'),
    'yueshan': ('岳山', '坦克', '霸体冲锋、化身神将、破坏阵型'),
    'cuisanniang': ('崔三娘', '控制', '水流束缚、大范围滞空控制、配合爆发'),
    'wuchen': ('无尘', '辅助', '斗转星移传送、剑气消耗、战术转移'),
    'guqinghan': ('顾清寒', '刺客', '冰冻控制、多段突进、极高容错率'),
    'wutianxinzha': ('武田信忠', '战士', '夺刀反击、恶鬼附身、极强拼刀能力'),
    'yinziping': ('殷紫萍', '辅助', '灵机护盾、免死机制、持续恢复'),
    'shenmiao': ('沈妙', '射手', '召唤机甲、火炮压制、超远距离救援'),
    'huwei': ('胡为', '刺客', '虎啸突进、多段跳跃、极强追击能力'),
    'jiyingying': ('季莹莹', '刺客', '锁链鞭打、无敌幽冥状态、持续灼烧'),
    'yulinglong': ('玉玲珑', '控制', '迷魂恐惧、狐狸位移、打乱敌方节奏'),
    'hadi': ('哈迪', '战士', '机械臂钩锁、长时间飞行、空中打击'),
    'weiqing': ('魏轻', '战士', '执明神君护体、盾反机制、攻守兼备'),
    'liulian': ('刘炼', '控制', '金石领域、限制位移、强力控场'),
    'zhangqiling': ('张起灵', '刺客', '黑金古刀爆发、麒麟血爆发、绝境反击'),
    'xila': ('席拉', '辅助', '光之护盾、群体治愈、神圣庇护'),
    'lanmeng': ('蓝梦', '法师', '幻境迷彩、法系爆发、视野干扰'),
    'ganxuan': ('甘璇', '辅助', '音波控制、群体增益、节奏把控'),
    'lixunhuan': ('李寻欢', '射手', '飞刀绝技、百发百中、超远距离斩杀'),
    'wanjun': ('万钧', '坦克', '雷霆之怒、重装护甲、绝对防御'),
    'wuzhen': ('巫真', '法师', '蛊毒术法、持续消耗、地形污染')
}

def generate_intro(h_name, h_role, h_trait):
    intros = [
        f"{h_name}在《永劫无间》中被定位为出色的{h_role}型英雄。凭借其{h_trait}的核心机制，{h_name}在聚窟洲中声名显赫。对于进阶玩家而言，该英雄不仅具备极高的操作上限，更能在实战博弈中提供极大的战术价值。无论是在单挑对线时的极限拉扯，还是在团战爆发时的关键切入，{h_name}都能游刃有余。深入理解其技能的底层逻辑，并将其与常规武器连招完美结合，是发挥该英雄真正实力的关键所在。",
        f"作为一名深受欢迎的{h_role}英雄，{h_name}以其独特的{h_trait}能力在战场上占据着不可替代的地位。在高端局的对抗中，{h_name}往往是队伍战术体系的核心枢纽。其技能组不仅提供了极佳的自保与反打能力，更能在瞬息万变的战斗中创造出不可思议的高光操作。掌握{h_name}，意味着你必须具备精准的时机判断力和极强的大局观，这也是众多绝活哥钟爱这名英雄的根本原因。",
        f"{h_name}是《永劫无间》中上限极高的{h_role}角色。其招牌的{h_trait}特性让对手在面对他时总是倍感压力。在熟练度达标的玩家手中，{h_name}就如同一件完美的杀戮艺术品，能够通过极其流畅的技能衔接打得对手毫无还手之力。想要真正精通这位英雄，除了需要苦练身法与基础连招外，更需要深刻领悟其在不同对局环境下的定位转换，从而在每一场战斗中都立于不败之地。"
    ]
    return random.choice(intros)

def generate_strategy(h_name, h_role, h_trait):
    return f"""**【单排思路】**
作为一名{h_role}英雄，{h_name}在单排模式下的核心法则可以概括为“扬长避短，伺机而动”。前期搜刮物资时，尽量选择能够快速脱战的路线，利用自身{h_trait}的特性去规避无意义的早期大乱斗。在遭遇战中，绝不能像莽夫一样死拼平A。你需要时刻盯紧自己的技能冷却时间：技能空窗期，多利用掩体和短闪避进行防守拉扯；一旦关键技能转好，则要果断发难，利用技能带来的高容错率去抓对手的普攻或振刀后摇。单排中最忌讳被第三方劝架，因此在击杀一人后，无论状态如何，都应优先考虑转移阵地。记住，活到梅花桩，你的上限才会真正显现。

**【三排思路】**
在三排的高强度团战中，{h_name}的战术价值会被无限放大。你不再是一个人在战斗，而是需要将“{h_trait}”的优势辐射给整个团队。在接团前，利用你的技能机制去抢占视野或进行骚扰，破坏敌方的阵型站位。一旦团战爆发，必须时刻关注敌方核心输出和己方辅助的位置。如果己方遭到强势开团，果断交出奥义大招进行拆火和反制，强行中断敌方的进攻节奏；如果己方处于追击态势，则要利用自身机动性封死敌人的退路。一个顶尖的{h_name}玩家，不仅是输出的利刃，更是团队的坚实后盾。在三排中多与队友沟通大招的衔接时机，往往能打出毁天灭地的完美团战。"""

hero_js_snippets = []

for h_id, (h_name, h_role, h_trait) in top_heroes.items():
    intro = generate_intro(h_name, h_role, h_trait).replace('\\', '\\\\').replace('\n', '\\n').replace("'", "\\'")
    strategy = generate_strategy(h_name, h_role, h_trait).replace('\\', '\\\\').replace('\n', '\\n').replace("'", "\\'")
    
    snippet = f"""  if (id === '{h_id}') {{
    tutorialData.value = {{
      title: '{h_name}进阶教学：深度解析',
      subtitle: '掌控绝技，主宰战场',
      author: '劫学院首席导师',
      date: '2026-06-05',
      difficulty: 4,
      intro: '{intro}',
      strategy: '{strategy}'
    }}"""
    hero_js_snippets.append(snippet)

js_code = """const updateData = (id) => {
  currentHeroId.value = id
  window.scrollTo({ top: 0, behavior: 'smooth' })
  
""" + " } else ".join([s.replace("  if", "if") for s in hero_js_snippets]) + """ } else {
    const heroInfo = allHeroes.find(h => h.id === id) || { name: '英雄' }
    tutorialData.value = {
      ...defaultData,
      title: `${heroInfo.name}进阶教学：全面解析`,
      intro: `${heroInfo.name}在战场上有着独特的定位，合理利用其招式可以克制诸多对手。`
    }
  }
}
"""

with open(vue_path, 'r', encoding='utf-8') as f:
    vue_content = f.read()

start_marker = "const updateData = (id) => {"
end_marker = "const selectHero = (id) => {"

start_idx = vue_content.find(start_marker)
end_idx = vue_content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    new_vue_content = vue_content[:start_idx] + js_code + "\n" + vue_content[end_idx:]
    with open(vue_path, 'w', encoding='utf-8') as f:
        f.write(new_vue_content)
    print("Successfully updated HeroTutorial.vue")
else:
    print("Could not find start or end markers in HeroTutorial.vue")
