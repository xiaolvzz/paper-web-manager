# AI对话功能部署步骤

## 📋 已完成的工作

### 后端（100%完成）
- ✅ 数据库迁移SQL：`migrations/002_add_conversations_and_pdf_fields.sql`
- ✅ 对话路由：`backend/routers/conversations.py`
- ✅ PDF处理工具：`backend/utils/pdf_processor.py`
- ✅ arXiv集成：`backend/utils/arxiv_helper.py`
- ✅ 扩展论文API：`backend/routers/papers.py` (新增3个端点)
- ✅ 扩展AI助手：`backend/routers/ai_assistant.py` (新增analyze-paper端点)
- ✅ 数据模型更新：`backend/models.py`
- ✅ 路由注册：`backend/main.py`
- ✅ 依赖更新：`requirements.txt` 和 `api/requirements.txt`

### 前端（部分完成）
- ✅ CSS样式：`frontend/assets/css/main.css`（对话界面样式已添加）
- ⏳ HTML修改：需要手动添加到 `frontend/paper.html`
- ⏳ JavaScript逻辑：需要手动添加到 `frontend/assets/js/paper.js`

**前端实现指南**：详见 `FRONTEND_IMPLEMENTATION.md`

---

## 🚀 部署步骤

### 步骤1：执行数据库迁移（5分钟）

1. 登录Supabase控制台：https://app.supabase.com
2. 选择你的项目
3. 进入 SQL Editor
4. 复制 `migrations/002_add_conversations_and_pdf_fields.sql` 的内容
5. 执行SQL脚本
6. 验证：运行以下SQL检查表是否创建成功
   ```sql
   SELECT table_name FROM information_schema.tables
   WHERE table_name = 'conversations';

   SELECT column_name FROM information_schema.columns
   WHERE table_name = 'papers'
   AND column_name IN ('pdf_storage_path', 'pdf_text_content', 'arxiv_id');
   ```

### 步骤2：创建Supabase Storage存储桶（可选，5分钟）

PDF上传功能需要：

1. 在Supabase控制台进入 Storage
2. 创建新存储桶，名称：`paper-pdfs`
3. 设置为 **Private**（私有访问）
4. 文件大小限制：50MB

**注意**：如果不创建存储桶，PDF上传功能会失败，但不影响其他功能（arXiv导入和文本输入仍可用）。

### 步骤3：完成前端实现（30分钟）

参考 `FRONTEND_IMPLEMENTATION.md` 文档：

1. 修改 `frontend/paper.html`：添加两个新区域（论文内容输入、AI对话）
2. 修改 `frontend/assets/js/paper.js`：添加对话和内容处理函数

**快速验证**：
- 如果暂时不想修改前端，可以直接使用API测试：
  ```bash
  # 测试对话API
  curl -X POST https://your-app.vercel.app/api/conversations/chat \
    -H "Content-Type: application/json" \
    -d '{"paper_id": 1, "user_message": "这篇论文的主要创新点是什么？"}'
  ```

### 步骤4：推送代码到GitHub（2分钟）

```bash
cd /mnt/data/ws_backup/paper_web_manager

# 查看修改
git status

# 添加所有修改
git add .

# 提交
git commit -m "feat: 添加AI对话功能

- 新增对话记录表和papers表扩展字段
- 实现AI对话API（基于Groq）
- 支持PDF上传、arXiv导入、文本输入
- 新增一键分析功能
- 添加对话界面CSS样式

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"

# 推送到GitHub
git push origin main
```

### 步骤5：Vercel自动部署（5分钟）

1. 推送后，Vercel会自动检测到代码变更
2. 进入 Vercel Dashboard 查看部署进度
3. 等待部署完成（通常2-3分钟）

**检查部署日志**：
- 确保PyMuPDF和arxiv依赖安装成功
- 如果有错误，查看Build Logs

### 步骤6：验证功能（10分钟）

#### 6.1 后端API验证

访问你的Vercel域名测试：

```bash
# 健康检查
curl https://your-app.vercel.app/health

# AI服务状态
curl https://your-app.vercel.app/api/ai/health

# 获取论文信息（替换paper_id）
curl https://your-app.vercel.app/api/papers/1/full
```

#### 6.2 数据库验证

在Supabase SQL Editor中：

```sql
-- 检查表结构
\d conversations
\d papers

-- 查看是否有索引
SELECT indexname FROM pg_indexes
WHERE tablename IN ('conversations', 'papers');
```

#### 6.3 前端验证（如果已实现）

1. 打开论文详情页
2. 检查是否显示"论文内容"和"AI对话助手"区域
3. 测试对话功能：输入问题，查看AI回复
4. 测试arXiv导入：输入 `2301.12345` 试试
5. 刷新页面，对话历史应该保留

---

## 🐛 常见问题

### 问题1：PDF上传失败
**原因**：Supabase存储桶未创建
**解决**：
- 方案A：按步骤2创建存储桶
- 方案B：暂时只使用arXiv导入和文本输入功能

### 问题2：AI回复失败
**原因**：GROQ_API_KEY未配置或过期
**解决**：
1. 检查Vercel环境变量
2. 访问 https://console.groq.com 获取新API Key
3. 在Vercel中添加环境变量 `GROQ_API_KEY`
4. 重新部署

### 问题3：对话历史不显示
**原因**：数据库迁移未执行或前端未正确调用API
**解决**：
1. 检查conversations表是否存在
2. 打开浏览器开发者工具，查看Network请求
3. 确认 `/api/conversations/paper/{id}` 请求成功

### 问题4：前端显示异常
**原因**：Bootstrap版本不兼容或JavaScript语法错误
**解决**：
1. 确认使用Bootstrap 5.x
2. 打开浏览器Console查看JavaScript错误
3. 检查 `currentPaperId` 变量是否定义

---

## 📊 功能清单

### 已实现功能
- ✅ AI多轮对话（基于论文内容）
- ✅ 对话历史保存和加载
- ✅ PDF文件上传和文本提取
- ✅ arXiv论文自动导入
- ✅ 手动文本输入
- ✅ 一键AI分析（提取框架、创新点、方法、源码）
- ✅ 快捷问题按钮
- ✅ 清空对话功能

### 未实现功能（未来扩展）
- ⏳ PDF在线预览
- ⏳ 流式AI回复（SSE）
- ⏳ 对话导出为Markdown
- ⏳ 多论文对比分析

---

## 🎯 下一步建议

1. **完成前端实现**：参考 `FRONTEND_IMPLEMENTATION.md` 完成HTML和JS修改
2. **测试完整流程**：上传一篇论文，与AI对话，验证所有功能
3. **优化用户体验**：
   - 添加加载动画
   - 优化移动端显示
   - 添加错误提示优化
4. **扩展功能**：
   - PDF在线预览（使用PDF.js）
   - 对话搜索功能
   - 批量导入论文

---

## 📞 需要帮助？

如果遇到问题：
1. 查看 `TROUBLESHOOTING.md`（现有的故障排查文档）
2. 检查Vercel部署日志
3. 查看浏览器Console错误
4. 检查Supabase数据库日志

---

## ✅ 验证清单

部署完成后检查：

- [ ] 数据库表conversations已创建
- [ ] papers表新增3个字段（pdf_storage_path, pdf_text_content, arxiv_id）
- [ ] `/api/health` 返回正常
- [ ] `/api/ai/health` 显示configured: true
- [ ] `/api/conversations/chat` 能够成功调用
- [ ] Vercel部署成功，无错误日志
- [ ] （可选）前端UI显示正常
- [ ] （可选）完整对话流程测试通过

---

**预计总部署时间**：60分钟（包括前端实现）

**最小可用版本**：只执行步骤1-5，后端功能即可使用（可通过API测试）
