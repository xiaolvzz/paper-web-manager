# 🔑 所有AI模型API密钥配置完整指南

本文档包含系统支持的所有7个AI模型的API密钥获取和配置方法。

---

## 📋 目录

1. [Google Gemini](#1-google-gemini)（完全免费，推荐）
2. [智谱AI GLM-4](#2-智谱ai-glm-4)（免费，国内推荐）
3. [DeepSeek](#3-deepseek)（极低成本）
4. [通义千问 Qwen](#4-通义千问-qwen)（便宜，阿里云）
5. [Anthropic Claude](#5-anthropic-claude)（推理最强）
6. [OpenAI GPT](#6-openai-gpt)（业界标杆）
7. [Groq](#7-groq)（免费，超快）

---

## 1. Google Gemini

### 🌟 特点
- **完全免费**（无需信用卡）
- 性能接近GPT-4
- 适合所有场景

### 📝 获取API密钥

#### 步骤：
1. **访问 Google AI Studio**
   https://aistudio.google.com/apikey

2. **登录Google账号**
   使用你的Gmail账号登录

3. **创建API密钥**
   - 点击 "Get API key" 或 "创建API密钥"
   - 选择或创建一个Google Cloud项目
   - 点击 "Create API key in new project"
   - 复制生成的密钥（格式：`AIzaSy...`）

4. **注意事项**
   - ⚠️ Gemini在中国大陆部分地区不可用
   - 如果显示"region not available"，使用智谱AI替代

### ⚙️ 配置方法

**本地开发（.env文件）**：
```bash
GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXX
GEMINI_MODEL=gemini-2.0-flash-exp
```

**Vercel部署**：
- Name: `GEMINI_API_KEY`
- Value: `AIzaSy...`

**推荐模型**：
- `gemini-2.0-flash-exp` - 最新实验版，完全免费（推荐）
- `gemini-1.5-flash` - 稳定版，$0.075/M tokens
- `gemini-1.5-pro` - 旗舰版，$1.25/M tokens

### 💰 价格
- **2.0-flash-exp**: 完全免费（有限流）
- **1.5-flash**: $0.075/M input, $0.3/M output
- **1.5-pro**: $1.25/M input, $5/M output

---

## 2. 智谱AI GLM-4

### 🌟 特点
- **完全免费**（GLM-4-Flash）
- 中文理解优秀
- 国内访问稳定
- **推荐中国用户使用**

### 📝 获取API密钥

#### 步骤：
1. **访问智谱AI开放平台**
   https://open.bigmodel.cn/

2. **注册/登录**
   - 点击右上角"注册"
   - 支持手机号注册
   - 需要实名认证

3. **进入控制台**
   - 登录后，点击"控制台"
   - 或访问：https://open.bigmodel.cn/usercenter/apikeys

4. **创建API密钥**
   - 点击"创建API Key"
   - 输入密钥名称（如：论文管理系统）
   - 复制生成的密钥（格式：长字符串）

5. **查看额度**
   - 新用户赠送免费额度
   - 控制台可查看剩余额度

### ⚙️ 配置方法

**本地开发（.env文件）**：
```bash
ZHIPU_API_KEY=your_long_api_key_string_here
ZHIPU_MODEL=glm-4-flash
```

**Vercel部署**：
- Name: `ZHIPU_API_KEY`
- Value: `your_api_key`

**推荐模型**：
- `glm-4-flash` - 完全免费，无限制使用（推荐）
- `glm-4-air` - 均衡版，1元/M tokens
- `glm-4-plus` - 旗舰版，50元/M tokens

### 💰 价格
- **glm-4-flash**: 完全免费！无限制
- **glm-4-air**: 1元/M tokens
- **glm-4-plus**: 50元/M tokens

---

## 3. DeepSeek

### 🌟 特点
- **极低成本**（业界最便宜）
- 性能接近GPT-4
- 开源友好

### 📝 获取API密钥

#### 步骤：
1. **访问DeepSeek平台**
   https://platform.deepseek.com/

2. **注册账号**
   - 点击右上角"Sign Up"
   - 支持邮箱注册或GitHub登录
   - 需要邮箱验证

3. **进入API Keys页面**
   - 登录后，点击左侧菜单"API Keys"
   - 或访问：https://platform.deepseek.com/api_keys

4. **创建API密钥**
   - 点击"Create API Key"
   - 输入名称（如：paper-manager）
   - 复制生成的密钥（格式：`sk-...`）
   - ⚠️ 密钥只显示一次，请妥善保存

5. **充值**
   - 新用户可能有免费额度
   - 支持支付宝充值（最低10元）

### ⚙️ 配置方法

**本地开发（.env文件）**：
```bash
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
DEEPSEEK_MODEL=deepseek-chat
```

**Vercel部署**：
- Name: `DEEPSEEK_API_KEY`
- Value: `sk-...`

**推荐模型**：
- `deepseek-chat` - 主力模型（推荐）
- `deepseek-coder` - 代码专用（更适合代码分析）

### 💰 价格
- **极低成本**: 0.14元/M input, 0.28元/M output
- **对比GPT-4**: 便宜100倍以上
- **充值门槛**: 最低10元，可用很久

---

## 4. 通义千问 (Qwen)

### 🌟 特点
- 阿里云出品
- 国内访问稳定
- 价格适中
- 中文理解好

### 📝 获取API密钥

#### 步骤：
1. **访问DashScope控制台**
   https://dashscope.console.aliyun.com/

2. **登录阿里云**
   - 使用阿里云账号登录
   - 没有账号则注册（需要实名）

3. **开通服务**
   - 点击"免费开通"开通DashScope服务
   - 实名认证

4. **创建API密钥**
   - 进入 API-KEY管理：https://dashscope.console.aliyun.com/apiKey
   - 点击"创建新的API-KEY"
   - 复制生成的密钥（格式：`sk-...`）

5. **查看额度**
   - 新用户赠送免费tokens
   - 资源包管理页面查看余额

### ⚙️ 配置方法

**本地开发（.env文件）**：
```bash
QWEN_API_KEY=sk-xxxxxxxxxxxxxxxx
QWEN_MODEL=qwen-turbo
```

**Vercel部署**：
- Name: `QWEN_API_KEY`
- Value: `sk-...`

**推荐模型**：
- `qwen-turbo` - 快速廉价（推荐日常）
- `qwen-plus` - 增强版（质量更高）
- `qwen-max` - 最强版（最高质量）
- `qwen-long` - 长文本（100万tokens上下文）

### 💰 价格
- **qwen-turbo**: 0.3元/M input, 0.6元/M output
- **qwen-plus**: 4元/M input, 8元/M output
- **qwen-max**: 20元/M input, 60元/M output
- **qwen-long**: 0.5元/M input, 2元/M output

---

## 5. Anthropic Claude

### 🌟 特点
- **推理能力最强**
- 代码理解优秀
- 适合复杂分析任务
- 公司常用

### 📝 获取API密钥

#### 步骤：
1. **访问Anthropic Console**
   https://console.anthropic.com/

2. **注册账号**
   - 点击"Sign Up"
   - 使用邮箱注册
   - 邮箱验证

3. **进入API Keys页面**
   - 登录后，左侧菜单 → "API Keys"
   - 或访问：https://console.anthropic.com/settings/keys

4. **创建API密钥**
   - 点击"Create Key"
   - 输入名称（如：paper-manager）
   - 复制生成的密钥（格式：`sk-ant-api03-...`）
   - ⚠️ 密钥只显示一次

5. **设置预算**（可选）
   - Settings → Billing
   - 添加信用卡
   - 设置每月消费上限

### ⚙️ 配置方法

**本地开发（.env文件）**：
```bash
CLAUDE_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxx
CLAUDE_MODEL=claude-3-5-haiku-20241022
```

**Vercel部署**：
- Name: `CLAUDE_API_KEY`
- Value: `sk-ant-api03-...`

**推荐模型**：
- `claude-3-5-haiku-20241022` - 快速版（推荐，性价比高）
- `claude-3-5-sonnet-20241022` - 平衡版（质量更好）
- `claude-3-opus-20240229` - 旗舰版（最强，但很贵）

### 💰 价格
- **Haiku**: $0.8/M input, $4/M output（推荐）
- **Sonnet**: $3/M input, $15/M output
- **Opus**: $15/M input, $75/M output

### 🏢 公司使用
如果你有公司的Claude API密钥，推荐使用Haiku模型：
```bash
CLAUDE_API_KEY=sk-ant-api03-xxx  # 公司提供的密钥
CLAUDE_MODEL=claude-3-5-haiku-20241022
```

---

## 6. OpenAI GPT

### 🌟 特点
- 业界标杆
- 生态完善
- 稳定可靠
- 价格较高

### 📝 获取API密钥

#### 步骤：
1. **访问OpenAI平台**
   https://platform.openai.com/

2. **注册账号**
   - 点击"Sign Up"
   - 使用邮箱或Google账号注册
   - 需要手机号验证（可能需要国外手机号）

3. **进入API Keys页面**
   - 登录后，点击右上角头像
   - 选择"View API keys"
   - 或访问：https://platform.openai.com/api-keys

4. **创建API密钥**
   - 点击"Create new secret key"
   - 输入名称（如：paper-manager）
   - 复制生成的密钥（格式：`sk-proj-...` 或 `sk-...`）
   - ⚠️ 密钥只显示一次

5. **充值**
   - Settings → Billing
   - 添加信用卡
   - 新用户可能有$5免费额度（有时间限制）

### ⚙️ 配置方法

**本地开发（.env文件）**：
```bash
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_MODEL=gpt-4o-mini
```

**Vercel部署**：
- Name: `OPENAI_API_KEY`
- Value: `sk-proj-...` 或 `sk-...`

**推荐模型**：
- `gpt-4o-mini` - 快速廉价（推荐，性价比最高）
- `gpt-4o` - 旗舰版（质量最好）
- `gpt-4-turbo` - 旧版旗舰（已被4o取代）

### 💰 价格
- **gpt-4o-mini**: $0.15/M input, $0.6/M output（推荐）
- **gpt-4o**: $2.5/M input, $10/M output
- **gpt-4-turbo**: $10/M input, $30/M output

---

## 7. Groq

### 🌟 特点
- **完全免费**
- 速度极快（最快的推理速度）
- 有每日限额

### 📝 获取API密钥

#### 步骤：
1. **访问Groq Console**
   https://console.groq.com/

2. **注册账号**
   - 点击"Sign Up"
   - 使用邮箱或Google账号注册
   - 邮箱验证

3. **进入API Keys页面**
   - 登录后，左侧菜单 → "API Keys"
   - 或访问：https://console.groq.com/keys

4. **创建API密钥**
   - 点击"Create API Key"
   - 输入名称（如：paper-manager）
   - 复制生成的密钥（格式：`gsk_...`）
   - ⚠️ 密钥只显示一次

### ⚙️ 配置方法

**本地开发（.env文件）**：
```bash
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxx
GROQ_MODEL=llama-3.2-90b-text-preview
```

**Vercel部署**：
- Name: `GROQ_API_KEY`
- Value: `gsk_...`

**推荐模型**：
- `llama-3.2-90b-text-preview` - 90B参数，性能强（推荐）
- `llama-3.1-70b-versatile` - 70B参数，速度更快
- `mixtral-8x7b-32768` - Mixtral模型

### 💰 价格
- **完全免费**
- 有每日请求限额（通常够用）
- 超限后需要等待重置

---

## 📊 所有模型对比表

| 模型 | 成本 | 性能 | 速度 | 中文 | 国内访问 | 推荐指数 |
|------|------|------|------|------|----------|----------|
| **Gemini 2.0 Flash** | 免费 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ❌ | ⭐⭐⭐⭐⭐ |
| **智谱AI GLM-4** | 免费 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ | ⭐⭐⭐⭐⭐ |
| **DeepSeek** | 极低 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ | ⭐⭐⭐⭐ |
| **通义千问** | 低 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ | ⭐⭐⭐⭐ |
| **Claude Haiku** | 中 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ | ⭐⭐⭐⭐ |
| **GPT-4o-mini** | 中 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ | ⭐⭐⭐ |
| **Groq (Llama)** | 免费 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ✅ | ⭐⭐⭐ |

---

## 🎯 推荐配置方案

### 方案1：完全免费（个人学习）
```bash
# 主力：Gemini 2.0（国外）
GEMINI_API_KEY=AIzaSy...
GEMINI_MODEL=gemini-2.0-flash-exp

# 备用：智谱AI（国内）
ZHIPU_API_KEY=xxx
ZHIPU_MODEL=glm-4-flash
```
**优势**：零成本，性能优秀
**适用**：个人学习、日常使用

---

### 方案2：国内用户（稳定访问）
```bash
# 主力：智谱AI（完全免费）
ZHIPU_API_KEY=xxx
ZHIPU_MODEL=glm-4-flash

# 备用：通义千问（便宜）
QWEN_API_KEY=sk-...
QWEN_MODEL=qwen-turbo
```
**优势**：国内访问稳定，无需VPN
**适用**：中国大陆用户

---

### 方案3：公司项目（质量优先）
```bash
# 主力：Claude（推理最强）
CLAUDE_API_KEY=sk-ant-api03-...
CLAUDE_MODEL=claude-3-5-haiku-20241022

# 备用：DeepSeek（性价比高）
DEEPSEEK_API_KEY=sk-...
DEEPSEEK_MODEL=deepseek-chat
```
**优势**：推理能力强，适合复杂任务
**适用**：企业应用、科研项目

---

### 方案4：成本优化（极致省钱）
```bash
# 主力：智谱AI或Gemini（免费）
ZHIPU_API_KEY=xxx
ZHIPU_MODEL=glm-4-flash

# 复杂任务：DeepSeek（便宜）
DEEPSEEK_API_KEY=sk-...
DEEPSEEK_MODEL=deepseek-chat
```
**优势**：日常免费，复杂任务成本极低
**适用**：预算有限的个人或团队

---

### 方案5：全能配置（推荐）
```bash
# 免费模型：日常使用
GEMINI_API_KEY=AIzaSy...
GEMINI_MODEL=gemini-2.0-flash-exp

ZHIPU_API_KEY=xxx
ZHIPU_MODEL=glm-4-flash

# 付费模型：复杂任务
CLAUDE_API_KEY=sk-ant-api03-...
CLAUDE_MODEL=claude-3-5-haiku-20241022

DEEPSEEK_API_KEY=sk-...
DEEPSEEK_MODEL=deepseek-chat
```
**优势**：灵活切换，各取所长
**适用**：专业用户、重度使用

---

## 📦 配置示例（完整.env文件）

```bash
# ============================================
# 数据库配置（必须）
# ============================================
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJhbGci...

# ============================================
# AI模型配置（至少配置一个）
# ============================================

# --- 免费模型（推荐配置） ---

# Gemini 2.0 Flash（完全免费，性能强）
GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXX
GEMINI_MODEL=gemini-2.0-flash-exp

# 智谱AI GLM-4-Flash（完全免费，国内稳定）
ZHIPU_API_KEY=your_zhipu_key_here
ZHIPU_MODEL=glm-4-flash

# Groq（免费，速度快）
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxx
GROQ_MODEL=llama-3.2-90b-text-preview

# --- 付费模型（按需配置） ---

# Claude（推理强，适合代码分析）
CLAUDE_API_KEY=sk-ant-api03-xxxxxxxxxxx
CLAUDE_MODEL=claude-3-5-haiku-20241022

# DeepSeek（极低成本）
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxx
DEEPSEEK_MODEL=deepseek-chat

# 通义千问（阿里云）
QWEN_API_KEY=sk-xxxxxxxxxxxxxxxxx
QWEN_MODEL=qwen-turbo

# OpenAI（业界标杆）
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxx
OPENAI_MODEL=gpt-4o-mini
```

---

## 🔧 配置后的验证

### 1. 本地开发验证

启动应用：
```bash
python -m uvicorn backend.main:app --reload
```

查看终端输出，应该看到：
```
✓ 使用 Google Gemini gemini-2.0-flash-exp (完全免费)
或
✓ 使用 智谱AI glm-4-flash (完全免费)
```

### 2. 浏览器验证

打开应用后：
1. 查看导航栏"AI设置"按钮的badge
   - 🟢 显示模型名称：配置成功
   - 🟡 显示"未配置"：需要配置

2. 点击"AI设置"打开面板
   - 查看哪些模型显示为"可选择"状态
   - 尝试切换不同模型

3. 测试AI功能
   - 打开任意论文详情页
   - 点击"生成摘要"或"提取创新点"
   - 查看是否正常返回结果

### 3. API接口验证

```bash
# 检查AI服务状态
curl https://your-app.vercel.app/api/ai/health

# 获取模型列表
curl https://your-app.vercel.app/api/ai/models
```

---

## 🌐 API密钥申请链接速查

| 模型 | 申请地址 | 难度 | 需要外网 |
|------|----------|------|----------|
| Gemini | https://aistudio.google.com/apikey | 简单 | 是 |
| 智谱AI | https://open.bigmodel.cn/ | 简单 | 否 |
| DeepSeek | https://platform.deepseek.com/ | 简单 | 否 |
| 通义千问 | https://dashscope.console.aliyun.com/ | 中等 | 否 |
| Claude | https://console.anthropic.com/ | 简单 | 是 |
| OpenAI | https://platform.openai.com/ | 中等 | 是 |
| Groq | https://console.groq.com/ | 简单 | 是 |

---

## 💡 使用技巧

### 1. 优先级设置

系统默认按优先级选择：
```
Gemini → 智谱AI → DeepSeek → 通义千问 → Claude → OpenAI → Groq
```

**如何调整**：
- 只配置你想用的模型，删除其他配置
- 或通过"AI设置"面板手动选择

### 2. 成本控制

**日常任务用免费模型**：
- 论文摘要 → Gemini/智谱AI
- 简单问答 → Groq

**复杂任务用付费模型**：
- 代码架构分析 → Claude
- 深度论文分析 → Claude/GPT-4o

### 3. 网络问题

**如果Gemini无法访问**：
- 使用智谱AI（国内完全免费）
- 或使用DeepSeek（极低成本）

**如果都无法访问**：
- 检查网络连接
- 尝试使用代理
- 使用国内模型（智谱AI、通义千问、DeepSeek）

### 4. 多账号管理

可以为不同用途创建多个API密钥：
```bash
# 开发环境
CLAUDE_API_KEY=sk-ant-api03-dev-xxx

# 生产环境
CLAUDE_API_KEY=sk-ant-api03-prod-xxx
```

---

## 🔒 安全建议

1. **不要提交.env文件到Git**
   - 已添加到.gitignore
   - 检查：`git status` 不应显示.env

2. **定期轮换密钥**
   - 每3-6个月更换一次
   - 删除不用的旧密钥

3. **设置消费限额**
   - Claude: Settings → Billing → Usage limits
   - OpenAI: Settings → Billing → Usage limits
   - 防止意外超支

4. **不要分享密钥**
   - 密钥等同于账号密码
   - 泄露后立即删除并重新创建

---

## ❓ 常见问题汇总

### Q1：我应该配置哪个模型？
**推荐顺序**：
1. 🥇 **智谱AI**（国内用户首选，免费）
2. 🥈 **Gemini**（国外用户首选，免费）
3. 🥉 **DeepSeek**（需要一点成本，但极便宜）

### Q2：可以同时配置多个吗？
**可以！** 配置多个模型的好处：
- 互为备用（一个挂了用另一个）
- 灵活切换（简单任务用免费的，复杂任务用付费的）
- 对比效果（不同模型结果对比）

### Q3：哪些模型需要绑定信用卡？
- ✅ **不需要**：Gemini 2.0、智谱AI Flash、Groq
- ⚠️ **需要**：Claude、OpenAI、DeepSeek（充值）、通义千问（充值）

### Q4：API密钥会过期吗？
**不会过期**，但需要注意：
- 账户余额不足会无法使用
- 长期不用可能被平台回收（一般不会）
- 建议定期检查和轮换

### Q5：配置后多久生效？
- **本地开发**：重启应用后立即生效
- **Vercel部署**：添加环境变量后，重新部署（1-2分钟）

### Q6：如何知道使用的是哪个模型？
三种方式：
1. 导航栏"AI设置"badge显示
2. "AI设置"面板查看"当前使用的模型"
3. AI功能返回结果中显示（如代码分析结果顶部）

### Q7：免费模型有什么限制？
- **Gemini**: 有频率限制（通常够用）
- **智谱AI**: 无限制使用
- **Groq**: 每日限额（几百次请求）

### Q8：付费模型大概要花多少钱？
以Claude Haiku为例：
- 1次代码分析（4000 tokens）≈ $0.003（约0.02元）
- 100次分析 ≈ $0.3（约2元）
- 月度使用（500次）≈ $1.5（约10元）

**结论**：即使是付费模型，成本也很低。

---

## 🚀 快速配置（3分钟搞定）

### 推荐配置：智谱AI（完全免费，国内可用）

1. **获取密钥**（1分钟）
   - 访问 https://open.bigmodel.cn/
   - 注册并登录
   - 创建API Key

2. **配置到项目**（1分钟）
   ```bash
   # 编辑.env文件
   ZHIPU_API_KEY=你的密钥
   ZHIPU_MODEL=glm-4-flash
   ```

3. **重启应用**（1分钟）
   ```bash
   python -m uvicorn backend.main:app --reload
   ```

4. **验证成功**
   - 终端显示：`✓ 使用 智谱AI glm-4-flash (完全免费)`
   - 打开应用，点击"AI设置"，看到智谱AI可选择
   - 测试论文摘要功能

**完成！** 🎉

---

## 📞 需要帮助？

如果配置过程中遇到问题：

1. **检查.env格式**
   - 等号两边不要空格
   - 密钥没有引号
   - 文件编码为UTF-8

2. **查看错误日志**
   - 本地：查看终端输出
   - Vercel：Deployments → 选择部署 → Runtime Logs

3. **验证密钥有效性**
   - 在对应平台的控制台测试密钥
   - 检查余额是否充足

4. **联系支持**
   - 各平台都有文档和客服
   - 通常响应很快

---

## 📚 更多文档

- `QUICK_START_AI.md` - AI配置快速开始
- `AI_CONFIG_GUIDE.md` - 完整配置指南
- `GLOBAL_AI_SETTINGS.md` - 全局设置使用说明
- `AI_MODEL_SELECTOR.md` - 模型选择器详解

---

**祝你配置顺利！** 🚀

如有任何问题，随时查看文档或修改配置。系统支持随时切换模型，非常灵活！
