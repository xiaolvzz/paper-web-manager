# 🎨 Render部署指南（完全免费，无需信用卡）

Render是一个优秀的免费托管平台，**无需绑定信用卡**！

## ✨ 免费额度

- ✅ 完全免费（无需信用卡）
- ✅ 750小时/月（个人使用足够）
- ✅ 自动HTTPS
- ✅ 全球CDN
- ⚠️ 15分钟无访问会休眠（首次访问需等待30秒唤醒）

**非常适合个人项目！**

---

## 第一步：注册Render（1分钟）

**1. 访问** https://render.com/

**2. 点击** "Get Started for Free"

**3. 选择** "Sign in with GitHub"

**4. 授权**：点击 "Authorize Render"

✅ 完成！无需绑定信用卡

---

## 第二步：创建Web Service（2分钟）

**1.** 点击 "New +" → "Web Service"

**2.** 选择 "Build and deploy from a Git repository"

**3.** 点击 "Connect account" 连接GitHub

**4.** 找到并选择 `xiaolvzz/paper-web-manager`

**5.** 点击 "Connect"

---

## 第三步：配置项目（3分钟）

在配置页面填写：

| 字段 | 填写内容 |
|------|---------|
| **Name** | `paper-web-manager`（或其他名称） |
| **Region** | 选择 `Singapore` |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn backend.main:app --host 0.0.0.0 --port $PORT` |

**Instance Type**: 选择 **"Free"**（免费）

---

## 第四步：添加环境变量（2分钟）

向下滚动到 "Environment Variables" 部分

**点击 "Add Environment Variable"**

**添加第一个变量：**
```
Key: SUPABASE_URL
Value: https://wlslekyepjebnzjmslld.supabase.co
```

**再次点击 "Add Environment Variable"**

**添加第二个变量：**
```
Key: SUPABASE_KEY
Value: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Indsc2xla3llcGplYm56am1zbGxkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzIwNjIwNTksImV4cCI6MjA4NzYzODA1OX0.Yuq7u2woJAdrnh2RLs06Vi8IObe52FaHMsRqHTRQ14M
```

---

## 第五步：部署（自动）

**点击** "Create Web Service"

Render会自动：
1. 克隆仓库
2. 安装依赖
3. 启动服务

**等待时间**：3-5分钟（首次部署）

**成功标志**：看到 "Live" 绿色标签

---

## 第六步：访问网站

部署成功后，Render会提供一个域名：

```
https://paper-web-manager-xxxx.onrender.com
```

**点击访问**，您的论文管理系统上线了！

---

## ⚠️ 重要提示：休眠机制

**免费版特性**：
- 15分钟无访问会自动休眠
- 休眠后首次访问需要30秒唤醒
- 唤醒后正常使用

**解决方案**：
- 经常使用就不会休眠
- 或设置定时任务每10分钟访问一次（可选）

---

## 📊 Render vs Vercel vs Railway

| 特性 | Render | Vercel | Railway |
|------|--------|--------|---------|
| **免费使用** | ✅ | ✅ | ✅ |
| **需要信用卡** | ❌ 不需要 | ❌ 不需要 | ✅ 需要 |
| **注册难度** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ 可能审核 | ⭐⭐⭐⭐ |
| **休眠机制** | ✅ 15分钟 | ❌ 不休眠 | ❌ 不休眠 |
| **适合人群** | 个人项目 | 专业项目 | 需要绑卡 |

**结论**：
- **Render最适合不想绑卡的用户**
- Vercel最好，但需要等审核
- Railway需要绑信用卡

---

## 💡 小贴士

1. **首次访问慢？** 这是正常的，服务正在唤醒（30秒）
2. **经常使用？** 就不会休眠了
3. **想保持活跃？** 可以用UptimeRobot监控（免费服务）

---

## 🎉 完全免费方案

```
Render (免费) + Supabase (免费) = ¥0/月
```

无需绑定任何支付方式！

---

开始部署吧！比Railway更适合个人使用！🚀
