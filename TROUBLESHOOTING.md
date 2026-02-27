# 🔧 部署故障排查指南

## 快速诊断

### 步骤1：检查Vercel部署状态

访问你的Vercel Dashboard：
1. 进入 https://vercel.com/dashboard
2. 选择 `paper-web-manager` 项目
3. 查看最新的部署状态（应该显示"Building"或"Ready"）

#### 如果显示"Failed"（失败）
点击失败的部署，查看构建日志。常见问题：

**问题A：Python依赖安装失败**
```
Error: Could not find a version that satisfies the requirement...
```
- 检查 `api/requirements.txt` 是否有拼写错误
- 确认所有包都存在于PyPI

**问题B：导入错误**
```
ModuleNotFoundError: No module named 'backend'
```
- 检查 `api/index.py` 的路径设置是否正确
- 确认 `backend/` 目录存在

**问题C：Mangum错误**
```
Error: handler is not callable
```
- 检查 `api/index.py` 是否正确导出了handler

### 步骤2：测试API端点

部署成功后，使用curl或浏览器测试：

```bash
# 测试健康检查（应该返回JSON）
curl https://your-app.vercel.app/api/health

# 测试论文列表（应该返回JSON数组）
curl https://your-app.vercel.app/api/papers
```

**预期响应：**
```json
{
  "status": "healthy",
  "message": "论文管理系统运行正常",
  "environment": "vercel"
}
```

**如果返回HTML或404：**
- 检查vercel.json的rewrites配置
- 确认api/index.py正确导出了handler
- 查看Vercel部署日志

### 步骤3：检查环境变量

在Vercel项目设置中确认环境变量：

**必需的环境变量：**
- ✅ `SUPABASE_URL` - Supabase项目URL
- ✅ `SUPABASE_KEY` - Supabase anon public key

**可选的环境变量：**
- ⭕ `GROQ_API_KEY` - AI功能需要（可选）

**如何检查：**
1. Vercel Dashboard → Settings → Environment Variables
2. 确认变量名拼写正确（区分大小写）
3. 确认变量值没有多余的空格

## 常见问题解决

### 问题1：API返回HTML而不是JSON

**症状：**
```bash
curl https://your-app.vercel.app/api/papers
# 返回：<!DOCTYPE html>...
```

**原因：** API路由未正确匹配，返回了前端页面

**解决方案：**
1. 检查 `api/index.py` 是否正确导出handler
2. 检查 `vercel.json` 的rewrites配置
3. 确认 `backend/main.py` 有 `root_path="/api"`

### 问题2：POST请求返回404

**症状：**
```bash
curl -X POST https://your-app.vercel.app/api/papers/ -d '{...}'
# 返回：404 Not Found
```

**原因：** 路由匹配问题或handler未正确处理POST请求

**解决方案：**
- 确认使用了Mangum适配器（已在最新代码中添加）
- 检查URL末尾的斜杠：`/api/papers/` vs `/api/papers`
- 查看Vercel Function日志

### 问题3：500 Internal Server Error

**症状：**
API返回500错误

**可能原因：**
1. 数据库连接失败（环境变量配置错误）
2. 代码运行时错误
3. 依赖包版本不兼容

**解决方案：**
1. 检查Vercel Function日志
2. 验证环境变量
3. 测试本地是否能运行：
```bash
cd /mnt/data/ws_backup/paper_web_manager
python -m uvicorn backend.main:app --reload
```

### 问题4：AI功能不可用

**症状：**
点击"生成中文摘要"返回错误

**可能原因：**
- 未配置GROQ_API_KEY
- API key无效
- Groq服务限流

**解决方案：**
1. 检查 `https://your-app.vercel.app/api/ai/health`
2. 预期响应：
```json
{
  "status": "healthy",
  "provider": "Groq",
  "configured": true
}
```
3. 如果`configured: false`，需要添加GROQ_API_KEY环境变量

## 调试工具

### 1. Vercel CLI（推荐安装）

```bash
npm i -g vercel

# 查看部署列表
vercel ls

# 查看最新部署日志
vercel logs

# 本地测试（模拟Vercel环境）
vercel dev
```

### 2. 浏览器开发者工具

1. 打开浏览器（Chrome/Firefox）
2. 按F12打开开发者工具
3. 切换到"Network"标签
4. 尝试添加论文
5. 查看失败的请求：
   - 状态码
   - 响应内容
   - 请求payload

### 3. 测试页面

访问 `https://your-app.vercel.app/test-add` 自动测试所有API端点。

## 配置验证清单

### Vercel配置
- [ ] vercel.json存在且格式正确
- [ ] api/index.py导出handler
- [ ] api/requirements.txt包含所有依赖
- [ ] 环境变量已配置

### Supabase配置
- [ ] 数据库迁移已执行
- [ ] papers表有github_url和domain列
- [ ] API密钥有效

### GitHub配置
- [ ] 代码已推送到main分支
- [ ] Vercel已连接到GitHub仓库
- [ ] 自动部署已启用

## 回滚方案

如果新版本有问题，快速回滚到上一个版本：

```bash
# 查看提交历史
git log --oneline -10

# 回滚到之前的提交
git reset --hard c90d538  # 替换为上一个工作版本的commit hash

# 强制推送（触发Vercel重新部署）
git push --force
```

**注意：** 强制推送前请确认这是必要的。

## 联系支持

如果以上方法都无法解决问题：

1. **Vercel支持：** https://vercel.com/support
2. **Supabase支持：** https://supabase.com/support
3. **项目Issues：** https://github.com/xiaolvzz/paper-web-manager/issues

## 最新修复（2026-02-27）

### 关键修改
- ✅ 添加Mangum适配器（FastAPI → Serverless Functions）
- ✅ 使用rewrites配置（更稳定）
- ✅ 简化api/index.py代码

### 验证命令

```bash
# 测试健康检查
curl https://your-app.vercel.app/api/health

# 测试论文列表
curl https://your-app.vercel.app/api/papers

# 测试创建论文
curl -X POST https://your-app.vercel.app/api/papers/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Paper","authors":"Test Author"}'

# 测试AI健康检查
curl https://your-app.vercel.app/api/ai/health
```

所有端点都应该返回JSON格式的响应。

## 部署时间线

通常Vercel部署需要：
- ⏱️ 构建：30-60秒
- ⏱️ 部署：10-30秒
- ⏱️ 总计：1-2分钟

推送代码后，等待2分钟再测试API。
