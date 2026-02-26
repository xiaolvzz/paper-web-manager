# 🚀 本地测试完整指南

由于当前环境Python版本较旧(3.7)，我们使用Docker来运行项目。

---

## 第一步：注册Supabase（5分钟）

### 1. 访问Supabase官网

打开浏览器访问：https://supabase.com/

### 2. 注册账号

- 点击 "Start your project"
- 可以使用GitHub账号直接登录（推荐）

### 3. 创建项目

- 点击 "New Project"
- 填写：
  - **Name**: `paper-manager`（项目名称）
  - **Database Password**: 点击"Generate a password"自动生成
  - **Region**: 选择 `Singapore` 或 `Tokyo`（离国内近，速度快）
- 点击 "Create new project"
- 等待1-2分钟项目初始化完成

### 4. 初始化数据库表

项目创建完成后：

1. 左侧菜单点击 **"SQL Editor"**
2. 点击 "New query"
3. 打开项目中的 `database_schema.sql` 文件
4. 复制全部内容到SQL编辑器
5. 点击 "Run" 执行

执行成功后，左侧 "Table Editor" 中会显示3个表：
- `papers` （论文表）
- `analysis` （分析表）
- `relations` （关系表）

### 5. 创建存储桶（用于框架图）

1. 左侧菜单点击 **"Storage"**
2. 点击 "Create a new bucket"
3. 填写：
   - **Name**: `framework-images`
   - **Public bucket**: ✅ 勾选（允许公开访问）
4. 点击 "Create bucket"

### 6. 获取API密钥

1. 左侧菜单点击 **"Settings"** → **"API"**
2. 记录以下信息：
   - **Project URL**: 类似 `https://xxxxx.supabase.co`
   - **anon public key**: 一长串字符（点击复制按钮）

---

## 第二步：配置环境变量（1分钟）

编辑项目根目录的 `.env` 文件：

```bash
# 打开编辑器
nano .env

# 或
vi .env
```

将刚才获取的信息填入：

```
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=你的anon_public_key
APP_ENV=development
```

保存并退出（nano: Ctrl+O, Enter, Ctrl+X）

---

## 第三步：使用Docker启动（2分钟）

### 构建Docker镜像

```bash
cd /mnt/data/ws_backup/paper_web_manager
docker build -t paper-manager .
```

第一次构建约需1-2分钟，会自动安装Python 3.10和所有依赖。

### 启动容器

```bash
docker run -d \
  -p 8000:8000 \
  -v $(pwd):/app \
  -e SUPABASE_URL=$(grep SUPABASE_URL .env | cut -d '=' -f2) \
  -e SUPABASE_KEY=$(grep SUPABASE_KEY .env | cut -d '=' -f2) \
  --name paper-manager \
  paper-manager
```

### 查看日志（确认启动成功）

```bash
docker logs -f paper-manager
```

看到以下内容表示启动成功：
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

按 `Ctrl+C` 退出日志查看。

---

## 第四步：访问和测试（3分钟）

### 1. 打开浏览器

访问：http://localhost:8000

应该能看到论文管理系统的首页。

### 2. 添加第一篇论文

- 点击 "添加论文" 按钮
- 填写示例：
  ```
  标题：Attention Is All You Need
  作者：Ashish Vaswani, Noam Shazeer, Niki Parmar
  年份：2017
  标签：Transformer, NLP, Deep Learning
  PDF路径：https://arxiv.org/pdf/1706.03762.pdf
  摘要：The dominant sequence transduction models...
  ```
- 点击"添加"

### 3. 查看论文详情

- 点击论文标题进入详情页
- 测试功能：
  - ✅ 填写创新点分析
  - ✅ 上传框架图（可以随便找个图片测试）
  - ✅ 添加个人备注
  - ✅ 点击"保存分析"

### 4. 添加更多论文并建立关联

- 返回首页，再添加一篇论文
- 在第二篇论文详情页点击"添加关联"
- 选择第一篇论文，建立关联关系

### 5. 查看关系图

- 点击导航栏的"关系图"
- 应该能看到两篇论文的关联图谱
- 可以拖拽节点，缩放图形

---

## 常用Docker命令

```bash
# 查看容器状态
docker ps

# 查看日志
docker logs -f paper-manager

# 停止容器
docker stop paper-manager

# 启动容器
docker start paper-manager

# 删除容器
docker rm -f paper-manager

# 重新构建镜像（修改代码后）
docker build -t paper-manager .
docker rm -f paper-manager
docker run -d -p 8000:8000 -v $(pwd):/app --name paper-manager paper-manager
```

---

## 故障排查

### 问题1：端口8000已被占用

```bash
# 查看占用端口的进程
lsof -i :8000

# 杀死进程或使用其他端口
docker run -d -p 8080:8000 ...  # 改用8080端口
```

### 问题2：Docker权限问题

```bash
# 添加当前用户到docker组
sudo usermod -aG docker $USER
# 重新登录或重启终端
```

### 问题3：无法连接数据库

检查：
- `.env` 文件是否正确配置
- Supabase项目是否正常运行
- 网络连接是否正常

### 问题4：前端页面空白

打开浏览器开发者工具（F12），查看Console是否有错误。

---

## 📊 成功标志

如果以下功能都正常，说明环境搭建成功：

- ✅ 能访问首页并看到界面
- ✅ 能添加论文并保存到数据库
- ✅ 能查看论文详情
- ✅ 能上传框架图
- ✅ 能建立关联关系
- ✅ 能查看关系图可视化

---

## 🎉 下一步

环境搭建完成后，可以：

1. **日常使用**：随时添加论文和分析记录
2. **云端部署**：参考 `DEPLOYMENT_GUIDE.md` 部署到Vercel
3. **功能扩展**：添加LLM集成等高级功能

祝使用愉快！📚✨
