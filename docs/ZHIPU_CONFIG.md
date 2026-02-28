# 智谱AI (GLM-4) API密钥配置指南

## 🌟 为什么选择智谱AI？

- ✅ **完全免费**（GLM-4-Flash无限制使用）
- ✅ **国内访问稳定**（无需VPN）
- ✅ **中文理解优秀**（国产大模型）
- ✅ **简单易用**（手机号即可注册）
- 🎯 **强烈推荐中国用户使用**

---

## 📝 获取API密钥（3分钟）

### 步骤1：访问智谱AI开放平台

在浏览器中打开：
```
https://open.bigmodel.cn/
```

### 步骤2：注册账号

1. **点击右上角"注册"**

2. **选择注册方式**
   - 推荐：手机号注册（快速）
   - 备选：邮箱注册

3. **手机号注册流程**
   - 输入手机号
   - 获取验证码
   - 设置密码
   - 同意用户协议

4. **实名认证**
   - 输入真实姓名和身份证号
   - 人脸识别验证
   - 通常几分钟完成

### 步骤3：进入控制台

1. **登录后点击"控制台"**
   - 右上角头像 → 控制台
   - 或访问：https://open.bigmodel.cn/usercenter/apikeys

2. **首次进入会赠送免费tokens**
   - 新用户通常赠送25M tokens
   - 足够使用很长时间

### 步骤4：创建API密钥

1. **进入API Keys页面**
   ```
   https://open.bigmodel.cn/usercenter/apikeys
   ```

2. **点击"创建API Key"**
   - 输入名称：如"论文管理系统"
   - 点击"确定"

3. **复制密钥**
   - 密钥格式：长字符串（没有特殊前缀）
   - ⚠️ **密钥只显示一次**
   - 立即复制并保存

4. **查看密钥状态**
   - 可以查看每个密钥的使用情况
   - 可以随时删除或禁用密钥

---

## ⚙️ 配置到项目

### 方法1：本地开发

#### 编辑.env文件
```bash
# 智谱AI配置
ZHIPU_API_KEY=你的完整API密钥字符串
ZHIPU_MODEL=glm-4-flash
```

**完整示例**：
```bash
# 数据库配置
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJhbGci...

# 智谱AI配置
ZHIPU_API_KEY=1234567890abcdefghijklmnopqrstuvwxyz  # 示例格式
ZHIPU_MODEL=glm-4-flash
```

#### 保存并重启
```bash
python -m uvicorn backend.main:app --reload
```

---

### 方法2：Vercel部署

1. **Vercel项目设置**
   - 打开项目 → Settings → Environment Variables

2. **添加ZHIPU_API_KEY**
   ```
   Name: ZHIPU_API_KEY
   Value: 你的API密钥（完整字符串）
   Environments: Production, Preview, Development（全选）
   ```
   点击Save

3. **添加ZHIPU_MODEL**
   ```
   Name: ZHIPU_MODEL
   Value: glm-4-flash
   Environments: Production, Preview, Development（全选）
   ```
   点击Save

4. **重新部署**
   - Vercel自动触发部署
   - 等待1-2分钟完成

---

## 🎨 智谱AI模型选择

### glm-4-flash（强烈推荐）
```bash
ZHIPU_MODEL=glm-4-flash
```
- **价格**：完全免费！无限制使用
- **性能**：接近GPT-3.5水平
- **速度**：快速响应
- **适用**：所有场景（推荐）
- **推荐指数**：⭐⭐⭐⭐⭐

### glm-4-air
```bash
ZHIPU_MODEL=glm-4-air
```
- **价格**：1元/M input, 1元/M output
- **性能**：更强的理解能力
- **适用**：需要更高质量时
- **推荐指数**：⭐⭐⭐⭐

### glm-4-plus
```bash
ZHIPU_MODEL=glm-4-plus
```
- **价格**：50元/M input, 50元/M output
- **性能**：旗舰级别
- **适用**：最高质量要求
- **推荐指数**：⭐⭐⭐

### glm-4-long（长文本专用）
```bash
ZHIPU_MODEL=glm-4-long
```
- **价格**：1元/M tokens
- **特点**：支持100万tokens超长上下文
- **适用**：分析整本书、超长论文

### glm-4v（视觉模型）
```bash
ZHIPU_MODEL=glm-4v
```
- **特点**：支持图片理解
- **适用**：论文中的图表分析
- **价格**：5元/M tokens

---

## ✅ 验证配置

### 验证1：启动日志
```
✓ 使用 智谱AI (GLM-4) glm-4-flash (完全免费)
```

### 验证2：访问AI设置
1. 打开应用
2. 点击"⚙️ AI设置"
3. 看到"智谱AI (GLM-4)"显示为可选择

### 验证3：API接口测试
```bash
curl http://localhost:8000/api/ai/health
```

返回：
```json
{
  "status": "healthy",
  "provider": "智谱AI (GLM-4)",
  "model": "glm-4-flash",
  "configured": true
}
```

### 验证4：实际使用
- 测试论文摘要生成
- 测试代码架构分析
- 检查分析结果顶部显示"智谱AI (GLM-4)"

---

## 💡 使用建议

### 推荐配置1：纯免费方案
```bash
# 智谱AI作为主力（完全免费）
ZHIPU_API_KEY=xxx
ZHIPU_MODEL=glm-4-flash
```
适合：个人学习、日常使用

### 推荐配置2：国内用户最佳
```bash
# 主力：智谱AI（免费）
ZHIPU_API_KEY=xxx
ZHIPU_MODEL=glm-4-flash

# 备用：通义千问（便宜）
QWEN_API_KEY=sk-xxx
QWEN_MODEL=qwen-turbo
```
适合：国内用户，稳定访问

### 推荐配置3：质量优先
```bash
# 日常：智谱AI（免费）
ZHIPU_API_KEY=xxx
ZHIPU_MODEL=glm-4-flash

# 复杂：Claude（推理强）
CLAUDE_API_KEY=sk-ant-api03-xxx
CLAUDE_MODEL=claude-3-5-haiku-20241022
```
适合：有预算，追求质量

---

## 🎓 进阶功能

### 1. 查看使用统计

在控制台查看：
- 每日调用次数
- Token消耗量
- 费用明细

### 2. 管理多个密钥

创建多个密钥用于：
- 不同项目
- 开发/生产环境分离
- 团队成员分配

### 3. 设置密钥权限

可以为每个密钥设置：
- 调用频率限制
- 使用模型限制
- 有效期限制

### 4. 申请企业认证

企业用户可以：
- 获得更高的免费额度
- 更高的API限额
- 专属技术支持

---

## ❓ 常见问题

### Q1：glm-4-flash真的完全免费吗？
**是的！**
- 无限制使用
- 无需绑定信用卡
- 不收取任何费用
- 新用户额外赠送tokens

### Q2：免费模型和付费模型差别大吗？
**差别不大**：
- glm-4-flash：适合90%的场景
- glm-4-air/plus：质量提升约10-20%
- 建议先用免费版，不够用再升级

### Q3：如何充值？
如果免费额度用完：
1. 控制台 → 充值中心
2. 选择充值金额
3. 支付宝/微信支付
4. 到账即可使用

### Q4：API密钥格式是什么样的？
智谱AI密钥格式：
- 长字符串，无特殊前缀
- 示例：`1234567890abcdef...`（实际更长）
- 与OpenAI的`sk-`前缀不同

### Q5：密钥找不到了怎么办？
- 密钥不会丢失，在控制台永久保存
- 访问 https://open.bigmodel.cn/usercenter/apikeys 查看
- 如果确实找不到，删除旧的创建新的

### Q6：可以在多个项目中使用同一个密钥吗？
**可以！**
- 同一个密钥可用于多个项目
- 但建议为每个项目创建独立密钥
- 方便管理和追踪使用情况

### Q7：智谱AI vs Gemini选哪个？
**国内用户**：智谱AI（访问稳定）
**国外用户**：Gemini（性能略好）
**最佳方案**：两个都配置，互为备用

### Q8：为什么配置后还是用的其他模型？
**原因**：系统优先级
- 如果同时配置了Gemini和智谱AI
- 系统默认优先用Gemini

**解决**：
- 方法1：删除Gemini配置，只保留智谱AI
- 方法2：在"AI设置"中手动选择智谱AI

---

## 🔗 官方资源

- **开放平台首页**: https://open.bigmodel.cn/
- **API Key管理**: https://open.bigmodel.cn/usercenter/apikeys
- **官方文档**: https://open.bigmodel.cn/dev/api
- **模型介绍**: https://open.bigmodel.cn/dev/howuse/model
- **价格说明**: https://open.bigmodel.cn/pricing
- **开发示例**: https://open.bigmodel.cn/dev/howuse/introduction

---

## 🎉 开始使用

配置完成后：

1. 重启应用
2. 打开"AI设置"
3. 看到"智谱AI (GLM-4)"可选择
4. 点击"选择"使其生效
5. 开始使用所有AI功能！

---

**智谱AI GLM-4-Flash：国内用户的最佳选择！** 🚀

完全免费，无限制使用，中文理解强，访问稳定。强烈推荐！

查看其他模型配置：[API_KEYS_GUIDE.md](../API_KEYS_GUIDE.md)
