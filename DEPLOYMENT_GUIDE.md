# 🚀 部署指南

本指南将帮助您完全免费地部署论文管理系统到云端。

## 📋 前置要求

- GitHub账号（用于托管代码）
- Supabase账号（免费PostgreSQL数据库）
- Vercel账号（免费Web托管）

---

## 第一步：创建Supabase数据库

### 1.1 注册Supabase

访问 https://supabase.com/ 并注册账号（可以用GitHub登录）

### 1.2 创建项目

1. 点击 "New Project"
2. 填写项目信息：
   - **Name**: paper-manager（项目名称）
   - **Database Password**: 自动生成或自定义
   - **Region**: 选择离你最近的区域（如Singapore）
3. 点击 "Create new project"，等待1-2分钟

### 1.3 初始化数据库表

1. 在项目页面左侧点击 "SQL Editor"
2. 点击 "New query"
3. 复制 `database_schema.sql` 文件的全部内容
4. 粘贴到SQL编辑器中
5. 点击 "Run" 执行SQL

执行成功后，在左侧 "Table Editor" 中应该能看到3个表：
- papers
- analysis
- relations

### 1.4 创建存储桶（用于框架图）

1. 左侧点击 "Storage"
2. 点击 "Create a new bucket"
3. 填写：
   - **Name**: framework-images
   - **Public bucket**: 勾选（允许公开访问）
4. 点击 "Create bucket"

### 1.5 获取API密钥

1. 左侧点击 "Settings" → "API"
2. 记录以下信息（后面会用到）：
   - **Project URL**: `https://xxx.supabase.co`
   - **anon public key**: 一长串字符

---

## 第二步：准备代码仓库

### 2.1 推送代码到GitHub

```bash
cd paper_web_manager

# 初始化Git仓库
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: Paper Management System"

# 连接到GitHub（需要先在GitHub创建仓库）
git remote add origin https://github.com/YOUR_USERNAME/paper-web-manager.git

# 推送
git push -u origin main
```

### 2.2 在GitHub创建仓库

1. 访问 https://github.com/new
2. 填写仓库名：`paper-web-manager`
3. 选择 Public 或 Private
4. 不要勾选任何初始化选项
5. 点击 "Create repository"
6. 按照页面提示执行推送命令

---

## 第三步：部署到Vercel

### 3.1 注册Vercel

访问 https://vercel.com/ 并用GitHub账号登录

### 3.2 导入项目

1. 点击 "Add New..." → "Project"
2. 选择刚才创建的 `paper-web-manager` 仓库
3. 点击 "Import"

### 3.3 配置环境变量

在 "Configure Project" 页面：

1. 展开 "Environment Variables"
2. 添加以下变量：

| Name | Value |
|------|-------|
| `SUPABASE_URL` | 从Supabase复制的Project URL |
| `SUPABASE_KEY` | 从Supabase复制的anon public key |

### 3.4 部署

1. 点击 "Deploy"
2. 等待1-2分钟部署完成
3. 部署成功后，Vercel会提供一个域名，如：`https://paper-web-manager.vercel.app`

---

## 第四步：访问和使用

### 4.1 首次访问

打开Vercel提供的域名，应该能看到论文管理系统的首页。

### 4.2 添加第一篇论文

1. 点击 "添加论文"
2. 填写论文信息
3. 保存

### 4.3 测试功能

- ✅ 论文列表显示
- ✅ 搜索和筛选
- ✅ 论文详情页
- ✅ 添加分析记录
- ✅ 上传框架图
- ✅ 建立关联关系
- ✅ 查看关系图

---

## 🎉 完成！

现在你拥有了一个完全免费、多设备同步的论文管理系统！

### 访问方式

- **电脑**：直接访问Vercel域名
- **手机/平板**：同样访问该域名，响应式设计自动适配

### 自定义域名（可选）

如果你有自己的域名：

1. 在Vercel项目设置中点击 "Domains"
2. 添加你的域名
3. 按照提示配置DNS记录

---

## 🔧 故障排查

### 问题1：部署失败

- 检查 `requirements.txt` 是否正确
- 查看Vercel部署日志

### 问题2：数据库连接失败

- 检查环境变量是否正确设置
- 确认Supabase项目状态正常

### 问题3：图片上传失败

- 确认Storage桶已创建且设置为Public
- 检查桶名称是否为 `framework-images`

### 问题4：页面空白

- 打开浏览器开发者工具（F12）查看控制台错误
- 检查API请求是否正常

---

## 📊 免费额度说明

### Supabase（免费版）
- ✅ 500MB数据库存储
- ✅ 1GB文件存储
- ✅ 50,000次请求/月
- ✅ 自动备份

### Vercel（免费版）
- ✅ 无限次部署
- ✅ 100GB带宽/月
- ✅ 全球CDN加速
- ✅ 自动HTTPS

**对于个人使用完全足够！**

---

## 🔄 更新部署

修改代码后，只需推送到GitHub：

```bash
git add .
git commit -m "Update: 功能描述"
git push
```

Vercel会自动检测更新并重新部署（约1分钟）。

---

## 💡 提示

1. 定期备份数据库（Supabase自动每天备份）
2. 使用标签组织论文（便于筛选）
3. 及时添加分析记录（避免遗忘）
4. 善用关系图发现论文间的联系

祝使用愉快！📚✨

---

## 🆕 2026-02-27 更新说明

### 本次更新内容

#### 1. 修复Vercel部署问题
- 移除TestClient，使用原生ASGI处理（修复API 404和返回HTML问题）
- 优化路由配置

#### 2. 新增字段
- **GitHub链接**：可以为每篇论文添加对应的GitHub代码仓库
- **研究领域**：支持NLP、CV、RL、ML、Robotics等领域分类

#### 3. AI助手功能
- 使用Groq免费API生成中文论文摘要
- 自动提取论文创新点
- 一键复制到分析区

### 更新部署步骤

#### 步骤A：执行数据库迁移

在Supabase SQL Editor中执行以下SQL：

```sql
-- 添加新字段
ALTER TABLE papers ADD COLUMN IF NOT EXISTS github_url TEXT;
ALTER TABLE papers ADD COLUMN IF NOT EXISTS domain TEXT;

-- 添加索引
CREATE INDEX IF NOT EXISTS idx_papers_domain ON papers(domain);
```

#### 步骤B：配置Groq API Key（可选）

AI助手功能需要Groq API Key：

1. 访问 https://console.groq.com 注册（免费）
2. 创建API Key
3. 在Vercel项目设置 → Environment Variables 中添加：
   - 变量名：`GROQ_API_KEY`
   - 变量值：你的API key

#### 步骤C：推送代码并部署

```bash
git add .
git commit -m "fix: 修复部署问题并添加新功能"
git push
```

Vercel会自动重新部署（约1-2分钟）。

### 新功能使用指南

#### 使用GitHub链接字段
在添加论文时，填写"GitHub代码链接"输入框，保存后会在论文列表和详情页显示。

#### 使用研究领域分类
选择论文的研究领域，列表页会在标题旁显示领域badge，方便筛选。

#### 使用AI助手
1. 进入论文详情页
2. 点击"生成中文摘要"或"提取创新点"
3. AI会在几秒内返回结果
4. 点击"复制到分析区"可以将AI输出复制到创新点分析框

**注意：** AI功能需要配置GROQ_API_KEY环境变量。
