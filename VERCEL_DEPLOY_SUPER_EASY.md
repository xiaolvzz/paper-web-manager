# 🎯 Vercel部署 - 超简单版（5分钟，不需要思考）

## 第一步：打开Vercel

**操作**：点击这个链接 👉 https://vercel.com/signup

**选择**：点击黑色按钮 "Continue with GitHub"

**授权**：点击绿色按钮 "Authorize Vercel"

✅ 完成！自动跳转到Vercel控制台

---

## 第二步：导入项目

**操作**：点击 "Add New..." → 点击 "Project"

**找到仓库**：在列表中找到 `xiaolvzz/paper-web-manager`

**如果看不到**：
- 点击 "Adjust GitHub App Permissions"
- 选择 "All repositories"
- 点击 "Save"
- 返回上一页，刷新

**导入**：找到后，点击右边的 "Import" 按钮

✅ 完成！进入配置页面

---

## 第三步：配置（关键步骤）

### 3.1 Framework设置

**找到**："Framework Preset" 下拉框

**选择**：点击选择 "Other"

### 3.2 向下滚动

**操作**：用鼠标滚轮向下滚动页面

**找到**："Environment Variables" 部分（有个锁的图标🔒）

**点击**：展开这个部分

### 3.3 添加第一个变量

**在三个输入框中依次填写**：

| 框 | 填写内容 |
|----|---------|
| 第1个框 (Name) | `SUPABASE_URL` |
| 第2个框 (Value) | `https://wlslekyepjebnzjmslld.supabase.co` |
| 第3个框 (Environment) | 保持默认（三个都勾选）|

**点击**：右边的 "Add" 按钮

### 3.4 添加第二个变量

**在三个输入框中依次填写**：

| 框 | 填写内容 |
|----|---------|
| 第1个框 (Name) | `SUPABASE_KEY` |
| 第2个框 (Value) | 复制下面这整段 👇 |

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Indsc2xla3llcGplYm56am1zbGxkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzIwNjIwNTksImV4cCI6MjA4NzYzODA1OX0.Yuq7u2woJAdrnh2RLs06Vi8IObe52FaHMsRqHTRQ14M
```

**点击**：右边的 "Add" 按钮

**验证**：应该能看到两个变量已添加：
- ✅ SUPABASE_URL
- ✅ SUPABASE_KEY

✅ 完成！环境变量配置成功

---

## 第四步：部署

**操作**：点击底部大大的蓝色按钮 "Deploy"

**等待**：1-2分钟（会看到进度条和日志）

**成功标志**：
- 看到 🎉 图标
- 出现 "Congratulations!" 文字
- 显示一个网址

✅ 完成！部署成功！

---

## 第五步：访问网站

**操作**：点击显示的网址（类似 `https://paper-web-manager-xxxxx.vercel.app`）

**或者**：点击 "Visit" 按钮

**看到**：论文管理系统的首页！

✅ 大功告成！🎉

---

## 📸 关键步骤总结

```
1. 访问 vercel.com/signup → Continue with GitHub
2. Add New → Project → Import paper-web-manager
3. Framework: Other
4. Environment Variables:
   - SUPABASE_URL = https://wlslekyepjebnzjmslld.supabase.co
   - SUPABASE_KEY = eyJhbGci...（那一长串）
5. 点击 Deploy
6. 等待 → 完成 → 访问网站
```

---

## ⏱️ 时间预估

- 步骤1：1分钟（登录）
- 步骤2：1分钟（导入）
- 步骤3：2分钟（配置环境变量）
- 步骤4：1-2分钟（自动部署）
- 步骤5：10秒（访问）

**总计：约5分钟**

---

## 💡 温馨提示

1. **两个环境变量都要添加**，缺一不可
2. **Value要完整复制**，不要有空格
3. **SUPABASE_KEY很长**，要完整复制整段
4. 部署过程会显示很多日志，这是正常的
5. 如果失败，查看日志底部的错误信息

---

## 🆘 常见问题

**Q: 找不到仓库？**
A: 点击 "Adjust GitHub App Permissions" → 选择 "All repositories"

**Q: 部署失败？**
A: 检查两个环境变量是否都添加成功，Value是否完整

**Q: 网站打不开？**
A: 等1分钟再试，Vercel需要时间完全部署

---

## ✅ 完成后

访问您的网站，测试添加第一篇论文！

网站地址会是：`https://paper-web-manager-xxxxx.vercel.app`

保存这个地址，以后随时访问！

---

**现在开始吧！只需要5分钟！** 🚀
