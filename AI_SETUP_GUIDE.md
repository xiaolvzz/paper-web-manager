# AI功能配置指南

## 🎯 推荐方案

### 方案A：最佳性价比（强烈推荐）⭐⭐⭐⭐⭐
```
主力：DeepSeek (0.1元/百万tokens，新用户送500万tokens)
备用：智谱AI (100万tokens/月免费)
```

### 方案B：纯免费方案
```
主力：智谱AI (100万tokens/月免费)
备用：通义千问 (新用户免费)
```

---

## 📋 各AI提供商对比

| 提供商 | 价格 | 免费额度 | 质量 | 访问 | 推荐指数 |
|--------|------|---------|------|------|---------|
| **DeepSeek** | 0.1元/百万tokens | 新用户500万 | ⭐⭐⭐⭐ | 国内直接访问 | ⭐⭐⭐⭐⭐ |
| **智谱AI (GLM-4)** | 0.5元/百万tokens | 100万/月 | ⭐⭐⭐⭐ | 国内直接访问 | ⭐⭐⭐⭐ |
| **通义千问** | 0.4元/百万tokens | 新用户100万 | ⭐⭐⭐⭐ | 需阿里云账号 | ⭐⭐⭐⭐ |
| **Groq** | 完全免费 | 无限制 | ⭐⭐⭐ | 可能需要梯子 | ⭐⭐⭐ |

---

## 🚀 配置步骤

### 方案1：使用DeepSeek（推荐）

#### 1. 注册DeepSeek账号
1. 访问：https://platform.deepseek.com/
2. 注册账号（可用邮箱或手机）
3. 新用户自动获得 **500万tokens** 免费额度

#### 2. 获取API密钥
1. 登录后点击右上角头像 → **API Keys**
2. 点击 **Create API Key**
3. 复制生成的密钥（格式：`sk-xxxxxx`）

#### 3. 配置到Vercel
1. 打开你的Vercel项目：https://vercel.com/dashboard
2. 选择 `paper-web-manager` 项目
3. 点击 **Settings** → **Environment Variables**
4. 添加新变量：
   - **Name**: `DEEPSEEK_API_KEY`
   - **Value**: 粘贴你的API密钥
   - **Environment**: 全选（Production, Preview, Development）
5. 点击 **Save**
6. 返回 **Deployments** 页面，点击最新部署的 **⋯** → **Redeploy**

#### 4. 验证配置
访问：https://paper-web-manager.vercel.app/api/ai/health

应该看到：
```json
{
  "status": "healthy",
  "provider": "DeepSeek",
  "model": "deepseek-chat",
  "configured": true
}
```

---

### 方案2：使用智谱AI（中文优秀）

#### 1. 注册智谱AI账号
1. 访问：https://open.bigmodel.cn/
2. 注册账号（需要手机号验证）
3. 实名认证后获得 **100万tokens/月** 免费额度

#### 2. 获取API密钥
1. 登录后点击 **控制台**
2. 左侧菜单点击 **API密钥**
3. 点击 **创建密钥**
4. 复制生成的密钥

#### 3. 配置到Vercel
添加环境变量：
- **Name**: `ZHIPU_API_KEY`
- **Value**: 你的智谱AI密钥
- 保存后重新部署

---

### 方案3：使用通义千问

#### 1. 开通阿里云DashScope
1. 访问：https://dashscope.aliyun.com/
2. 登录阿里云账号
3. 开通服务，新用户有免费额度

#### 2. 获取API密钥
1. 进入控制台
2. 点击 **API-KEY管理**
3. 创建并复制密钥

#### 3. 配置到Vercel
添加环境变量：
- **Name**: `QWEN_API_KEY`
- **Value**: 你的通义千问密钥

---

### 方案4：使用Groq（备选）

如果你能访问Groq（可能需要梯子）：

#### 1. 注册Groq账号
访问：https://console.groq.com/

#### 2. 获取API密钥
注册后在控制台创建API Key

#### 3. 配置到Vercel
添加环境变量：
- **Name**: `GROQ_API_KEY`
- **Value**: 你的Groq密钥

---

## 🔄 自动优先级选择

系统会按以下优先级自动选择可用的AI服务：

1. **DeepSeek** （性价比最高）
2. **智谱AI** （中文理解优秀）
3. **通义千问** （阿里云生态）
4. **Groq** （备选）

**你可以同时配置多个**，系统会自动选择第一个可用的。

---

## 💰 成本估算

### 个人使用（每月约100篇论文，每篇10次对话）

| 提供商 | 每月tokens消耗 | 费用 |
|--------|---------------|------|
| DeepSeek | ~200万tokens | 0.2元 💰 |
| 智谱AI | ~200万tokens | 1元（前100万免费） |
| 通义千问 | ~200万tokens | 0.8元 |
| Groq | ~200万tokens | 免费 🎉 |

**推荐**：使用DeepSeek + 智谱AI组合，几乎零成本！

---

## 🧪 测试AI功能

### 1. 健康检查
```bash
curl https://paper-web-manager.vercel.app/api/ai/health
```

### 2. 前端测试
1. 添加一篇论文
2. 点击"一键分析"按钮
3. 或使用AI对话功能提问

---

## ❓ 常见问题

### Q1: 配置后还是显示"未配置"？
**A**: 确保：
1. 环境变量名称正确（区分大小写）
2. 保存后重新部署了Vercel项目
3. 等待2-3分钟让部署完成

### Q2: 提示"API调用失败"？
**A**: 检查：
1. API密钥是否正确复制（没有多余空格）
2. 账户是否还有免费额度
3. 是否需要实名认证（智谱AI需要）

### Q3: 可以同时配置多个吗？
**A**: 可以！系统会自动选择第一个可用的，其他作为备份。

### Q4: 如何查看当前使用哪个AI？
**A**: 访问 `/api/ai/health` 查看 `provider` 字段。

### Q5: DeepSeek和智谱AI哪个更好？
**A**:
- **DeepSeek**: 成本最低，代码理解强，英文论文推荐
- **智谱AI**: 中文理解优秀，中文论文推荐
- 建议两个都配置，系统会优先用DeepSeek

---

## 📞 获取帮助

如果遇到问题：
1. 查看Vercel部署日志
2. 检查浏览器控制台（F12）
3. 访问 `/api/ai/health` 检查配置状态

---

**祝你使用愉快！如有问题随时反馈。** 🎉
