# Google Gemini API密钥配置指南

## 🌟 为什么选择Gemini？

- ✅ **完全免费**（2.0-flash-exp版本）
- ✅ **性能强大**（接近GPT-4水平）
- ✅ **无需信用卡**
- ✅ **Google账号即可使用**
- ⚠️ **国内部分地区无法访问**

---

## 📝 获取API密钥（5分钟）

### 步骤1：访问Google AI Studio

在浏览器中打开：
```
https://aistudio.google.com/apikey
```

或访问：
```
https://makersuite.google.com/app/apikey
```

### 步骤2：登录Google账号

- 使用你的Gmail账号登录
- 如果没有Gmail，需要先注册一个

### 步骤3：创建API密钥

页面会显示：
```
┌────────────────────────────────┐
│ Get API key                     │
│                                 │
│ [Create API key] 按钮           │
└────────────────────────────────┘
```

点击步骤：
1. 点击 **"Create API key"** 或 **"Get API key"**
2. 选择或创建Google Cloud项目：
   - 如果已有项目，选择现有项目
   - 如果没有，选择 **"Create API key in new project"**
3. 等待几秒钟，API密钥生成
4. 复制密钥（格式：`AIzaSyXXXXXXXXXXXXXXXXXXXXXX`）

### 步骤4：保存密钥

⚠️ **重要**：虽然密钥可以重复查看，但建议立即保存：
- 复制到文本文件
- 或使用密码管理器保存

---

## ⚙️ 配置到项目

### 方法1：本地开发

#### 编辑.env文件

```bash
# 打开.env文件
nano .env
# 或
vim .env
```

#### 添加配置

```bash
# Google Gemini配置
GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXX
GEMINI_MODEL=gemini-2.0-flash-exp
```

#### 保存并重启

```bash
# 保存文件后，重启应用
python -m uvicorn backend.main:app --reload
```

### 方法2：Vercel部署

1. **登录Vercel控制台**
   https://vercel.com/dashboard

2. **选择项目**
   找到 paper-web-manager 项目

3. **添加环境变量**
   - Settings → Environment Variables
   - 添加变量：
     ```
     Name: GEMINI_API_KEY
     Value: AIzaSyXXXXXXXXXXXXXXXXXXXXXXXX
     ```
   - 再添加一个：
     ```
     Name: GEMINI_MODEL
     Value: gemini-2.0-flash-exp
     ```

4. **保存并部署**
   - 点击Save
   - Vercel自动重新部署（1-2分钟）

---

## 🎨 可用的Gemini模型

### gemini-2.0-flash-exp（推荐）
```bash
GEMINI_MODEL=gemini-2.0-flash-exp
```
- **价格**：完全免费！
- **性能**：接近GPT-4
- **特点**：最新实验版，性能优秀
- **适用**：所有场景（推荐）

### gemini-1.5-flash
```bash
GEMINI_MODEL=gemini-1.5-flash
```
- **价格**：$0.075/M input, $0.3/M output
- **性能**：快速稳定
- **特点**：生产就绪版本
- **适用**：需要稳定API的商业应用

### gemini-1.5-flash-8b
```bash
GEMINI_MODEL=gemini-1.5-flash-8b
```
- **价格**：$0.0375/M input, $0.15/M output
- **性能**：更快，略低质量
- **特点**：8B小模型，速度极快
- **适用**：简单任务，追求速度

### gemini-1.5-pro
```bash
GEMINI_MODEL=gemini-1.5-pro
```
- **价格**：$1.25/M input, $5/M output
- **性能**：最高质量
- **特点**：旗舰版
- **适用**：复杂分析、高质量要求

---

## ✅ 验证配置

### 验证1：查看启动日志

启动应用后看到：
```
✓ 使用 Google Gemini gemini-2.0-flash-exp (完全免费)
```

### 验证2：访问AI设置

1. 打开应用
2. 点击"⚙️ AI设置"
3. 看到 "Google Gemini" 可选择
4. 当前模型显示为 "Google Gemini"

### 验证3：测试功能

- 测试论文摘要生成
- 测试代码架构分析
- 检查返回结果是否正常

---

## 🌍 地区限制问题

### 如果显示"region not available"

**原因**：
- Google AI Studio在某些地区不可用
- 特别是中国大陆

**解决方案**：

#### 方案1：使用智谱AI（推荐国内用户）
```bash
ZHIPU_API_KEY=xxx
ZHIPU_MODEL=glm-4-flash
```
完全免费，国内访问，查看 [ZHIPU_CONFIG.md](ZHIPU_CONFIG.md)

#### 方案2：使用VPN
- 连接到支持的地区（如美国、欧洲）
- 重新访问 Google AI Studio
- 创建API密钥

#### 方案3：使用Groq（免费替代）
```bash
GROQ_API_KEY=gsk_xxx
GROQ_MODEL=llama-3.2-90b-text-preview
```
完全免费，速度快

---

## 💰 成本分析

### 免费版本（2.0-flash-exp）

- **价格**：完全免费
- **限制**：有频率限制（RPM: Requests Per Minute）
  - 通常：15 RPM
  - 对个人用户足够

### 付费版本（1.5-flash/pro）

如果免费版限制不够用，可以升级：

**1.5-flash成本示例**：
```
假设每天使用50次，每次5000 tokens

月度tokens: 50 × 30 × 5000 = 7.5M tokens
月度成本: 7.5M × $0.075 = $0.56（约4元）
```

**结论**：即使是付费版，成本也很低

---

## 🔧 高级配置

### 1. 设置API限制

在Google Cloud Console中可以：
- 限制API的使用配额
- 设置预算提醒
- 查看详细使用统计

### 2. 多项目管理

如果你有多个项目：
```bash
# 项目A
GEMINI_API_KEY=key_for_project_a

# 项目B
GEMINI_API_KEY=key_for_project_b
```

在Google AI Studio中可以：
- 为每个项目创建独立的API Key
- 方便追踪每个项目的使用情况

### 3. 使用Google Cloud Project

如果需要更高级的功能：
1. 访问 https://console.cloud.google.com/
2. 启用 Generative AI API
3. 设置计费账户
4. 获得更高的配额和更多功能

---

## ❓ 常见问题

### Q1：Gemini完全免费吗？
**2.0-flash-exp**: 完全免费
**1.5-flash/pro**: 需要付费

推荐使用 `gemini-2.0-flash-exp`，性能强且免费。

### Q2：免费版本有什么限制？
- **频率限制**：15 RPM（每分钟15次请求）
- **每日限制**：1500次请求/天
- **上下文限制**：100万tokens

对个人使用完全足够！

### Q3：如何升级到付费版本？
1. 在Google Cloud Console设置计费账户
2. 启用Generative AI API计费
3. 修改模型配置为 `gemini-1.5-flash`

### Q4：API密钥会过期吗？
**不会过期**，但：
- 长期未使用可能被停用
- 可以在控制台随时查看和管理

### Q5：Gemini vs ChatGPT哪个更好？
**Gemini优势**：
- 完全免费
- 性能接近GPT-4
- Google生态集成

**ChatGPT优势**：
- 知名度高
- 生态更完善
- 部分任务更准确

**建议**：免费的Gemini 2.0已经非常强大，优先尝试！

### Q6：国内用户能用Gemini吗？
**可能性**：
- 部分地区可以访问
- 部分地区被限制

**替代方案**：
- 使用智谱AI GLM-4-Flash（完全免费，国内稳定）
- 使用VPN访问Gemini

---

## 🔗 官方资源

- **API Key管理**: https://aistudio.google.com/apikey
- **官方文档**: https://ai.google.dev/docs
- **价格说明**: https://ai.google.dev/pricing
- **快速开始**: https://ai.google.dev/tutorials/python_quickstart
- **Gemini API参考**: https://ai.google.dev/api/rest

---

## 🎓 最佳实践

### 1. 使用免费版本

除非有特殊需求，免费的2.0-flash-exp完全够用：
```bash
GEMINI_MODEL=gemini-2.0-flash-exp
```

### 2. 处理频率限制

如果遇到15 RPM限制：
- 添加请求间隔（系统已处理）
- 或升级到付费版本（无限制）

### 3. 监控使用情况

在Google Cloud Console查看：
- API调用次数
- 成功/失败率
- 响应时间

---

**开始使用Gemini吧！** 🚀

完全免费的AI模型，性能强大，值得拥有！
