# ⚠️ Vercel 环境变量配置（必需）

## 问题诊断

测试显示所有API都返回500错误的根本原因：
1. ✅ **已修复**: vercel.json配置缺失 → 已添加正确的builds和routes配置
2. ⚠️ **需要配置**: Vercel环境变量未设置 → 需要你手动添加

---

## 🔧 立即配置环境变量

### 步骤1: 登录Vercel控制台

访问：https://vercel.com/xiaolvzz/paper-web-manager/settings/environment-variables

或者：
1. 进入 https://vercel.com/
2. 选择你的项目 `paper-web-manager`
3. 点击 **Settings**（设置）
4. 点击左侧 **Environment Variables**（环境变量）

### 步骤2: 添加以下环境变量

#### 变量1: SUPABASE_URL
```
Name: SUPABASE_URL
Value: https://wlslekyepjebnzjmslld.supabase.co
Environment: Production, Preview, Development (全选)
```

#### 变量2: SUPABASE_KEY
```
Name: SUPABASE_KEY
Value: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Indsc2xla3llcGplYm56am1zbGxkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzUyODkzMDIsImV4cCI6MjA1MDg2NTMwMn0.tDSXMfEpCbvK5wYVaHxSIZhSMxsP2-OL2g_j0eVFJY0
Environment: Production, Preview, Development (全选)
```

**注意**：如果你的Supabase Key不同，使用你自己的Key。

### 步骤3: 重新部署

配置完环境变量后，需要触发重新部署：

**方法1: 在Vercel控制台重新部署**
1. 进入 **Deployments** 页面
2. 点击最新的部署
3. 点击右上角的 **⋯** 菜单
4. 选择 **Redeploy**

**方法2: 推送新的代码**（已经完成）
- 代码已经推送到GitHub，Vercel会自动检测并重新部署

---

## ✅ 验证配置

### 等待部署完成（约2-3分钟）

在Vercel的Deployments页面查看部署状态：
- **Building**: 正在构建
- **Ready**: 部署成功 ✅

### 测试API

部署完成后，访问以下URL测试：

#### 测试1: 健康检查
```
https://paper-web-manager.vercel.app/api/health
```

**预期响应**：
```json
{
  "status": "healthy",
  "message": "论文管理系统运行正常",
  "environment": "vercel"
}
```

#### 测试2: arXiv服务
```
https://paper-web-manager.vercel.app/api/arxiv/health
```

**预期响应**：
```json
{
  "status": "ok",
  "message": "arXiv API连接正常"
}
```

#### 测试3: 论文列表
```
https://paper-web-manager.vercel.app/api/papers/
```

**预期响应**：
```json
[]
```
（空数组，因为还没有添加论文）

---

## 🧪 完整测试

配置完成后，重新运行自动化测试：

```
https://paper-web-manager.vercel.app/test_complete.html
```

点击"开始测试"，应该看到：
- ✅ 测试1-3: 通过（绿色）
- ⚠️ 测试4: 可能警告（如果arXiv ID不存在）
- ✅ 测试5-8: 通过（绿色）

---

## 🐛 如果仍然失败

### 检查1: 环境变量是否正确设置

在Vercel Settings → Environment Variables 页面：
- 确认 `SUPABASE_URL` 存在
- 确认 `SUPABASE_KEY` 存在
- 确认两者都选择了所有环境（Production, Preview, Development）

### 检查2: 查看部署日志

1. 进入 **Deployments** 页面
2. 点击最新的部署
3. 点击 **View Function Logs**
4. 查看错误信息

常见错误：
- `Environment variable ... not found` → 环境变量未配置
- `Connection refused` → Supabase URL或Key错误
- `Import error` → Python依赖问题

### 检查3: Supabase连接

确认Supabase服务正常：
1. 登录 https://supabase.com
2. 选择你的项目
3. 在 **Settings** → **API** 页面确认：
   - Project URL正确
   - anon public key正确

---

## 📋 配置清单

在继续之前，确认以下步骤都已完成：

- [ ] Vercel环境变量：SUPABASE_URL 已添加
- [ ] Vercel环境变量：SUPABASE_KEY 已添加
- [ ] 两个变量都选择了所有环境
- [ ] 触发了重新部署（自动或手动）
- [ ] 等待部署完成（状态显示 Ready）
- [ ] 测试 /api/health 返回200
- [ ] 测试 /api/papers/ 返回200
- [ ] 运行自动化测试并查看结果

---

## 🎯 下一步

配置完成并验证成功后：

1. **测试添加论文**
   - 使用 PDF URL: `https://arxiv.org/pdf/1706.03762.pdf`
   - 或你的论文: `https://arxiv.org/pdf/2602.06521.pdf`

2. **查看论文列表**
   - 访问首页应该能看到添加的论文

3. **测试完整功能**
   - 论文详情页
   - 添加分析记录
   - 创建关联关系
   - 查看关系图

---

## 💡 提示

- 环境变量更改后，**必须重新部署**才能生效
- 可以在Vercel的 **Settings** → **Environment Variables** 中随时修改
- 建议保存一份环境变量的备份（不包括在Git中）

**配置完成后，请告诉我测试结果！** 🚀
