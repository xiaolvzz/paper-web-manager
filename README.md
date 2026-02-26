# 📚 论文管理系统

一个完全免费的个人论文管理Web应用，支持多设备同步、关联关系管理和AI辅助分析。

---

## 🚀 快速开始

### 👉 推荐：纯云端部署（15分钟，无需本地环境）

**[点击这里查看详细指南 →](./CLOUD_ONLY_DEPLOYMENT.md)**

只需：注册Supabase → 推送代码到GitHub → Vercel部署 → 完成！

### 🔧 本地测试开发（需要Docker）

**[点击这里查看本地指南 →](./LOCAL_SETUP_GUIDE.md)**

---

## 📖 选择部署方式

**不确定选哪个？** 👉 **[START_HERE.md](./START_HERE.md)** - 帮你选择最合适的方案

---

## ✨ 功能特性

- **论文管理**：添加、编辑、删除论文，记录标题、作者、年份、摘要等信息
- **分析记录**：记录创新点分析、上传框架图、添加个人备注
- **关联关系**：建立论文间的关联（方法相似、问题相关、自定义关系）
- **关系图谱**：可视化展示论文间的关联关系网络
- **搜索筛选**：按标题、作者、年份、标签快速查找论文
- **多设备同步**：云端部署，随时随地访问

## 🚀 技术栈

- **后端**：FastAPI (Python)
- **前端**：Bootstrap 5 + Vanilla JavaScript
- **数据库**：PostgreSQL (Supabase)
- **文件存储**：Supabase Storage
- **部署**：Vercel (免费)

## 📦 本地开发

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env`，填入Supabase配置：

```bash
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
```

### 3. 初始化数据库

在Supabase SQL编辑器中执行 `database_schema.sql` 中的SQL语句。

### 4. 启动服务

```bash
# 开发模式（带热重载）
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# 或者直接运行
python -m backend.main
```

访问：http://localhost:8000

## ☁️ 云端部署（Vercel + Supabase）

### 步骤1：创建Supabase项目

1. 访问 https://supabase.com/
2. 注册并创建新项目（免费）
3. 在SQL编辑器中执行 `database_schema.sql`
4. 在Settings → Storage 中创建 `framework-images` 存储桶（公开访问）
5. 获取项目URL和anon key（Settings → API）

### 步骤2：部署到Vercel

1. 访问 https://vercel.com/
2. 导入GitHub仓库
3. 配置环境变量：
   - `SUPABASE_URL`：你的Supabase项目URL
   - `SUPABASE_KEY`：你的Supabase anon key
4. 点击部署

部署完成后，Vercel会提供一个免费域名访问你的应用。

## 📊 数据库结构

### papers（论文表）
- id, title, authors, year, pdf_path, abstract, tags
- created_at, updated_at

### analysis（分析记录表）
- id, paper_id（外键）
- innovation_points, framework_image, personal_notes
- created_at

### relations（关联关系表）
- id, paper_from_id, paper_to_id
- relation_type, description
- created_at

## 🎯 使用指南

### 添加论文

1. 点击首页"添加论文"按钮
2. 填写论文信息（标题必填）
3. PDF路径可以是：
   - 本地路径：`D:\Papers\paper.pdf`
   - 云盘链接：`https://arxiv.org/pdf/2301.12345.pdf`

### 记录分析

1. 在论文详情页填写创新点分析
2. 上传框架图（自动保存到云端）
3. 添加个人备注

### 建立关联

1. 在论文详情页点击"添加关联"
2. 选择要关联的论文
3. 选择关系类型并添加描述
4. 在关系图页面查看可视化图谱

## 🔧 开发规范

- 遵循KISS原则：代码简洁、避免过度设计
- 模块化：单一职责、低耦合
- 前后端分离：API RESTful设计

## 📝 TODO（后续扩展）

- [ ] LLM集成：自动提取论文创新点
- [ ] PDF在线预览
- [ ] 标注功能（高亮、笔记）
- [ ] 导出Markdown笔记
- [ ] 批量导入（从BibTeX）
- [ ] 多用户支持

## 📄 许可证

MIT License

## 🙋 问题反馈

如有问题或建议，请提Issue。
