# 🤖 AI模型配置完全指南

## 📋 快速开始

### 第1步：添加你的API密钥

编辑项目根目录的 `.env` 文件，添加你公司的API密钥：

```bash
# .env 文件

# Supabase配置（已有）
SUPABASE_URL=https://wlslekyepjebnzjmslld.supabase.co
SUPABASE_KEY=...

# 添加你公司的Claude API密钥
CLAUDE_API_KEY=sk-ant-api03-xxx...
CLAUDE_MODEL=claude-3-5-haiku-20241022

# 添加你公司的Gemini API密钥
GEMINI_API_KEY=AIzaSy...
GEMINI_MODEL=gemini-2.0-flash-exp
```

### 第2步：重启服务

如果是本地开发：
```bash
# 停止当前服务（Ctrl+C）
# 重新启动
python -m uvicorn backend.main:app --reload
```

如果是Vercel部署：
```bash
# 1. 在Vercel项目设置中添加环境变量
# 2. Settings → Environment Variables
# 3. 添加 CLAUDE_API_KEY 和 GEMINI_API_KEY
# 4. 触发重新部署
```

### 第3步：测试

系统启动时会自动显示使用的模型：
```
✓ 使用 Google Gemini gemini-2.0-flash-exp (完全免费)
```

---

## 🎯 推荐配置方案

### 方案A：完全免费（推荐个人使用）

```bash
# 1. Gemini 作为主力（免费，性能强）
GEMINI_API_KEY=你的密钥
GEMINI_MODEL=gemini-2.0-flash-exp

# 2. 智谱AI GLM-4 作为备用（免费，国内访问快）
ZHIPU_API_KEY=你的密钥
ZHIPU_MODEL=glm-4-flash
```

**优势**：
- ✅ 完全免费
- ✅ Gemini 性能接近GPT-4
- ✅ 智谱AI 中文理解优秀
- ✅ 每天150万tokens够用

---

### 方案B：公司商用（平衡性价比）

```bash
# 1. Claude 作为主力（质量最高）
CLAUDE_API_KEY=你的密钥
CLAUDE_MODEL=claude-3-5-haiku-20241022

# 2. DeepSeek 作为备用（极低成本）
DEEPSEEK_API_KEY=你的密钥
DEEPSEEK_MODEL=deepseek-chat

# 3. Gemini 作为免费补充
GEMINI_API_KEY=你的密钥
```

**优势**：
- ✅ Claude Haiku 输出质量最稳定
- ✅ 成本控制：$0.8/M input
- ✅ DeepSeek 作为廉价备用
- ✅ Gemini 免费额度作为补充

**月成本估算**：
- 轻度使用（<100万tokens）：<$5
- 中度使用（100-500万tokens）：$10-30
- 重度使用（>500万tokens）：$50+

---

### 方案C：追求极致质量

```bash
# 1. Claude Sonnet 作为主力
CLAUDE_API_KEY=你的密钥
CLAUDE_MODEL=claude-3-5-sonnet-20241022

# 2. GPT-4o 作为对比
OPENAI_API_KEY=你的密钥
OPENAI_MODEL=gpt-4o

# 3. Gemini Pro 作为第三选择
GEMINI_API_KEY=你的密钥
GEMINI_MODEL=gemini-1.5-pro
```

**适用场景**：
- 代码架构深度分析
- 复杂推理任务
- 学术论文精读
- 需要最高准确度的场景

---

## 📚 详细配置说明

### 🏆 Google Gemini 配置

**获取API密钥：**
1. 访问：https://ai.google.dev/
2. 点击 "Get API Key"
3. 创建或选择Google Cloud项目
4. 复制API密钥

**配置：**
```bash
GEMINI_API_KEY=AIzaSyC...
GEMINI_MODEL=gemini-2.0-flash-exp
```

**可用模型：**
| 模型 | 价格 | 上下文 | 适用场景 |
|------|------|--------|----------|
| gemini-2.0-flash-exp | 免费 | 1M tokens | 日常使用（推荐） |
| gemini-1.5-flash | $0.075/M | 1M tokens | 快速响应 |
| gemini-1.5-pro | $1.25/M | 2M tokens | 长文本分析 |

**免费额度：**
- 15次/分钟
- 150万tokens/天
- 完全够个人使用

---

### 💎 Anthropic Claude 配置

**获取API密钥：**
1. 访问：https://console.anthropic.com/
2. 注册账号（需要国外手机号）
3. Settings → API Keys
4. Create Key

**配置：**
```bash
CLAUDE_API_KEY=sk-ant-api03-...
CLAUDE_MODEL=claude-3-5-haiku-20241022
```

**可用模型：**
| 模型 | 输入价格 | 输出价格 | 特点 |
|------|---------|---------|------|
| claude-3-5-haiku | $0.8/M | $4/M | 快速，性价比高 |
| claude-3-5-sonnet | $3/M | $15/M | 推理能力最强 |
| claude-3-opus | $15/M | $75/M | 极致质量 |

**适用场景：**
- ✅ 代码架构分析（最准确）
- ✅ 结构化输出（最稳定）
- ✅ 复杂推理任务
- ✅ 论文速读生成

**注意事项：**
- 需要绑定信用卡
- 新账号有$5免费额度
- 建议设置消费上限

---

### 🌟 DeepSeek 配置

**获取API密钥：**
1. 访问：https://platform.deepseek.com/
2. 注册账号（支持国内手机号）
3. API Keys → Create API Key

**配置：**
```bash
DEEPSEEK_API_KEY=sk-...
DEEPSEEK_MODEL=deepseek-chat
```

**优势：**
- 💰 极低成本：$0.27/M input（GPT-4的1/20）
- 🇨🇳 中文理解优秀
- 🚀 性能接近GPT-4水平
- 💳 支持支付宝充值

**适用场景：**
- 中文论文分析
- 大量文本处理
- 成本敏感项目

---

### 🔷 OpenAI GPT 配置

**获取API密钥：**
1. 访问：https://platform.openai.com/
2. 注册账号
3. API keys → Create new secret key

**配置：**
```bash
OPENAI_API_KEY=sk-proj-...
OPENAI_MODEL=gpt-4o-mini
```

**可用模型：**
| 模型 | 输入价格 | 输出价格 | 适用场景 |
|------|---------|---------|----------|
| gpt-4o-mini | $0.15/M | $0.6/M | 日常使用 |
| gpt-4o | $2.5/M | $10/M | 旗舰质量 |
| gpt-4-turbo | $10/M | $30/M | 旧版旗舰 |

---

## 🔧 Vercel环境变量配置

如果你的项目部署在Vercel上：

### 第1步：添加环境变量

1. 打开Vercel项目
2. Settings → Environment Variables
3. 添加以下变量：

```
Name: CLAUDE_API_KEY
Value: sk-ant-api03-xxx...
```

```
Name: GEMINI_API_KEY
Value: AIzaSy...
```

### 第2步：触发重新部署

1. Deployments → 最新部署 → ⋯ → Redeploy
2. 或者推送代码到GitHub触发自动部署

### 第3步：验证

访问：`https://your-app.vercel.app/api/health`

查看响应中的AI配置信息。

---

## 🎯 模型选择优先级

系统会自动按以下顺序选择可用模型：

```
1. Gemini (完全免费，性能强) ⭐⭐⭐⭐⭐
2. 智谱AI GLM-4-Flash (完全免费) ⭐⭐⭐⭐
3. DeepSeek (极低成本) ⭐⭐⭐⭐
4. 通义千问 (廉价) ⭐⭐⭐
5. Claude (高质量) ⭐⭐⭐⭐⭐
6. OpenAI (标杆) ⭐⭐⭐⭐
7. Groq (免费备选) ⭐⭐⭐
```

**你只需要配置你拥有的API KEY，系统会自动选择最优的！**

---

## 📊 成本对比表

| 模型 | 输入价格 | 输出价格 | 100万tokens成本 | 推荐度 |
|------|---------|---------|----------------|--------|
| Gemini 2.0 Flash | 免费 | 免费 | $0 | ⭐⭐⭐⭐⭐ |
| 智谱GLM-4-Flash | 免费 | 免费 | $0 | ⭐⭐⭐⭐ |
| DeepSeek | $0.27 | $1.1 | $1.37 | ⭐⭐⭐⭐ |
| Claude Haiku | $0.8 | $4 | $4.8 | ⭐⭐⭐⭐⭐ |
| GPT-4o mini | $0.15 | $0.6 | $0.75 | ⭐⭐⭐⭐ |
| GPT-4o | $2.5 | $10 | $12.5 | ⭐⭐⭐⭐ |
| Claude Sonnet | $3 | $15 | $18 | ⭐⭐⭐⭐⭐ |

---

## 🚨 常见问题

### Q: 配置了多个API KEY，会使用哪个？

系统会按优先级自动选择第一个可用的模型。查看日志可以看到：
```
✓ 使用 Google Gemini gemini-2.0-flash-exp (完全免费)
```

### Q: 如何强制使用特定模型？

只配置该模型的API KEY，删除或注释掉其他模型的配置。

### Q: 成本如何控制？

1. 优先使用免费模型（Gemini、智谱AI）
2. 设置API消费上限（在服务商后台）
3. 监控token使用量
4. 选择便宜的模型（DeepSeek、GPT-4o mini）

### Q: Gemini API在国内能用吗？

需要科学上网。如果无法访问，使用智谱AI GLM-4-Flash（完全免费，国内可用）。

### Q: 如何获取免费的API密钥？

| 服务 | 免费额度 | 获取地址 |
|------|---------|---------|
| Gemini | 150万tokens/天 | https://ai.google.dev/ |
| 智谱AI | 无限制 | https://open.bigmodel.cn/ |
| Groq | 30次/分钟 | https://console.groq.com/ |

---

## 🔍 测试你的配置

在浏览器控制台（F12）运行：

```javascript
// 测试AI对话
const response = await fetch('/api/conversations/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        paper_id: 1,
        user_message: '测试AI配置'
    })
});
const data = await response.json();
console.log(data);
```

或访问健康检查端点：
```
https://your-app.vercel.app/api/health
```

---

## 📞 需要帮助？

如有问题，请检查：
1. API密钥格式是否正确
2. 环境变量是否生效（重启服务）
3. 服务商账户是否有余额
4. 网络是否可以访问API

推荐配置：**Gemini (主力) + DeepSeek (备用)**，成本极低且性能强大！
