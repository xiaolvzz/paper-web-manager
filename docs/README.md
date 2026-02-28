# 📚 AI配置文档导航

欢迎使用论文管理系统的AI功能！本目录包含所有AI模型的详细配置指南。

---

## 🚀 快速开始

### 我应该配置哪个模型？

#### 如果你在国内 → 智谱AI
👉 [智谱AI配置指南](ZHIPU_CONFIG.md)
- ✅ 完全免费
- ✅ 国内访问
- ✅ 中文理解强

#### 如果你在国外 → Gemini
👉 [Gemini配置指南](GEMINI_CONFIG.md)
- ✅ 完全免费
- ✅ 性能强大
- ✅ Google生态

#### 如果你有预算 → Claude
👉 [Claude配置指南](CLAUDE_CONFIG.md)
- ✅ 推理最强
- ✅ 代码理解好
- ⚠️ 需要付费

---

## 📖 详细配置文档

### 单个模型详细指南

| 模型 | 配置文档 | 特点 | 成本 |
|------|---------|------|------|
| **智谱AI GLM-4** | [ZHIPU_CONFIG.md](ZHIPU_CONFIG.md) | 免费，国内访问 | 免费 |
| **Google Gemini** | [GEMINI_CONFIG.md](GEMINI_CONFIG.md) | 免费，性能强 | 免费 |
| **Anthropic Claude** | [CLAUDE_CONFIG.md](CLAUDE_CONFIG.md) | 推理最强 | 付费 |
| **通义千问 Qwen** | [QWEN_CONFIG.md](QWEN_CONFIG.md) | 阿里云，便宜 | 付费 |

### 综合配置文档

| 文档 | 说明 |
|------|------|
| [API_KEYS_GUIDE.md](../API_KEYS_GUIDE.md) | 所有7个模型的完整配置指南 |
| [AI_QUICK_CONFIG.md](../AI_QUICK_CONFIG.md) | 快速配置索引（3分钟配置） |
| [GLOBAL_AI_SETTINGS.md](../GLOBAL_AI_SETTINGS.md) | 全局AI设置使用说明 |
| [AI_MODEL_SELECTOR.md](../AI_MODEL_SELECTOR.md) | 模型选择器详解 |
| [QUICK_START_AI.md](../QUICK_START_AI.md) | AI功能快速开始 |
| [AI_CONFIG_GUIDE.md](../AI_CONFIG_GUIDE.md) | 完整的AI配置指南 |

---

## 🎯 推荐配置方案

### 方案1：完全免费（个人学习）
```bash
# 主力
ZHIPU_API_KEY=xxx          # 国内用户
# 或
GEMINI_API_KEY=AIzaSy...   # 国外用户

# 备用
GROQ_API_KEY=gsk_xxx       # 免费，速度快
```
**成本**：$0/月

---

### 方案2：国内用户最佳
```bash
# 主力：智谱AI（免费）
ZHIPU_API_KEY=xxx
ZHIPU_MODEL=glm-4-flash

# 备用：通义千问（便宜）
QWEN_API_KEY=sk-xxx
QWEN_MODEL=qwen-turbo
```
**成本**：约1-5元/月

---

### 方案3：公司项目（质量优先）
```bash
# 主力：Claude（推理强）
CLAUDE_API_KEY=sk-ant-api03-xxx
CLAUDE_MODEL=claude-3-5-haiku-20241022

# 备用：DeepSeek（便宜）
DEEPSEEK_API_KEY=sk-xxx
DEEPSEEK_MODEL=deepseek-chat
```
**成本**：约20-50元/月

---

### 方案4：全能配置
```bash
# 免费模型
GEMINI_API_KEY=AIzaSy...
ZHIPU_API_KEY=xxx

# 付费模型（按需切换）
CLAUDE_API_KEY=sk-ant-api03-xxx
DEEPSEEK_API_KEY=sk-xxx
```
**成本**：灵活控制

---

## 📱 配置步骤（通用）

所有模型的配置步骤都类似：

### 1️⃣ 获取API密钥
访问对应平台 → 注册/登录 → 创建API Key → 复制密钥

### 2️⃣ 配置到项目
编辑.env文件或在Vercel添加环境变量

### 3️⃣ 重启应用
本地重启或Vercel重新部署

### 4️⃣ 验证配置
打开"AI设置"查看模型是否可用

---

## 🔍 功能对照表

| 功能 | 使用AI模型 | 推荐模型 |
|------|-----------|---------|
| 论文摘要 | ✓ | Gemini/智谱AI（免费） |
| 创新点提取 | ✓ | Gemini/智谱AI（免费） |
| 代码架构分析 | ✓ | Claude（质量）/DeepSeek（便宜） |
| PDF翻译 | ✓ | Gemini/智谱AI（免费） |
| AI对话 | ✓ | 任意模型 |

---

## 📊 模型对比速查表

| 特性 | Gemini | 智谱AI | Claude | DeepSeek | Qwen |
|------|--------|--------|--------|----------|------|
| **成本** | 免费 | 免费 | 付费 | 极低 | 低 |
| **性能** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **中文** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **代码** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **速度** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **国内** | ❌ | ✅ | ✅ | ✅ | ✅ |

---

## 🆘 需要帮助？

### 配置问题
1. 查看对应模型的详细配置文档
2. 查看 [API_KEYS_GUIDE.md](../API_KEYS_GUIDE.md) 常见问题章节
3. 检查.env文件格式
4. 查看应用错误日志

### 使用问题
1. 查看 [GLOBAL_AI_SETTINGS.md](../GLOBAL_AI_SETTINGS.md)
2. 测试API健康接口：`/api/ai/health`
3. 查看浏览器控制台错误

### 账单问题
- 免费模型：无需担心
- 付费模型：查看对应平台的计费页面

---

## 📞 联系支持

### 智谱AI
- 官网：https://open.bigmodel.cn/
- 工单系统：控制台 → 工单支持

### Google Gemini
- 文档：https://ai.google.dev/docs
- 社区：https://developers.googleblog.com/

### Anthropic Claude
- 支持：support@anthropic.com
- 文档：https://docs.anthropic.com/

---

## 🎉 开始配置

选择一个模型开始配置：

1. **国内用户** → [智谱AI配置](ZHIPU_CONFIG.md)（3分钟）
2. **国外用户** → [Gemini配置](GEMINI_CONFIG.md)（5分钟）
3. **公司项目** → [Claude配置](CLAUDE_CONFIG.md)（5分钟）
4. **阿里云用户** → [通义千问配置](QWEN_CONFIG.md)（5分钟）

配置任意一个模型，即可使用所有AI功能！

---

**祝你配置顺利！** 🚀
