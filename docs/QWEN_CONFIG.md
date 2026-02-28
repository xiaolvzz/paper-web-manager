# 通义千问（Qwen）API密钥配置详细指南

## 📋 目录
1. [快速开始（5分钟）](#快速开始)
2. [详细步骤（带截图说明）](#详细步骤)
3. [配置到项目](#配置到项目)
4. [验证配置](#验证配置)
5. [常见问题](#常见问题)

---

## ⚡ 快速开始

### 第一步：获取API密钥

1. **访问阿里云DashScope**
   ```
   https://dashscope.console.aliyun.com/
   ```

2. **登录阿里云账号**
   - 如果没有阿里云账号，点击"免费注册"
   - 需要手机号和实名认证

3. **开通DashScope服务**
   - 点击"免费开通"
   - 阅读并同意服务协议

4. **创建API密钥**
   - 进入API-KEY管理：https://dashscope.console.aliyun.com/apiKey
   - 点击"创建新的API-KEY"
   - 复制生成的密钥（类似：`sk-xxxxxxxxxx`）

### 第二步：配置到项目

编辑 `.env` 文件：
```bash
QWEN_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxx
QWEN_MODEL=qwen-turbo
```

### 第三步：重启应用
```bash
python -m uvicorn backend.main:app --reload
```

### 第四步：验证
打开应用，点击"AI设置"，看到"通义千问"可选择，配置成功！

---

## 📖 详细步骤

### 步骤1：注册阿里云账号

如果你还没有阿里云账号：

1. **访问阿里云官网**
   https://www.aliyun.com/

2. **点击"免费注册"**
   - 选择注册方式：手机号注册（推荐）
   - 输入手机号，获取验证码
   - 设置密码

3. **实名认证**
   - 个人认证：上传身份证
   - 企业认证：上传营业执照
   - 审核时间：通常几分钟到几小时

### 步骤2：开通DashScope服务

1. **访问DashScope控制台**
   https://dashscope.console.aliyun.com/

2. **首次进入会提示开通**
   - 点击"免费开通"
   - 阅读服务协议
   - 点击"立即开通"

3. **服务开通成功**
   - 自动跳转到控制台首页
   - 显示可用模型列表

### 步骤3：获取免费额度

阿里云通常为新用户提供免费额度：

1. **查看资源包**
   - 控制台首页 → "资源包管理"
   - 查看当前可用的tokens额度

2. **领取免费额度**（如果有活动）
   - 控制台可能显示免费试用活动
   - 点击领取

3. **购买资源包**（可选）
   - 如果免费额度用完
   - 可购买资源包（比按量计费更便宜）

### 步骤4：创建API密钥

1. **进入API-KEY管理**
   - 方式1：控制台首页 → 点击右上角头像 → "API-KEY管理"
   - 方式2：直接访问 https://dashscope.console.aliyun.com/apiKey

2. **创建新密钥**
   - 点击"创建新的API-KEY"按钮
   - 输入密钥描述（如：论文管理系统）
   - 点击"确定"

3. **复制密钥**
   - 密钥格式：`sk-xxxxxxxxxxxxxxxxxxxxxxxx`
   - ⚠️ **重要**：密钥只显示一次，请立即复制保存
   - 建议保存到密码管理器

4. **管理密钥**
   - 可以创建多个密钥（用于不同项目）
   - 可以随时删除不用的密钥
   - 可以查看每个密钥的使用情况

---

## ⚙️ 配置到项目

### 方法1：本地开发（推荐新手）

#### 找到.env文件
```bash
cd /path/to/paper-web-manager
ls -la .env
```

如果.env文件不存在，创建它：
```bash
cp .env.example .env  # 如果有example文件
# 或
touch .env
```

#### 编辑.env文件
```bash
# 使用任意文本编辑器
nano .env
# 或
vim .env
# 或在VS Code中打开
```

#### 添加配置
```bash
# 通义千问配置
QWEN_API_KEY=sk-your-actual-api-key-here
QWEN_MODEL=qwen-turbo
```

**完整示例**：
```bash
# 数据库配置
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJhbGci...

# AI模型配置
QWEN_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxx
QWEN_MODEL=qwen-turbo
```

#### 保存文件
- nano: `Ctrl + X`，然后 `Y`，然后 `Enter`
- vim: `ESC`，然后 `:wq`

#### 重启应用
```bash
# 停止当前运行（Ctrl + C）
# 重新启动
python -m uvicorn backend.main:app --reload
```

---

### 方法2：Vercel部署

#### 步骤：
1. **登录Vercel**
   https://vercel.com/dashboard

2. **选择项目**
   找到你的 paper-web-manager 项目

3. **进入设置**
   点击项目 → **Settings** 标签

4. **添加环境变量**
   - 左侧菜单 → **Environment Variables**
   - 点击顶部的输入框

5. **添加QWEN_API_KEY**
   - Name: `QWEN_API_KEY`
   - Value: `sk-xxxxxxxxxxxxxxxxxxxxxxxxxx`（你的实际密钥）
   - Environments: 选择所有（Production, Preview, Development）
   - 点击 **Save**

6. **添加QWEN_MODEL**
   - Name: `QWEN_MODEL`
   - Value: `qwen-turbo`
   - Environments: 选择所有
   - 点击 **Save**

7. **重新部署**
   - Vercel会自动触发重新部署
   - 或手动触发：Deployments → 最新部署 → 右侧三点菜单 → Redeploy

8. **等待部署完成**
   - 通常1-2分钟
   - 部署状态变为"Ready"即完成

---

### 方法3：使用配置脚本（仅本地）

如果你在Linux/Mac系统：

```bash
./configure_ai.sh
```

按提示选择"通义千问"，输入API密钥即可。

---

## ✅ 验证配置

### 验证1：查看启动日志

启动应用后，终端应该显示：

```bash
✓ 使用 通义千问 qwen-turbo
```

如果看到这行，说明配置成功！

### 验证2：访问健康检查接口

```bash
curl http://localhost:8000/api/ai/health
```

返回示例：
```json
{
  "status": "healthy",
  "provider": "通义千问",
  "model": "qwen-turbo",
  "configured": true
}
```

### 验证3：打开AI设置面板

1. 打开论文管理系统
2. 点击导航栏的"⚙️ AI设置"
3. 查看模型列表

**配置成功标志**：
- ✅ "通义千问 (qwen-turbo) - 廉价"显示为可选择状态
- ✅ 可以点击"选择"按钮
- ✅ 选择后，badge显示"通义千问"

### 验证4：测试AI功能

1. **测试论文摘要**
   - 打开任意论文详情页
   - 点击"生成摘要"
   - 查看是否正常返回结果

2. **测试代码分析**
   - 输入GitHub源码链接
   - 点击"分析架构"
   - 查看分析结果顶部显示的模型信息

---

## 🎨 可选的模型配置

通义千问提供多个模型，根据需求选择：

### qwen-turbo（推荐）
```bash
QWEN_MODEL=qwen-turbo
```
- **价格**：0.3元/M input, 0.6元/M output
- **特点**：快速、便宜、够用
- **适用**：日常使用、论文摘要、简单分析

### qwen-plus
```bash
QWEN_MODEL=qwen-plus
```
- **价格**：4元/M input, 8元/M output
- **特点**：质量更高，理解能力强
- **适用**：复杂任务、代码分析

### qwen-max
```bash
QWEN_MODEL=qwen-max
```
- **价格**：20元/M input, 60元/M output
- **特点**：最强版本
- **适用**：最高质量要求

### qwen-long
```bash
QWEN_MODEL=qwen-long
```
- **价格**：0.5元/M input, 2元/M output
- **特点**：支持100万tokens超长上下文
- **适用**：长文档分析、整本书摘要

### qwen-coder-turbo（代码专用）
```bash
QWEN_MODEL=qwen-coder-turbo
```
- **价格**：2元/M input, 6元/M output
- **特点**：专门优化代码理解和生成
- **适用**：代码架构分析、代码生成

---

## 💰 成本估算

### 使用qwen-turbo的成本

假设使用场景：
- 每次代码分析：约4000 tokens
- 每次论文摘要：约1000 tokens
- 每月使用100次各类功能

**计算**：
```
输入tokens: 100 × (4000 + 1000) = 500,000 tokens = 0.5M tokens
成本: 0.5M × 0.3元 = 0.15元

输出tokens: 约100,000 tokens = 0.1M tokens
成本: 0.1M × 0.6元 = 0.06元

总计: 0.15 + 0.06 = 0.21元/月
```

**结论**：即使重度使用，每月成本不到1元！

### 免费额度可用多久？

新用户通常赠送100万tokens（1M）：
```
1M tokens ÷ 5000 tokens/次 = 200次使用
```

按每天使用5次计算，可免费使用40天！

---

## 🔧 高级配置

### 同时配置多个阿里云模型

```bash
# 通用任务用turbo（便宜）
QWEN_API_KEY=sk-xxx
QWEN_MODEL=qwen-turbo

# 如果想用代码专用模型，可以在代码中动态切换
# 或者配置多个.env文件
```

### 设置API密钥权限

在DashScope控制台可以：
1. 设置密钥的访问权限
2. 限制密钥的QPS（每秒请求数）
3. 设置密钥的有效期
4. 查看密钥的使用统计

### 监控使用情况

在控制台查看：
1. **用量统计**
   - Dashboard → 用量统计
   - 查看每天/每月的token消耗

2. **费用账单**
   - 费用中心 → 账单明细
   - 查看详细花费

3. **设置预警**
   - 费用中心 → 余额预警
   - 设置余额不足提醒

---

## 📱 移动端配置

### 使用支付宝

如果你在手机上：
1. 打开支付宝
2. 搜索"阿里云"
3. 进入阿里云小程序
4. 登录并管理资源

### 使用浏览器

手机浏览器访问：
- https://dashscope.console.aliyun.com/
- 横屏使用体验更好

---

## ❓ 常见问题

### Q1：通义千问和Qwen是同一个吗？
**是的！**
- 通义千问：中文品牌名
- Qwen (千问)：英文/技术名称
- 都是阿里云的大语言模型

### Q2：需要充值吗？
**看情况**：
- 新用户有免费额度（通常100万tokens）
- 免费额度用完后需要充值
- 充值方式：支付宝、网银

### Q3：最低充值多少？
- 按量计费：用多少扣多少，无最低充值
- 购买资源包：有不同规格（如50元、100元）

### Q4：Qwen和其他模型比怎么样？

**对比Gemini**：
- Gemini：免费，但国内可能无法访问
- Qwen：便宜，国内访问稳定

**对比Claude**：
- Claude：推理能力更强，但贵10倍
- Qwen：性价比高，中文理解好

**对比DeepSeek**：
- DeepSeek：更便宜（0.14元 vs 0.3元）
- Qwen：阿里云生态，更稳定

### Q5：API密钥会过期吗？
**不会自动过期**，但：
- 长期不用可能被回收（通常不会）
- 账户欠费会停止服务
- 可以手动删除和重新创建

### Q6：如何查看剩余额度？
1. 登录DashScope控制台
2. 首页显示剩余tokens
3. 或进入"资源包管理"查看详细

### Q7：可以创建多个API密钥吗？
**可以！**
- 不同项目用不同密钥
- 方便管理和追踪使用量
- 泄露后只需删除单个密钥

### Q8：密钥泄露了怎么办？
1. 立即删除泄露的密钥
2. 创建新的密钥
3. 更新项目配置
4. 检查是否有异常使用

### Q9：为什么我的密钥无法使用？
**可能原因**：
- 账户余额不足
- 密钥复制时多了空格
- 服务未开通
- 网络问题

**解决方法**：
1. 检查DashScope控制台状态
2. 重新复制密钥（确保完整）
3. 查看应用错误日志

### Q10：如何升级到更好的模型？
修改 `.env` 文件：
```bash
# 从 turbo 升级到 plus
QWEN_MODEL=qwen-plus

# 或升级到 max
QWEN_MODEL=qwen-max
```
重启应用即可。

---

## 💡 使用建议

### 日常使用
推荐 `qwen-turbo`：
```bash
QWEN_MODEL=qwen-turbo
```
- 速度快
- 成本低
- 质量够用

### 代码分析
推荐 `qwen-coder-turbo`：
```bash
QWEN_MODEL=qwen-coder-turbo
```
- 专门优化代码理解
- 更适合架构分析

### 长文档
推荐 `qwen-long`：
```bash
QWEN_MODEL=qwen-long
```
- 支持100万tokens上下文
- 可以分析整篇论文

### 最高质量
推荐 `qwen-max`：
```bash
QWEN_MODEL=qwen-max
```
- 最强的推理能力
- 适合复杂学术分析

---

## 🔗 相关链接

### 官方资源
- **控制台首页**: https://dashscope.console.aliyun.com/
- **API Key管理**: https://dashscope.console.aliyun.com/apiKey
- **官方文档**: https://help.aliyun.com/zh/dashscope/
- **API参考**: https://help.aliyun.com/zh/dashscope/developer-reference/api-details
- **价格说明**: https://help.aliyun.com/zh/dashscope/developer-reference/tongyi-thousand-questions-metering-and-billing

### 社区资源
- **模型广场**: https://dashscope.console.aliyun.com/model
- **示例代码**: https://help.aliyun.com/zh/dashscope/developer-reference/quick-start
- **常见问题**: https://help.aliyun.com/zh/dashscope/support/faq

---

## 🎓 进阶技巧

### 1. 设置消费限额

为防止意外超支：
1. 进入阿里云费用中心
2. 设置账户余额预警
3. 设置每日消费上限

### 2. 批量处理优化

如果需要批量分析论文：
- 考虑购买资源包（更便宜）
- 使用 `qwen-turbo`（最快）
- 合理设置并发数

### 3. 错误重试策略

在代码中实现重试：
```python
# 系统已内置重试逻辑
# 429错误会自动重试
# 500错误会报告给用户
```

### 4. 多密钥轮换

创建多个API密钥，在不同时间使用：
- 避免单个密钥超限
- 更好的负载均衡

---

## 📸 界面示意

### DashScope控制台
```
┌─────────────────────────────────────┐
│ DashScope - 模型服务灵积              │
├─────────────────────────────────────┤
│ Dashboard                            │
│ > API-KEY管理        <-- 点击这里    │
│   用量统计                           │
│   资源包管理                         │
│   账单明细                           │
└─────────────────────────────────────┘
```

### API Key管理页面
```
┌─────────────────────────────────────┐
│ API-KEY 管理                         │
├─────────────────────────────────────┤
│ [+ 创建新的API-KEY]  <-- 点击这里   │
│                                      │
│ 我的API Keys:                        │
│                                      │
│ ┌─────────────────────────────────┐ │
│ │ 名称: paper-manager              │ │
│ │ Key: sk-xxx...xxx  [复制] [删除] │ │
│ │ 创建时间: 2024-01-01             │ │
│ │ 状态: 启用                       │ │
│ └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

---

## 🚨 故障排查

### 错误1：API key验证失败

**现象**：
```
401 Unauthorized: Invalid API key
```

**解决**：
1. 检查密钥是否完整（没有多余空格）
2. 检查密钥是否已失效
3. 重新创建密钥

### 错误2：余额不足

**现象**：
```
403 Forbidden: Insufficient balance
```

**解决**：
1. 登录DashScope控制台
2. 查看资源包余额
3. 充值或购买资源包

### 错误3：超出限额

**现象**：
```
429 Too Many Requests
```

**解决**：
1. 等待1分钟后重试
2. 升级到更高QPS的资源包
3. 创建多个密钥分散请求

### 错误4：模型不存在

**现象**：
```
Model 'xxx' not found
```

**解决**：
检查QWEN_MODEL配置是否正确：
```bash
# 正确的模型名称
qwen-turbo
qwen-plus
qwen-max
qwen-long

# 错误示例（不要这样写）
qwen-1.5
qwen-v2
tongyi-qwen
```

---

## 🎉 配置完成！

配置成功后，你可以：

1. ✅ 在"AI设置"中看到"通义千问"
2. ✅ 选择"通义千问"作为全局模型
3. ✅ 使用所有AI功能：
   - 论文摘要生成
   - 创新点提取
   - 代码架构分析
   - PDF翻译（未来）

4. ✅ 导航栏显示：**⚙️ AI设置 [通义千问]**

---

## 📞 需要帮助？

- **官方文档**: https://help.aliyun.com/zh/dashscope/
- **工单支持**: 阿里云控制台 → 工单
- **社区论坛**: https://developer.aliyun.com/ask/
- **客服电话**: 95187

---

## 🔄 更新日志

- 2026-02-28: 创建文档
- 支持的模型: qwen-turbo, qwen-plus, qwen-max, qwen-long, qwen-coder-turbo

---

**祝配置顺利！** 🎊

如果配置过程中遇到问题，欢迎查阅 [API_KEYS_GUIDE.md](../API_KEYS_GUIDE.md) 获取更多帮助。
