import os
import re

base_dir = r"e:\My_project\JieAcademy"
vue_path = os.path.join(base_dir, r"frontend\src\views\weapon\WeaponTutorial.vue")

weapons = [
    ('changjian', '长剑'),
    ('taidao', '太刀'),
    ('kuodao', '阔刀'),
    ('zhanmadao', '斩马刀'),
    ('changqiang', '长枪'),
    ('gun', '棍'),
    ('bishou', '匕首'),
    ('shanzi', '扇子'),
    ('shuangdao', '双刀'),
    ('shuangji', '双戟'),
    ('shuangjiegun', '双节棍'),
    ('hengdao', '横刀'),
    ('quanren', '拳刃'),
    ('lianjian', '链剑'),
    ('feidao', '飞刀')
]

js_snippets = []

for w_id, w_name in weapons:
    md_path = os.path.join(base_dir, f"{w_name}教学.md")
    if not os.path.exists(md_path):
        print(f"Skipping {w_name}, file not found")
        continue
    
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    intro_match = re.search(r'## 一、 武器简介\n(.*?)\n## 三、', content, re.DOTALL)
    advanced_match = re.search(r'## 三、 进阶技巧\n(.*?)\n## 四、', content, re.DOTALL)
    matchups_match = re.search(r'## 四、 实战应对\n(.*)', content, re.DOTALL)
    
    if intro_match and advanced_match and matchups_match:
        intro = intro_match.group(1).strip().replace('\n', '\\n').replace("'", "\\'")
        advanced = advanced_match.group(1).strip().replace('\n', '\\n').replace("'", "\\'")
        matchups = matchups_match.group(1).strip().replace('\n', '\\n').replace("'", "\\'")
        
        snippet = f"""  if (id === '{w_id}') {{
    tutorialData.value = {{
      title: '{w_name}进阶教学：深度解析',
      subtitle: '掌握核心技巧，制霸聚窟洲',
      author: '劫学院首席导师',
      date: '2026-06-05',
      difficulty: 4,
      intro: '{intro}',
      advanced: '{advanced}',
      matchups: '{matchups}'
    }}"""
        js_snippets.append(snippet)
    else:
        print(f"Skipping {w_name}, missing sections")

if not js_snippets:
    print("No valid snippets found.")
    exit(1)

js_code = """const updateData = (id) => {
  currentWeaponId.value = id
  window.scrollTo({ top: 0, behavior: 'smooth' })
  
""" + " } else ".join([s.replace("  if", "if") for s in js_snippets]) + """ } else {
    const weaponInfo = allWeapons.find(w => w.id === id) || { name: '武器' }
    tutorialData.value = {
      ...defaultData,
      title: `${weaponInfo.name}进阶教学：全面解析`,
      intro: `${weaponInfo.name}在战场上有着独特的定位，合理利用其招式可以克制诸多对手。`
    }
  }
}
"""

with open(vue_path, 'r', encoding='utf-8') as f:
    vue_content = f.read()

start_marker = "const updateData = (id) => {"
end_marker = "const selectWeapon = (id) => {"

start_idx = vue_content.find(start_marker)
end_idx = vue_content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    new_vue_content = vue_content[:start_idx] + js_code + "\n" + vue_content[end_idx:]
    with open(vue_path, 'w', encoding='utf-8') as f:
        f.write(new_vue_content)
    print("Successfully updated WeaponTutorial.vue")
else:
    print("Could not find start or end markers in WeaponTutorial.vue")
