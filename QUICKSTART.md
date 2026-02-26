# 🚀 快速开始

## 方式一：本地测试运行（5分钟）

### 1. 安装依赖

```bash
cd paper_web_manager
pip install -r requirements.txt
```

### 2. 配置Supabase

如果还没有Supabase账号：

1. 访问 https://supabase.com/ 注册（免费）
2. 创建新项目（1-2分钟）
3. 在SQL编辑器中执行 `database_schema.sql`
4. 创建存储桶 `framework-images`（设置为Public）
5. 获取Project URL和anon key

### 3. 配置环境变量

```bash
# 复制配置文件
cp .env.example .env

# 编辑.env文件，填入Supabase信息
# SUPABASE_URL=https://xxx.supabase.co
# SUPABASE_KEY=your_anon_key
```

### 4. 启动服务

```bash
# 开发模式
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. 访问

打开浏览器访问：http://localhost:8000

---

## 方式二：云端部署（15分钟）

详细步骤请查看 [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)

简要步骤：
1. ✅ 创建Supabase项目（2分钟）
2. ✅ 推送代码到GitHub（3分钟）
3. ✅ 在Vercel导入项目（5分钟）
4. ✅ 配置环境变量并部署（5分钟）

---

## 💡 使用提示

### 添加第一篇论文

```
标题：Attention Is All You Need
作者：Ashish Vaswani, Noam Shazeer
年份：2017
标签：Transformer, NLP
PDF路径：https://arxiv.org/pdf/1706.03762.pdf
```

### 记录分析

在论文详情页：
- 填写创新点分析
- 上传论文框架图
- 添加个人备注

### 建立关联

1. 添加多篇论文
2. 在详情页点击"添加关联"
3. 选择关系类型
4. 在关系图页面查看可视化

---

## 📚 功能清单

- [x] 论文增删改查
- [x] 搜索和筛选
- [x] 分析记录（创新点、框架图、备注）
- [x] 关联关系（方法相似、问题相关、自定义）
- [x] 关系图可视化
- [x] 响应式设计（手机适配）
- [x] 多设备同步

---

## 🔧 技术架构

```
Frontend (Bootstrap 5 + Vanilla JS)
    ↓
FastAPI Backend (Python)
    ↓
PostgreSQL Database (Supabase)
    ↓
Supabase Storage (框架图存储)
```

---

## 📝 下一步扩展

想要添加更多功能？

1. **LLM集成**：自动提取论文创新点
   - 修改 `backend/routers/analysis.py`
   - 集成OpenAI/Claude API

2. **PDF预览**：在线查看PDF
   - 使用PDF.js库
   - 添加到详情页

3. **批量导入**：从BibTeX导入
   - 添加导入API
   - 解析BibTeX格式

4. **导出功能**：导出Markdown笔记
   - 添加导出按钮
   - 生成Markdown文件

---

## ❓ 常见问题

**Q: 本地运行时无法连接数据库？**
A: 检查 `.env` 文件是否正确配置，确认Supabase项目状态正常。

**Q: 图片上传失败？**
A: 确认Storage桶 `framework-images` 已创建且设置为Public。

**Q: 部署后页面空白？**
A: 检查Vercel环境变量是否正确配置。

**Q: 如何备份数据？**
A: Supabase自动每天备份。也可以在SQL编辑器导出数据。

---

## 💬 反馈

遇到问题或有建议？欢迎提Issue！

祝使用愉快！📚✨
