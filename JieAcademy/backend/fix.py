import os
import re

def process_vue_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update <script setup> imports
    content = content.replace(
        "import { getContributions, createContribution } from '@/api/tutorials'",
        "import { getContributions, createContribution, updateContribution, deleteContribution } from '@/api/tutorials'"
    )
    content = content.replace(
        "import { ElMessage } from 'element-plus'",
        "import { ElMessage, ElMessageBox } from 'element-plus'"
    )
    content = content.replace("import { ref, onMounted, watch } from 'vue'", "import { ref, computed, onMounted, watch } from 'vue'")

    # 2. Update reactive variables
    old_vars = """const dialogVisible = ref(false)
const form = ref({ category: 'insight', content: '' })
const submitting = ref(false)
const contributions = ref([])"""
    new_vars = """const dialogVisible = ref(false)
const isEditing = ref(false)
const editId = ref(null)
const form = ref({ category: 'combo', content: '', comboName: '', comboDetails: '', comboNotes: '', videoUrl: '' })
const submitting = ref(false)
const contributions = ref([])

const comboContributions = computed(() => contributions.value.filter(c => c.category === 'combo'))
const insightContributions = computed(() => contributions.value.filter(c => c.category === 'insight'))"""
    content = content.replace(old_vars, new_vars)

    # 3. Update openDialog
    old_openDialog = """const openDialog = () => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录后再发表心得！')
    router.push('/login')
    return
  }
  form.value = { category: 'insight', content: '' }
  dialogVisible.value = true
}"""
    new_openDialog = """const openDialog = (item = null) => {
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
    form.value = { category: 'combo', content: '', comboName: '', comboDetails: '', comboNotes: '', videoUrl: '' }
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
}"""
    content = content.replace(old_openDialog, new_openDialog)

    # 4. Update submitForm
    old_submitForm = """const submitForm = async () => {
  if (!form.value.content.trim()) {
    ElMessage.error('内容不能为空')
    return
  }
  submitting.value = true
  try {
    await createContribution({
      target_id: currentWeaponId.value,
      target_type: 'weapon',
      category: form.value.category,
      content: form.value.content
    })
    ElMessage.success('发布成功！')
    dialogVisible.value = false
    fetchContributions()
  } catch (err) {
    ElMessage.error('发布失败')
  } finally {
    submitting.value = false
  }
}"""
    target_type = "'weapon'" if 'Weapon' in file_path else "'hero'"
    
    new_submitForm = f"""const submitForm = async () => {{
  let finalContent = ''
  if (form.value.category === 'combo' && !isEditing.value) {{
    if (!form.value.comboName.trim() || !form.value.comboDetails.trim()) {{
      ElMessage.error('连招名称和详情不能为空')
      return
    }}
    finalContent = `### 🌪️ ${{form.value.comboName}}\\n\\n**具体连招：**\\n${{form.value.comboDetails}}\\n`
    if (form.value.comboNotes && form.value.comboNotes.trim()) {{
      finalContent += `\\n**💡 注意点：**\\n${{form.value.comboNotes}}\\n`
    }}
    if (form.value.videoUrl && form.value.videoUrl.trim()) {{
      finalContent += `\\n[🔗 点击前往观看教学视频](${{form.value.videoUrl}})\\n`
    }}
  }} else {{
    if (!form.value.content.trim()) {{
      ElMessage.error('内容不能为空')
      return
    }}
    finalContent = form.value.content
  }}

  submitting.value = true
  try {{
    if (isEditing.value) {{
       await updateContribution(editId.value, {{ category: form.value.category, content: finalContent }})
    }} else {{
       await createContribution({{
         target_id: {'currentWeaponId.value' if target_type == "'weapon'" else 'currentHeroId.value'},
         target_type: {target_type},
         category: form.value.category,
         content: finalContent
       }})
    }}
    ElMessage.success(isEditing.value ? '修改成功！' : '发布成功！')
    dialogVisible.value = false
    fetchContributions()
  }} catch (err) {{
    ElMessage.error(isEditing.value ? '修改失败' : '发布失败')
  }} finally {{
    submitting.value = false
  }}
}}"""
    if 'currentWeaponId' not in old_submitForm:
        old_submitForm = old_submitForm.replace('currentWeaponId', 'currentHeroId')
        
    content = content.replace(old_submitForm, new_submitForm)

    # 5. Template changes: Nav sidebar button
    nav_tree = """            </ul>
          </div>
        </div>"""
    nav_tree_new = """            </ul>
            <button class="primary-btn publish-btn" @click="openDialog()" style="margin-top: 20px; width: 100%;">
              ✏️ 发布我的教学
            </button>
          </div>
        </div>"""
    content = content.replace(nav_tree, nav_tree_new)

    # 6. Template changes: Combos integration
    combo_old = """<pre><code>// 连招输入指令示例
LMB -> LMB -> C + RMB (升龙) -> 在空中 LMB</code></pre>"""
    if 'Hero' in file_path:
        combo_old = """<li><strong>F技能接大招：</strong> 很多英雄的核心连招都是利用F技能的僵直或击飞，来保证大招的绝对命中。</li>
          </ul>"""
          
    combo_new = combo_old + """
          
          <div class="ugc-combos" v-if="comboContributions.length > 0" style="margin-top: 30px;">
            <h3 style="color: var(--accent-gold); border-bottom: 1px dashed var(--border-default); padding-bottom: 10px;">🌟 玩家连招分享</h3>
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
              <div class="card-content markdown-body">
                {{ item.content }}
              </div>
            </div>
          </div>"""
    content = content.replace(combo_old, combo_new)

    # 7. Template changes: Matchups integration
    if 'Weapon' in file_path:
        matchup_old = """<li><strong>对战阔刀：</strong> 阔刀拥有磐石架势，不要盲目攻击，可以尝试使用蓄力骗对方出招。</li>
          </ul>"""
    else:
        matchup_old = """<li><strong>面对控制英雄：</strong> 注意躲避控制技能，利用身法拉扯。</li>
          </ul>"""
    
    matchup_new = matchup_old + """
          <div class="ugc-insights" v-if="insightContributions.length > 0" style="margin-top: 30px;">
            <h3 style="color: var(--accent-gold); border-bottom: 1px dashed var(--border-default); padding-bottom: 10px;">💡 玩家实战感悟</h3>
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
              <div class="card-content markdown-body">
                {{ item.content }}
              </div>
            </div>
          </div>"""
    content = content.replace(matchup_old, matchup_new)

    # 8. Remove old community section
    community_old = re.search(r'<h2 id="community">五、 玩家感悟与连招</h2>.*?</div>\s*</div>\s*</div>', content, re.DOTALL)
    if community_old:
        content = content.replace(community_old.group(0), '</div>')
        content = content.replace('<li><a href="#community">五、 玩家感悟与连招</a></li>', '')

    # 9. Update Dialog Template
    dialog_old = """<el-dialog v-model="dialogVisible" title="分享我的心得" width="600px" custom-class="glass-dialog">
      <el-form :model="form" label-width="80px">
        <el-form-item label="分类">
          <el-radio-group v-model="form.category">
            <el-radio label="combo">连招分享</el-radio>
            <el-radio label="insight">实战感悟</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="内容">
          <el-input 
            v-model="form.content" 
            type="textarea" 
            :rows="8" 
            placeholder="分享你的实战思路或者连招按键（支持 Markdown 格式）..." 
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm" :loading="submitting">发布</el-button>
        </span>
      </template>
    </el-dialog>"""
    
    dialog_new = """<el-dialog v-model="dialogVisible" :title="isEditing ? '修改教学内容' : '发布我的教学'" width="650px" custom-class="glass-dialog">
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
          <el-form-item label="教学视频">
            <el-input v-model="form.videoUrl" placeholder="选填，输入B站或抖音链接..." />
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
    </el-dialog>"""
    content = content.replace(dialog_old, dialog_new)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

process_vue_file(r'e:\My_project\JieAcademy\frontend\src\views\weapon\WeaponTutorial.vue')
process_vue_file(r'e:\My_project\JieAcademy\frontend\src\views\hero\HeroTutorial.vue')
print('Update complete.')
