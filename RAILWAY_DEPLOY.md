# 🚂 Railway部署指南（Vercel替代方案）

Railway是另一个优秀的免费云托管平台，注册简单，功能强大！

## 免费额度

- ✅ $5/月免费额度（足够个人使用）
- ✅ 512MB内存
- ✅ 自动HTTPS
- ✅ 全球CDN

---

## 第一步：注册Railway（1分钟）

**1. 访问** https://railway.app/

**2. 点击** "Login" → "Login with GitHub"

**3. 授权**：点击 "Authorize Railway"

✅ 完成！直接进入控制台（比Vercel简单）

---

## 第二步：创建项目（2分钟）

**1.** 点击 "New Project"

**2.** 选择 "Deploy from GitHub repo"

**3.** 找到并点击 `xiaolvzz/paper-web-manager`

**4.** 点击 "Deploy Now"

✅ Railway会自动开始部署

---

## 第三步：添加环境变量（2分钟）

部署开始后：

**1.** 点击刚创建的项目（会看到部署日志）

**2.** 点击 "Variables" 标签页

**3.** 点击 "New Variable"

**添加第一个变量：**
```
SUPABASE_URL = https://wlslekyepjebnzjmslld.supabase.co
```

**4.** 再次点击 "New Variable"

**添加第二个变量：**
```
SUPABASE_KEY = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Indsc2xla3llcGplYm56am1zbGxkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzIwNjIwNTksImV4cCI6MjA4NzYzODA1OX0.Yuq7u2woJAdrnh2RLs06Vi8IObe52FaHMsRqHTRQ14M
```

✅ 环境变量添加成功，Railway会自动重新部署

---

## 第四步：获取网站地址（1分钟）

**1.** 点击 "Settings" 标签页

**2.** 找到 "Domains" 部分

**3.** 点击 "Generate Domain"

**4.** Railway会生成一个域名，类似：
```
paper-web-manager-production.up.railway.app
```

✅ 点击这个域名，访问您的网站！

---

## 🎉 部署完成！

现在您的论文管理系统已经上线！

**您的网站**：`https://xxxxx.up.railway.app`

---

## 📊 Railway vs Vercel

| 特性 | Railway | Vercel |
|------|---------|--------|
| **注册难度** | ⭐⭐⭐⭐⭐ 超简单 | ⭐⭐⭐ 可能需要审核 |
| **免费额度** | $5/月 | 100GB带宽/月 |
| **部署速度** | 快 | 快 |
| **自定义域名** | 支持 | 支持 |

**结论**：两个都很好，Railway更容易注册！

---

## 💡 小贴士

1. Railway每月自动赠送$5额度
2. 个人使用不会超出免费额度
3. 如果Vercel审核通过，可以同时使用两个平台

---

## 🆘 常见问题

**Q: Railway需要付款信息吗？**
A: 可以不提供，直接使用免费额度

**Q: 会扣费吗？**
A: 不会，$5/月的免费额度足够使用

**Q: 比Vercel慢吗？**
A: 不会，速度差不多

---

开始部署吧！比Vercel更简单！🚀
