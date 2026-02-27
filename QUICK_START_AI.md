# 🚀 AI配置快速开始

## 方法1：手动配置（推荐公司使用）

编辑 `.env` 文件，添加你的API密钥：

```bash
# 添加Claude API密钥（你公司有的）
CLAUDE_API_KEY=sk-ant-api03-xxx...
CLAUDE_MODEL=claude-3-5-haiku-20241022

# 添加Gemini API密钥（你公司有的）
GEMINI_API_KEY=AIzaSy...
GEMINI_MODEL=gemini-2.0-flash-exp
```

然后重启应用：
```bash
# 本地开发
python -m uvicorn backend.main:app --reload

# Vercel部署
# 在Vercel项目设置中添加环境变量，然后重新部署
```

---

## 方法2：使用配置脚本（Linux/Mac）

```bash
./configure_ai.sh
```

按提示输入API密钥即可。

---

## 方法3：Vercel环境变量配置

1. 打开你的Vercel项目
2. Settings → Environment Variables
3. 添加变量：

```
Name: CLAUDE_API_KEY
Value: sk-ant-api03-xxx...

Name: GEMINI_API_KEY
Value: AIzaSy...
```

4. 重新部署项目

---

## ✅ 验证配置

启动应用后，查看日志会显示：

```
✓ 使用 Anthropic Claude claude-3-5-haiku-20241022
```

或访问：`https://your-app.vercel.app/api/health`

---

## 📊 推荐配置

### 如果你有Claude和Gemini API：

```bash
# 主力：Claude（质量最高）
CLAUDE_API_KEY=sk-ant-...
CLAUDE_MODEL=claude-3-5-haiku-20241022

# 备用：Gemini（免费，性能强）
GEMINI_API_KEY=AIzaSy...
GEMINI_MODEL=gemini-2.0-flash-exp
```

系统会优先使用Gemini（免费），节省Claude的成本。如果需要更高质量，可以只配置Claude。

### 如果只有Claude：

```bash
CLAUDE_API_KEY=sk-ant-...
CLAUDE_MODEL=claude-3-5-haiku-20241022
```

### 如果只有Gemini：

```bash
GEMINI_API_KEY=AIzaSy...
GEMINI_MODEL=gemini-2.0-flash-exp
```

Gemini 2.0 Flash完全免费，性能接近GPT-4，完全够用！

---

## 💡 成本优化建议

1. **优先使用免费模型**：Gemini、智谱AI GLM-4-Flash
2. **高质量任务用Claude**：代码分析、论文速读
3. **简单任务用便宜模型**：翻译可以用Gemini
4. **设置消费上限**：在API提供商后台设置

---

## 🔍 故障排查

### 问题：配置了但没生效

**解决**：
1. 检查.env文件格式（等号两边不要空格）
2. 重启应用
3. 查看日志确认使用的模型

### 问题：API报错

**解决**：
1. 检查API密钥是否正确
2. 检查账户是否有余额
3. 检查网络是否可以访问API

### 问题：想切换使用的模型

**解决**：
只配置你想用的模型的API密钥，删除或注释其他模型的配置。

---

## 📖 详细文档

查看 `AI_CONFIG_GUIDE.md` 获取完整的配置指南，包括：
- 所有模型的详细说明
- 价格对比
- 使用场景推荐
- 常见问题解答

---

## 需要帮助？

系统已内置6种AI模型支持，配置任意一个即可使用！

推荐：**Claude（公司）+ Gemini（免费备用）** 🎯
