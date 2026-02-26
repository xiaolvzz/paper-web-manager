# 📝 GitHub账号注册指南（2分钟）

## 第一步：访问注册页面

打开浏览器，访问：**https://github.com/signup**

---

## 第二步：填写注册信息

### 1. 输入邮箱

```
Email: gxinghua711@163.com
```

点击 "Continue"

### 2. 设置密码

```
Password: 设置一个强密码（至少8位，包含字母和数字）
```

点击 "Continue"

### 3. 设置用户名

**重要！** 这就是您的GitHub用户名

建议填写：
```
Username: gxinghua711
```

或者其他您喜欢的用户名（只能包含字母、数字和连字符）

如果这个用户名被占用，GitHub会提示您，可以尝试：
- `gxinghua-711`
- `gxinghua2024`
- 或其他变体

点击 "Continue"

### 4. 邮件验证

GitHub会提示是否接收产品更新邮件：
- 输入 `n`（不接收）或 `y`（接收）

点击 "Continue"

### 5. 验证码

完成人机验证（点击图片或拼图）

点击 "Create account"

### 6. 邮箱验证

1. GitHub会发送验证码到您的邮箱 `gxinghua711@163.com`
2. 打开邮箱，查看GitHub发来的邮件
3. 复制邮件中的验证码
4. 粘贴到GitHub页面

---

## 第三步：完成设置

邮箱验证后，GitHub可能会问几个问题：

- **团队规模**：选择 "Just me"
- **用途**：选择 "Other"
- **功能**：可以全部跳过（Skip）

---

## 🎉 注册完成！

现在您的GitHub账号：
- **用户名**：`gxinghua711` （或您刚才设置的）
- **邮箱**：`gxinghua711@163.com`

---

## 第四步：获取Personal Access Token

注册完成后，我们需要获取一个Token用于推送代码：

### 1. 访问Token设置页面

**https://github.com/settings/tokens**

或者：
1. 点击右上角头像
2. Settings
3. 左侧菜单最下方 → Developer settings
4. Personal access tokens → Tokens (classic)

### 2. 生成新Token

1. 点击 **"Generate new token"** → **"Generate new token (classic)"**
2. 填写：
   - **Note**: `paper-web-manager`（备注名称）
   - **Expiration**: `90 days`（有效期90天）
   - **Select scopes**: 勾选 ✅ **`repo`**（所有repo权限）
3. 滚动到底部，点击 **"Generate token"**

### 3. 复制Token

⚠️ **重要**：生成后的Token只显示一次！

```
ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**立即复制并保存这个Token**（后面推送代码会用到）

---

## ✅ 准备就绪

现在告诉我：
1. 您的GitHub用户名（比如 `gxinghua711`）
2. 您已经复制了Personal Access Token

我会帮您推送代码！
