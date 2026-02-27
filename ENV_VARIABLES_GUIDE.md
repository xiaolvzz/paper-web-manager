# 环境变量配置完整指南

## 🎯 快速开始

**是的！只需要添加API Key就可以了！**

系统会自动按优先级选择第一个配置了的AI服务，无需修改代码。

---

## 📋 所有支持的环境变量

### AI服务配置（按优先级排序）

#### 1. Google Gemini（最优先）
```env
GEMINI_API_KEY=你的Gemini_API密钥
GEMINI_MODEL=gemini-2.0-flash-exp  # 可选，默认为2.0-flash-exp
```

**可选模型：**
- `gemini-2.0-flash-exp` - 最新实验版，完全免费（推荐）
- `gemini-1.5-flash` - 快速版，$0.075/M
- `gemini-1.5-pro` - 旗舰版，$1.25/M

**优先级：第1位**

---

#### 2. 智谱AI（第二优先）
```env
ZHIPU_API_KEY=你的智谱AI_API密钥
ZHIPU_MODEL=glm-4-flash  # 可选，默认为glm-4-flash
```

**可选模型：**
- `glm-4-flash` - 完全免费（推荐）
- `glm-4-air` - 均衡版，1元/M
- `glm-4-plus` - 旗舰版，50元/M

**优先级：第2位**

---

#### 3. DeepSeek（第三优先）
```env
DEEPSEEK_API_KEY=你的DeepSeek_API密钥
```

**模型：** `deepseek-chat`（DeepSeek-V3）
**优先级：第3位**

---

#### 4. 通义千问（第四优先）
```env
QWEN_API_KEY=你的通义千问_API密钥
QWEN_MODEL=qwen-turbo  # 可选，默认为qwen-turbo
```

**可选模型：**
- `qwen-turbo` - 快速廉价，0.3元/M（推荐）
- `qwen-plus` - 增强版，4元/M
- `qwen-max` - 最强版，20元/M
- `qwen-long` - 长文本，0.5元/M（支持1M tokens上下文）

**优先级：第4位**

---

#### 5. Anthropic Claude（第五优先）
```env
CLAUDE_API_KEY=你的Claude_API密钥
CLAUDE_MODEL=claude-3-5-haiku-20241022  # 可选
```

**可选模型：**
- `claude-3-5-haiku-20241022` - 快速版，$0.8/M（推荐）
- `claude-3-5-sonnet-20241022` - 旗舰版，$3/M
- `claude-3-opus-20240229` - 最强版，$15/M

**优先级：第5位**

---

#### 6. OpenAI GPT（第六优先）
```env
OPENAI_API_KEY=你的OpenAI_API密钥
OPENAI_MODEL=gpt-4o-mini  # 可选，默认为gpt-4o-mini
```

**可选模型：**
- `gpt-4o-mini` - 快速廉价，$0.15/M（推荐）
- `gpt-4o` - 旗舰版，$2.5/M
- `gpt-4-turbo` - 旧版旗舰，$10/M

**优先级：第6位**

---

#### 7. Groq（备选）
```env
GROQ_API_KEY=你的Groq_API密钥
```

**模型：** `llama-3.2-90b-text-preview`
**优先级：第7位（最后备选）**

---

## 🔄 系统自动选择逻辑

系统会按以下顺序检查环境变量，使用**第一个配置了的**服务：

```
Gemini → 智谱AI → DeepSeek → 通义千问 → Claude → OpenAI → Groq
```

**示例1：只配置了智谱AI**
```env
ZHIPU_API_KEY=sk-xxxxx
```
→ 系统使用智谱AI GLM-4-Flash

**示例2：配置了多个**
```env
GEMINI_API_KEY=AIza-xxxxx
ZHIPU_API_KEY=sk-xxxxx
DEEPSEEK_API_KEY=sk-xxxxx
```
→ 系统使用Gemini（优先级最高）

**示例3：Gemini未配置，但配置了智谱和DeepSeek**
```env
ZHIPU_API_KEY=sk-xxxxx
DEEPSEEK_API_KEY=sk-xxxxx
```
→ 系统使用智谱AI（优先级第二）

---

## 🎯 推荐配置方案

### 方案A：完全免费（国内用户）⭐⭐⭐⭐⭐
```env
ZHIPU_API_KEY=你的智谱AI密钥
DEEPSEEK_API_KEY=你的DeepSeek密钥
```
**说明：** 智谱主力（免费），DeepSeek备用（新用户500万tokens免费）
**成本：** 0元/月

---

### 方案B：完全免费（有梯子）⭐⭐⭐⭐⭐
```env
GEMINI_API_KEY=你的Gemini密钥
ZHIPU_API_KEY=你的智谱AI密钥
```
**说明：** Gemini主力（免费+性能强），智谱备用（国内访问）
**成本：** 0元/月

---

### 方案C：极致性价比（国内）⭐⭐⭐⭐⭐
```env
ZHIPU_API_KEY=你的智谱AI密钥
DEEPSEEK_API_KEY=你的DeepSeek密钥
QWEN_API_KEY=你的通义千问密钥
```
**说明：** 三重备份，智谱免费主力
**成本：** 0元/月（DeepSeek 0.44元/月，通义0.36元/月）

---

### 方案D：顶级性能（需梯子）⭐⭐⭐⭐
```env
GEMINI_API_KEY=你的Gemini密钥
GEMINI_MODEL=gemini-1.5-pro
CLAUDE_API_KEY=你的Claude密钥
CLAUDE_MODEL=claude-3-5-sonnet-20241022
```
**说明：** 顶级模型配置
**成本：** 约18-22元/月

---

## 🚀 如何配置到Vercel

### 步骤1：获取API密钥
根据你选择的服务，去对应网站注册并获取API Key：
- Gemini: https://aistudio.google.com/
- 智谱AI: https://open.bigmodel.cn/
- DeepSeek: https://platform.deepseek.com/
- 通义千问: https://dashscope.aliyun.com/
- Claude: https://console.anthropic.com/
- OpenAI: https://platform.openai.com/

### 步骤2：添加到Vercel
1. 打开 https://vercel.com/dashboard
2. 选择 `paper-web-manager` 项目
3. 点击 **Settings** → **Environment Variables**
4. 点击 **Add New**
5. 填写：
   - **Name**: 环境变量名（如 `ZHIPU_API_KEY`）
   - **Value**: 你的API密钥
   - **Environments**: 全选 ✅
6. 点击 **Save**

### 步骤3：重新部署
1. 返回 **Deployments**
2. 点击最新部署的 **⋯**
3. 选择 **Redeploy**
4. 等待2-3分钟

### 步骤4：验证配置
访问：https://paper-web-manager.vercel.app/api/ai/health

应该看到：
```json
{
  "status": "healthy",
  "provider": "Google Gemini",  // 或其他你配置的服务
  "model": "gemini-2.0-flash-exp",
  "configured": true
}
```

---

## 🔍 如何检查当前使用哪个服务？

### 方法1：访问健康检查API
```
https://paper-web-manager.vercel.app/api/ai/health
```

返回示例：
```json
{
  "status": "healthy",
  "provider": "智谱AI (GLM-4)",
  "model": "glm-4-flash",
  "configured": true
}
```

### 方法2：查看Vercel部署日志
1. Vercel Dashboard → Deployments
2. 点击最新部署
3. 查看 **Function Logs**
4. 应该能看到类似：
```
✓ 使用 智谱AI glm-4-flash (完全免费)
```

---

## 🎛️ 高级配置

### 自定义模型选择

**智谱AI切换到Plus版本：**
```env
ZHIPU_API_KEY=你的密钥
ZHIPU_MODEL=glm-4-plus
```

**通义千问切换到Long版本（超长文本）：**
```env
QWEN_API_KEY=你的密钥
QWEN_MODEL=qwen-long
```

**Gemini切换到Pro版本：**
```env
GEMINI_API_KEY=你的密钥
GEMINI_MODEL=gemini-1.5-pro
```

**OpenAI切换到GPT-4o：**
```env
OPENAI_API_KEY=你的密钥
OPENAI_MODEL=gpt-4o
```

---

## ❓ 常见问题

### Q1: 我配置了API Key，但还是显示"未配置"？
**A:** 检查：
1. 环境变量名是否正确（区分大小写）
2. API Key是否复制完整（没有多余空格）
3. 是否重新部署了Vercel项目
4. 等待2-3分钟让部署完成

### Q2: 可以同时配置多个API Key吗？
**A:** 可以！推荐配置2-3个作为备份。系统会自动选择优先级最高的可用服务。

### Q3: 如何强制使用某个特定的服务？
**A:** 方法1：只配置那一个API Key
方法2：删除其他优先级更高的API Key

### Q4: 配置后如何验证是否生效？
**A:** 访问 `/api/ai/health` 查看 `provider` 字段，确认当前使用的服务。

### Q5: API Key会过期吗？
**A:**
- 大部分服务的API Key不会过期
- 免费额度可能有时间限制（如每月重置）
- 如果失效，系统会自动切换到下一个可用服务

### Q6: 能不能调整优先级顺序？
**A:** 目前优先级是硬编码的（免费 > 廉价 > 昂贵）。如果你想自定义，我可以帮你修改代码。

---

## 💡 配置建议

### 对于个人用户（每天1-2篇论文）
**推荐：**
```env
ZHIPU_API_KEY=xxx  # 完全免费，够用
```

### 对于重度用户（每天3-5篇论文）
**推荐：**
```env
GEMINI_API_KEY=xxx     # 主力，免费
ZHIPU_API_KEY=xxx      # 备用，国内访问
DEEPSEEK_API_KEY=xxx   # 备用，廉价
```

### 对于追求极致性能
**推荐：**
```env
GEMINI_API_KEY=xxx
GEMINI_MODEL=gemini-1.5-pro
CLAUDE_API_KEY=xxx
CLAUDE_MODEL=claude-3-5-sonnet-20241022
```

---

## 📊 配置对比表

| 配置方案 | 环境变量 | 月成本 | 国内访问 | 性能 |
|---------|---------|--------|---------|------|
| **纯免费** | ZHIPU_API_KEY | 0元 | ✅ | ⭐⭐⭐ |
| **免费最佳** | GEMINI_API_KEY | 0元 | ❌需梯子 | ⭐⭐⭐⭐⭐ |
| **极致廉价** | DEEPSEEK_API_KEY | 0.44元 | ✅ | ⭐⭐⭐⭐ |
| **多重备份** | 智谱+DeepSeek+千问 | 0-1元 | ✅ | ⭐⭐⭐⭐ |
| **顶级性能** | Gemini Pro+Claude | 18-22元 | ❌需梯子 | ⭐⭐⭐⭐⭐ |

---

**更新日期：2026年2月27日**
**版本：v2.0 - 支持7个AI提供商**
