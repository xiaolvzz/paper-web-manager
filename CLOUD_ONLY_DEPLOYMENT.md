# ☁️ 纯云端部署指南（无需本地环境）

**适合人群**：不想安装任何本地环境，直接使用云端服务

**总耗时**：约15分钟

**成本**：完全免费（¥0/月）

---

## 第一步：注册Supabase（5分钟）

### 1. 访问并注册

打开浏览器：https://supabase.com/

- 点击 "Start your project"
- 使用GitHub账号登录（推荐）或邮箱注册

### 2. 创建数据库项目

点击 "New Project"，填写：

| 字段 | 填写内容 |
|------|---------|
| **Name** | `paper-manager` |
| **Database Password** | 点击"Generate"自动生成 |
| **Region** | 选择 `Singapore` 或 `Tokyo` |

点击 "Create new project"，等待1-2分钟。

### 3. 初始化数据库表

项目创建完成后：

1. 左侧点击 "SQL Editor"
2. 点击 "New query"
3. 访问项目GitHub：`https://github.com/YOUR_USERNAME/paper-web-manager`
4. 打开 `database_schema.sql` 文件
5. 复制全部内容到Supabase SQL编辑器
6. 点击 "Run" 执行

**验证**：左侧"Table Editor"中看到3个表（papers、analysis、relations）

### 4. 创建存储桶

1. 左侧点击 "Storage"
2. 点击 "Create a new bucket"
3. 填写：
   - Name: `framework-images`
   - Public bucket: ✅ 勾选
4. 点击 "Create bucket"

### 5. 获取API密钥

1. 左侧点击 "Settings" → "API"
2. **记录**（后面会用到）：
   - ✅ **Project URL**：`https://xxxxx.supabase.co`
   - ✅ **anon public key**：一长串字符

---

## 第二步：推送代码到GitHub（3分钟）

### 如果您已有代码在本地：

```bash
cd paper_web_manager

# 初始化Git
git init
git add .
git commit -m "Initial commit"

# 创建GitHub仓库后推送
git remote add origin https://github.com/YOUR_USERNAME/paper-web-manager.git
git branch -M main
git push -u origin main
```

### 如果没有本地代码：

1. 访问GitHub：https://github.com/
2. 点击 "New repository"
3. 填写：
   - Repository name: `paper-web-manager`
   - Public（公开）
4. 点击 "Create repository"
5. 将项目代码上传到GitHub（可以通过GitHub网页界面上传文件）

---

## 第三步：部署到Vercel（5分钟）

### 1. 访问Vercel

打开：https://vercel.com/

- 点击 "Sign Up"
- 使用GitHub账号登录

### 2. 导入项目

1. 点击 "Add New..." → "Project"
2. 找到并选择 `paper-web-manager` 仓库
3. 点击 "Import"

### 3. 配置项目

在 "Configure Project" 页面：

**Framework Preset**：选择 "Other"（或不选）

**Root Directory**：`.`（默认即可）

### 4. 配置环境变量 ⚠️ 重要

展开 "Environment Variables"，添加：

| Name | Value |
|------|-------|
| `SUPABASE_URL` | 粘贴你的Supabase Project URL |
| `SUPABASE_KEY` | 粘贴你的Supabase anon public key |

**提示**：这些值就是第一步第5点记录的。

### 5. 部署

点击 "Deploy" 按钮，等待1-2分钟。

### 6. 完成！

部署成功后，Vercel会提供一个免费域名：

```
https://paper-web-manager.vercel.app
```

---

## 第四步：访问和使用（2分钟）

### 1. 打开你的网站

访问Vercel提供的域名（类似 `https://xxx.vercel.app`）

### 2. 添加第一篇论文

点击 "添加论文"，填写示例：

```
标题：Attention Is All You Need
作者：Ashish Vaswani, Noam Shazeer, Niki Parmar
年份：2017
标签：Transformer, NLP
PDF路径：https://arxiv.org/pdf/1706.03762.pdf
摘要：The dominant sequence transduction models are based on...
```

点击"添加"，论文会自动保存到云端数据库！

### 3. 测试功能

- ✅ 查看论文详情
- ✅ 添加分析记录
- ✅ 上传框架图
- ✅ 建立论文关联
- ✅ 查看关系图

### 4. 多设备访问

现在你可以在：
- 🖥️ 办公室电脑
- 💻 家里笔记本
- 📱 手机浏览器

随时访问这个网址，数据完全同步！

---

## 🎉 部署完成！

现在你拥有了一个：

✅ **完全免费**的云端论文管理系统
✅ **自动备份**（Supabase每天自动备份）
✅ **全球加速**（Vercel CDN）
✅ **多设备同步**（随时随地访问）

---

## 💡 后续操作

### 更新代码

修改代码后，只需推送到GitHub：

```bash
git add .
git commit -m "Update: 功能描述"
git push
```

Vercel会自动检测更新并重新部署（约1分钟）。

### 自定义域名（可选）

如果你有自己的域名：

1. 在Vercel项目设置中点击 "Domains"
2. 添加你的域名
3. 按照提示配置DNS记录

### 查看访问统计

在Vercel控制台可以看到：
- 访问次数
- 响应时间
- 错误日志

---

## ❓ 常见问题

**Q: 需要支付费用吗？**
A: 不需要！Supabase和Vercel的免费额度完全够个人使用。

**Q: 数据安全吗？**
A: 非常安全。Supabase使用企业级PostgreSQL，每天自动备份。

**Q: 能支持多少论文？**
A: Supabase免费版有500MB存储，可以存储数千篇论文的信息。

**Q: 访问速度快吗？**
A: 很快。Vercel提供全球CDN，国内访问速度也不错。

**Q: 如果超过免费额度会怎样？**
A: 系统会提示，你可以选择升级或清理旧数据。但正常个人使用不会超。

**Q: 可以备份数据吗？**
A: 可以。在Supabase SQL编辑器中可以导出所有数据。

---

## 🆘 遇到问题？

### 部署失败

检查：
- GitHub仓库是否public
- 环境变量是否正确填写
- Vercel日志中的错误信息

### 无法访问

检查：
- Vercel域名是否正确
- 浏览器是否能访问Vercel服务（可能需要科学上网）

### 数据库连接失败

检查：
- Supabase项目是否正常运行
- API密钥是否正确复制（注意不要有空格）
- 数据库表是否已创建

---

## 📧 技术支持

- Supabase文档：https://supabase.com/docs
- Vercel文档：https://vercel.com/docs

---

恭喜！你现在拥有了一个专业的云端论文管理系统！🎉📚
