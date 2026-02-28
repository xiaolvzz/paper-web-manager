# Anthropic Claude API密钥配置指南

## 🌟 为什么选择Claude？

- ✅ **推理能力最强**（超越GPT-4）
- ✅ **代码理解优秀**（特别适合代码分析）
- ✅ **安全可靠**（Anthropic专注AI安全）
- ✅ **支持长文本**（200K tokens上下文）
- ⚠️ **需要付费**（但性价比高）

---

## 📝 获取API密钥（5分钟）

### 步骤1：访问Anthropic Console

在浏览器中打开：
```
https://console.anthropic.com/
```

### 步骤2：注册账号

1. **点击"Sign Up"**
2. **输入邮箱地址**
3. **验证邮箱**
   - 查收验证邮件
   - 点击邮件中的验证链接
4. **设置密码**

### 步骤3：设置计费（首次使用）

⚠️ **Claude需要绑定信用卡才能使用**

1. **进入Billing页面**
   - 左侧菜单 → Settings → Billing
   - 或访问：https://console.anthropic.com/settings/billing

2. **添加支付方式**
   - 点击"Add payment method"
   - 输入信用卡信息
   - 支持Visa、MasterCard、美国运通

3. **设置预算限额**（可选但推荐）
   - 点击"Usage limits"
   - 设置每月最高消费（如$10、$20）
   - 防止意外超支

4. **充值**（可选）
   - 可以预充值（如$10）
   - 或使用按量计费（推荐）

### 步骤4：创建API密钥

1. **进入API Keys页面**
   - 左侧菜单 → API Keys
   - 或访问：https://console.anthropic.com/settings/keys

2. **创建新密钥**
   - 点击 **"Create Key"** 按钮
   - 输入密钥名称（如：paper-manager）
   - 点击"Create"

3. **复制密钥**
   - 密钥格式：`sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - ⚠️ **密钥只显示一次！** 请立即复制保存
   - 如果忘记保存，需要删除并重新创建

---

## ⚙️ 配置到项目

### 方法1：本地开发

#### 编辑.env文件
```bash
# Claude配置
CLAUDE_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
CLAUDE_MODEL=claude-3-5-haiku-20241022
```

#### 重启应用
```bash
python -m uvicorn backend.main:app --reload
```

#### 验证
终端应显示：
```
✓ 使用 Anthropic Claude claude-3-5-haiku-20241022
```

---

### 方法2：Vercel部署

1. **进入Vercel项目设置**
   https://vercel.com/dashboard → 选择项目 → Settings

2. **添加环境变量**
   - Environment Variables
   - 添加第一个变量：
     ```
     Name: CLAUDE_API_KEY
     Value: sk-ant-api03-xxxxx...
     ```
   - 添加第二个变量：
     ```
     Name: CLAUDE_MODEL
     Value: claude-3-5-haiku-20241022
     ```

3. **选择环境**
   - Production: ✓（必选）
   - Preview: ✓（推荐）
   - Development: ✓（推荐）

4. **保存并部署**
   - 点击Save
   - 等待自动部署（1-2分钟）

---

## 🎨 可用的Claude模型

### claude-3-5-haiku-20241022（推荐）
```bash
CLAUDE_MODEL=claude-3-5-haiku-20241022
```
- **价格**：$0.8/M input, $4/M output
- **特点**：快速、便宜、质量高
- **速度**：最快的Claude模型
- **适用**：日常使用、代码分析、论文摘要
- **推荐指数**：⭐⭐⭐⭐⭐

### claude-3-5-sonnet-20241022
```bash
CLAUDE_MODEL=claude-3-5-sonnet-20241022
```
- **价格**：$3/M input, $15/M output
- **特点**：平衡版，质量更好
- **适用**：复杂推理、深度分析
- **推荐指数**：⭐⭐⭐⭐

### claude-3-opus-20240229
```bash
CLAUDE_MODEL=claude-3-opus-20240229
```
- **价格**：$15/M input, $75/M output（很贵）
- **特点**：最强版本，但贵很多
- **适用**：最高质量要求
- **推荐指数**：⭐⭐⭐（性价比低）

---

## 💰 成本估算

### 使用claude-3-5-haiku的成本

#### 场景1：论文摘要（每次约2000 tokens）
```
100次摘要 = 0.2M input + 0.05M output
成本 = 0.2 × $0.8 + 0.05 × $4
    = $0.16 + $0.20
    = $0.36（约2.5元）
```

#### 场景2：代码架构分析（每次约6000 tokens）
```
50次分析 = 0.3M input + 0.1M output
成本 = 0.3 × $0.8 + 0.1 × $4
    = $0.24 + $0.40
    = $0.64（约4.5元）
```

#### 月度使用估算
假设每月：
- 200次论文摘要
- 100次代码分析
- 50次创新点提取

**总成本**：约$3-5（20-35元/月）

**结论**：Claude Haiku性价比很高，推荐使用！

---

## 🎯 与其他模型对比

### Claude vs GPT-4
- **推理能力**：Claude > GPT-4
- **代码理解**：Claude ≈ GPT-4
- **价格**：Claude Haiku便宜很多

### Claude vs Gemini
- **质量**：Claude略胜
- **成本**：Gemini免费（Claude付费）
- **建议**：日常用Gemini，复杂任务用Claude

### Claude vs DeepSeek
- **质量**：Claude更好
- **成本**：DeepSeek便宜10倍（$0.14 vs $0.8）
- **建议**：预算充足选Claude，预算有限选DeepSeek

---

## ✅ 验证配置成功

### 1. 启动日志检查
```
✓ 使用 Anthropic Claude claude-3-5-haiku-20241022
```

### 2. 健康检查接口
```bash
curl http://localhost:8000/api/ai/health
```

返回：
```json
{
  "status": "healthy",
  "provider": "Anthropic Claude",
  "model": "claude-3-5-haiku-20241022",
  "configured": true
}
```

### 3. 前端验证
- 导航栏显示：**⚙️ AI设置 [Claude]**
- AI设置面板中"Anthropic Claude"可选择
- 当前模型显示为"Anthropic Claude"

---

## 🔒 安全建议

### 1. 保护API密钥
- ❌ 不要提交到Git
- ❌ 不要分享给他人
- ✅ 使用环境变量
- ✅ 定期轮换密钥

### 2. 设置消费限额
在Console → Settings → Billing → Usage limits：
- 每月限额（如$20）
- 每日限额（如$5）
- 超限后API自动停止

### 3. 监控使用情况
- Console → Usage 查看实时使用
- 设置邮件提醒（余额不足时）
- 定期查看账单

### 4. 密钥泄露处理
如果密钥泄露：
1. 立即删除泄露的密钥
2. 检查Usage查看异常使用
3. 创建新密钥并更新配置
4. 联系Anthropic支持（如有异常扣费）

---

## 🏢 公司使用

### 如果你有公司提供的Claude API密钥

直接配置即可：
```bash
CLAUDE_API_KEY=sk-ant-api03-公司提供的密钥
CLAUDE_MODEL=claude-3-5-haiku-20241022
```

### 企业账户优势
- 更高的API限额
- 专属技术支持
- 团队协作功能
- 统一计费管理

---

## 🚀 快速测试

### 测试API密钥是否有效

```bash
# 使用curl测试
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $CLAUDE_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-3-5-haiku-20241022",
    "max_tokens": 100,
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

返回JSON响应说明密钥有效。

---

## 💡 使用建议

### 日常使用
配合免费模型使用：
```bash
# 主力：Gemini（免费）
GEMINI_API_KEY=xxx

# 复杂任务：Claude（付费）
CLAUDE_API_KEY=sk-ant-api03-xxx
```

在AI设置中随时切换！

### 代码分析专用
Claude特别适合代码架构分析：
```bash
CLAUDE_API_KEY=sk-ant-api03-xxx
CLAUDE_MODEL=claude-3-5-haiku-20241022
```

推理能力强，能深入理解代码逻辑。

### 成本控制
- 简单任务用免费模型（Gemini、智谱AI）
- 复杂任务才用Claude
- 通过AI设置随时切换

---

## 📞 获取帮助

### 官方支持
- **文档**: https://docs.anthropic.com/
- **API参考**: https://docs.anthropic.com/claude/reference/
- **社区**: https://www.anthropic.com/community
- **支持**: support@anthropic.com

### 常见问题
- **计费问题**: 查看Console → Billing
- **API错误**: 查看API文档排查
- **账户问题**: 联系官方支持

---

## 🎉 配置完成

配置成功后：

1. ✅ 导航栏显示"Claude"
2. ✅ AI设置中可以选择Claude
3. ✅ 所有AI功能使用Claude进行分析
4. ✅ 享受最强的推理能力！

---

**Claude是最强的AI推理模型，值得配置！** 🎯

查看其他模型配置：[API_KEYS_GUIDE.md](../API_KEYS_GUIDE.md)
