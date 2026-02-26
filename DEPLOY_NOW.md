# 🚀 立即部署 - 跟我一起做

代码已经准备好！现在跟着我一步步操作。

---

## ✅ 第一步：创建GitHub仓库（3分钟）

### 1.1 打开GitHub

在浏览器中打开：**https://github.com/new**

（如果还没登录，先登录GitHub账号。没有账号？点击Sign Up注册）

### 1.2 填写仓库信息

| 字段 | 填写内容 |
|------|---------|
| **Repository name** | `paper-web-manager` |
| **Description** | 个人论文管理系统 |
| **Public/Private** | ✅ 选择 **Public** |
| **Initialize...** | ❌ 全部不勾选 |

### 1.3 点击 "Create repository"

创建完成后，GitHub会显示一个页面，上面有很多命令。**先不管它**，继续下一步。

### 1.4 回到终端，推送代码

**复制下面的命令，替换 `YOUR_USERNAME` 为你的GitHub用户名，然后执行：**

```bash
# 替换YOUR_USERNAME为你的GitHub用户名
git remote add origin https://github.com/YOUR_USERNAME/paper-web-manager.git
git branch -M main
git push -u origin main
```

**提示**：如果要求输入用户名密码，GitHub现在要求使用Personal Access Token。

**快速获取Token**：
1. 访问：https://github.com/settings/tokens
2. 点击 "Generate new token" → "Generate new token (classic)"
3. 勾选 `repo` 权限
4. 点击 "Generate token"
5. 复制生成的token（形如：`ghp_xxxxxxxxxxxx`）
6. 在终端输入：用户名用你的GitHub用户名，密码用刚才的token

---

## ✅ 第二步：配置Supabase数据库（5分钟）

### 2.1 注册Supabase

在浏览器中打开：**https://supabase.com/**

点击 **"Start your project"**

使用GitHub账号登录（推荐）或邮箱注册

### 2.2 创建项目

登录后，点击 **"New Project"**

填写以下信息：

| 字段 | 填写内容 |
|------|---------|
| **Name** | `paper-manager` |
| **Database Password** | 点击 "Generate a password" 自动生成 |
| **Region** | 选择 `Singapore` 或 `Tokyo` |

点击 **"Create new project"**，等待1-2分钟初始化。

### 2.3 执行数据库脚本

项目创建完成后：

1. **左侧菜单** → 点击 **"SQL Editor"**
2. 点击 **"New query"**
3. 在新标签页打开你的GitHub仓库：
   ```
   https://github.com/YOUR_USERNAME/paper-web-manager
   ```
4. 找到并点击 **`database_schema.sql`** 文件
5. 点击 **"Copy raw file"** 按钮（或者手动复制全部内容）
6. 回到Supabase，粘贴到SQL编辑器
7. 点击 **"Run"** 按钮（右下角）

**验证**：左侧 **"Table Editor"** 中应该能看到3个表：
- ✅ papers
- ✅ analysis
- ✅ relations

如果看到了，说明成功！

### 2.4 创建存储桶

1. **左侧菜单** → 点击 **"Storage"**
2. 点击 **"Create a new bucket"**
3. 填写：
   - **Name**: `framework-images`
   - **Public bucket**: ✅ **必须勾选**（重要！）
4. 点击 **"Create bucket"**

### 2.5 获取API密钥（重要！）

1. **左侧菜单** → 点击 **"Settings"** → **"API"**
2. 在 "Project API keys" 部分，找到并复制：

**📋 请复制并保存以下两个值（后面会用）：**

```
Project URL: https://xxxxxxxx.supabase.co
anon public key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.ey...（很长）
```

**提示**：点击每个值旁边的复制按钮即可。

---

## ✅ 第三步：部署到Vercel（5分钟）

### 3.1 注册Vercel

在浏览器中打开：**https://vercel.com/signup**

点击 **"Continue with GitHub"**（使用GitHub登录）

### 3.2 导入项目

1. 登录后，点击 **"Add New..."** → **"Project"**
2. 在仓库列表中找到 **`paper-web-manager`**
   - 如果没看到，点击 "Adjust GitHub App Permissions" 授权
3. 点击 **"Import"**

### 3.3 配置项目

在 "Configure Project" 页面：

| 字段 | 设置 |
|------|------|
| **Framework Preset** | 选择 "Other" |
| **Root Directory** | `.` （默认，不用改） |
| **Build Command** | 留空（不用填） |
| **Output Directory** | 留空（不用填） |

### 3.4 配置环境变量（关键步骤！）

向下滚动，展开 **"Environment Variables"**

添加以下两个变量：

**第一个变量：**
- **Name**: `SUPABASE_URL`
- **Value**: 粘贴刚才从Supabase复制的 Project URL

**第二个变量：**
- **Name**: `SUPABASE_KEY`
- **Value**: 粘贴刚才从Supabase复制的 anon public key

**注意**：确保没有多余的空格！

### 3.5 部署

点击 **"Deploy"** 按钮

等待1-2分钟，Vercel会自动构建和部署。

**成功标志**：看到🎉图标和 "Congratulations!" 消息

### 3.6 获取网站地址

部署成功后，Vercel会显示你的网站地址：

```
https://paper-web-manager-xxxx.vercel.app
```

**点击这个地址**，应该能打开你的论文管理系统了！

---

## ✅ 第四步：测试功能（3分钟）

### 4.1 访问网站

打开Vercel提供的网址（形如 `https://xxx.vercel.app`）

应该能看到论文管理系统的首页！

### 4.2 添加第一篇论文

点击 **"添加论文"** 按钮，填写测试数据：

```
标题：Attention Is All You Need
作者：Ashish Vaswani, Noam Shazeer, Niki Parmar
年份：2017
标签：Transformer, NLP, Deep Learning
PDF路径：https://arxiv.org/pdf/1706.03762.pdf
摘要：The dominant sequence transduction models are based on complex recurrent or convolutional neural networks...
```

点击 **"添加"**

如果成功保存，说明一切正常！🎉

### 4.3 测试其他功能

- ✅ 点击论文标题进入详情页
- ✅ 填写创新点分析
- ✅ 上传框架图（随便找个图片）
- ✅ 添加个人备注
- ✅ 点击"保存分析"
- ✅ 添加第二篇论文
- ✅ 建立关联关系
- ✅ 查看关系图

---

## 🎉 部署完成！

现在你拥有了一个：

✅ **完全免费**的云端论文管理系统
✅ **自动备份**的数据库
✅ **全球CDN**加速
✅ **多设备同步**（办公室、家里、手机都能访问）

**你的网站地址**：`https://xxx.vercel.app`

保存这个地址，随时随地访问！

---

## 🔧 后续操作

### 绑定自定义域名（可选）

如果你有域名：

1. Vercel项目设置 → Domains
2. 添加你的域名
3. 按提示配置DNS

### 更新代码

修改代码后：

```bash
git add .
git commit -m "Update: 描述修改内容"
git push
```

Vercel会自动重新部署（约1分钟）。

---

## ❓ 遇到问题？

### GitHub推送失败

- 检查是否使用Personal Access Token而不是密码
- 确认token有repo权限

### Vercel部署失败

- 检查环境变量是否正确配置
- 查看Vercel部署日志中的错误信息

### 无法连接数据库

- 确认Supabase URL和Key正确
- 确认没有多余的空格
- 确认数据库表已创建

### 图片上传失败

- 确认Storage桶 `framework-images` 已创建
- 确认桶设置为Public

---

## 💡 小贴士

1. **书签你的网站**：添加到浏览器收藏夹
2. **手机也能用**：手机浏览器访问同样的地址
3. **分享给朋友**：如果需要，可以分享网址
4. **定期备份**：Supabase自动每天备份，也可以手动导出数据

---

祝你使用愉快！📚✨
