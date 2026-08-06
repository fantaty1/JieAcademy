import os
import re

def fix_markdown(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add markdown-it import
    if "import MarkdownIt from 'markdown-it'" not in content:
        content = content.replace("import { ElMessage, ElMessageBox } from 'element-plus'", 
                                  "import { ElMessage, ElMessageBox } from 'element-plus'\nimport MarkdownIt from 'markdown-it'\nconst md = new MarkdownIt({ html: true, breaks: true, linkify: true })")
    
    # 2. Replace {{ item.content }} with v-html
    content = content.replace("<div class=\"card-content markdown-body\">\n                {{ item.content }}\n              </div>", 
                              "<div class=\"card-content markdown-body\" v-html=\"md.render(item.content)\"></div>")
    
    # 3. Enhance combo form markdown generation (WeaponTutorial.vue)
    if 'Weapon' in filepath:
        old_submit_combo = """finalContent = `### 🌪️ ${form.value.comboName}\\n\\n**具体连招：**\\n${form.value.comboDetails}\\n`
    if (form.value.comboNotes && form.value.comboNotes.trim()) {
      finalContent += `\\n**💡 注意点：**\\n${form.value.comboNotes}\\n`
    }
    if (form.value.videoUrl && form.value.videoUrl.trim()) {
      finalContent += `\\n[🔗 点击前往观看教学视频](${form.value.videoUrl})\\n`
    }"""
        new_submit_combo = """finalContent = `### 🌪️ ${form.value.comboName}\\n\\n**📜 具体连招：**\\n<div style="margin:10px 0; padding:15px; background:rgba(255,255,255,0.05); border-left:4px solid var(--accent-gold); border-radius:4px; line-height:1.8;">${form.value.comboDetails.replace(/\\n/g, '<br>')}</div>\\n`
    if (form.value.comboNotes && form.value.comboNotes.trim()) {
      finalContent += `**💡 注意点：**\\n<div style="margin:10px 0; padding:15px; background:rgba(255,255,255,0.05); border-left:4px solid #E6A23C; border-radius:4px; line-height:1.8;">${form.value.comboNotes.replace(/\\n/g, '<br>')}</div>\\n`
    }
    if (form.value.videoUrl && form.value.videoUrl.trim()) {
      finalContent += `<a href="${form.value.videoUrl}" target="_blank" style="display:inline-block; margin-top:15px; padding:10px 20px; background:var(--accent-gold); color:#000; border-radius:6px; text-decoration:none; font-weight:bold; box-shadow:0 2px 4px rgba(0,0,0,0.2); transition:all 0.3s;">🎬 点击前往观看教学视频</a>\\n`
    }"""
        content = content.replace(old_submit_combo, new_submit_combo)

    # 4. Enhance matchup form markdown generation (HeroTutorial.vue)
    if 'Hero' in filepath:
        old_submit_matchup = """finalContent = `### ⚔️ 对阵【${form.value.comboName}】\\n\\n**应对策略：**\\n${form.value.comboDetails}\\n`
    if (form.value.videoUrl && form.value.videoUrl.trim()) {
      finalContent += `\\n[🔗 点击前往观看教学视频](${form.value.videoUrl})\\n`
    }"""
        new_submit_matchup = """finalContent = `### ⚔️ 对阵【${form.value.comboName}】\\n\\n**🛡️ 应对策略：**\\n<div style="margin:10px 0; padding:15px; background:rgba(255,255,255,0.05); border-left:4px solid var(--accent-gold); border-radius:4px; line-height:1.8;">${form.value.comboDetails.replace(/\\n/g, '<br>')}</div>\\n`
    if (form.value.videoUrl && form.value.videoUrl.trim()) {
      finalContent += `<a href="${form.value.videoUrl}" target="_blank" style="display:inline-block; margin-top:15px; padding:10px 20px; background:var(--accent-gold); color:#000; border-radius:6px; text-decoration:none; font-weight:bold; box-shadow:0 2px 4px rgba(0,0,0,0.2); transition:all 0.3s;">🎬 点击前往观看教学视频</a>\\n`
    }"""
        content = content.replace(old_submit_matchup, new_submit_matchup)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_markdown(r'e:\My_project\JieAcademy\frontend\src\views\weapon\WeaponTutorial.vue')
fix_markdown(r'e:\My_project\JieAcademy\frontend\src\views\hero\HeroTutorial.vue')
print('Fixed Markdown rendering!')
