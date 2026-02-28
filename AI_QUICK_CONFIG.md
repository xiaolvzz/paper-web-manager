# ⚡ AI模型快速配置索引

选择你想配置的模型，查看对应的快速指南：

---

## 🎯 推荐配置（3分钟）

### 选择1：完全免费 + 国内可用

**智谱AI GLM-4-Flash**（推荐国内用户）

1. 访问：https://open.bigmodel.cn/
2. 注册并创建API Key
3. 配置：
```bash
ZHIPU_API_KEY=你的密钥
ZHIPU_MODEL=glm-4-flash
```
4. 重启应用

**特点**：完全免费，无限制使用，中文理解强

---

### 选择2：完全免费 + 性能强

**Google Gemini 2.0 Flash**（推荐国外用户）

1. 访问：https://aistudio.google.com/apikey
2. 登录Google账号，创建API Key
3. 配置：
```bash
GEMINI_API_KEY=AIzaSy...
GEMINI_MODEL=gemini-2.0-flash-exp
```
4. 重启应用

**特点**：完全免费，性能接近GPT-4

⚠️ **注意**：Gemini在中国大陆部分地区不可用

---

### 选择3：公司使用

**Anthropic Claude**（推理能力最强）

1. 访问：https://console.anthropic.com/
2. 注册并创建API Key
3. 配置：
```bash
CLAUDE_API_KEY=sk-ant-api03-...
CLAUDE_MODEL=claude-3-5-haiku-20241022
```
4. 重启应用

**特点**：推理能力强，适合复杂代码分析

**成本**：约$0.8/M tokens（很便宜）

---

## 📖 详细配置指南

需要更详细的配置说明？查看完整文档：

| 模型 | 快速链接 | 详细文档 |
|------|---------|----------|
| **所有模型** | - | [API_KEYS_GUIDE.md](API_KEYS_GUIDE.md) |
| **Gemini** | https://aistudio.google.com/apikey | 第1章节 |
| **智谱AI** | https://open.bigmodel.cn/ | 第2章节 |
| **DeepSeek** | https://platform.deepseek.com/ | 第3章节 |
| **通义千问** | https://dashscope.console.aliyun.com/ | 第4章节 |
| **Claude** | https://console.anthropic.com/ | 第5章节 |
| **OpenAI** | https://platform.openai.com/ | 第6章节 |
| **Groq** | https://console.groq.com/ | 第7章节 |

---

## 🎯 配置建议

### 你在国内 → 配置智谱AI
```bash
ZHIPU_API_KEY=xxx
ZHIPU_MODEL=glm-4-flash
```
✅ 完全免费，国内稳定

### 你在国外 → 配置Gemini
```bash
GEMINI_API_KEY=AIzaSy...
GEMINI_MODEL=gemini-2.0-flash-exp
```
✅ 完全免费，性能强

### 你有预算 → 配置Claude
```bash
CLAUDE_API_KEY=sk-ant-api03-...
CLAUDE_MODEL=claude-3-5-haiku-20241022
```
✅ 推理最强，成本不高

### 你想要最便宜的付费模型 → 配置DeepSeek
```bash
DEEPSEEK_API_KEY=sk-...
DEEPSEEK_MODEL=deepseek-chat
```
✅ 0.14元/M tokens，业界最便宜

---

## 🔄 配置流程（统一步骤）

### 1️⃣ 获取API密钥
- 访问对应平台的控制台
- 注册/登录
- 创建API Key
- 复制密钥

### 2️⃣ 添加到项目

**本地开发**：
```bash
# 编辑.env文件
vim .env

# 或使用配置脚本
./configure_ai.sh
```

**Vercel部署**：
- 打开Vercel项目设置
- Environment Variables
- 添加对应的变量
- 保存并重新部署

### 3️⃣ 重启应用
```bash
# 本地
python -m uvicorn backend.main:app --reload

# Vercel会自动部署
```

### 4️⃣ 验证配置
- 打开应用
- 点击"AI设置"
- 查看模型是否可选择
- 测试AI功能

---

## 📱 移动端配置

如果你在手机上配置：

### Vercel部署配置（推荐）
1. 手机浏览器打开 https://vercel.com/
2. 登录你的账号
3. 选择项目 → Settings → Environment Variables
4. 点击"Add" 添加变量
5. 保存并重新部署

### 使用Web编辑器配置
1. 访问 GitHub Web编辑器
2. 打开.env文件
3. 添加配置
4. 提交更改
5. Vercel自动部署

---

## 🆘 故障排查

### 问题：配置后不生效

**检查清单**：
- [ ] .env文件格式正确（无空格，无引号）
- [ ] 已重启应用或重新部署
- [ ] API密钥完整（没有被截断）
- [ ] 账户有余额（付费模型）
- [ ] 网络可以访问（国外模型）

### 问题：API报错

**常见错误**：
- `401 Unauthorized` → 密钥错误或已失效
- `429 Too Many Requests` → 超出限额，等待或升级
- `503 Service Unavailable` → 服务暂时不可用，稍后重试

---

## 🎉 配置成功后

你可以：
1. 在"AI设置"中看到配置的模型
2. 随时切换使用不同的模型
3. 所有AI功能都可以使用了：
   - 📝 论文摘要
   - 💡 创新点提取
   - 🔬 代码架构分析
   - 🌐 PDF翻译（未来）

---

**开始配置吧！** 推荐从免费模型开始 🚀

需要详细说明请查看 [API_KEYS_GUIDE.md](API_KEYS_GUIDE.md)
