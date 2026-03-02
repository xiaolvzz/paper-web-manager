# 🔐 认证系统设置指南

## 快速开始

### 1. 执行数据库迁移

在 Supabase SQL Editor 中执行：

```sql
-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    last_login TIMESTAMPTZ,
    is_active BOOLEAN DEFAULT TRUE
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);

-- 插入默认管理员账户（密码: admin123）
INSERT INTO users (username, password_hash, is_active)
VALUES (
    'admin',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLhJ5MbS',
    true
)
ON CONFLICT (username) DO NOTHING;
```

### 2. 配置环境变量（可选）

在 `.env` 文件或 Vercel 环境变量中添加：

```bash
# JWT 密钥（生产环境必须修改！）
JWT_SECRET_KEY=your-super-secret-key-change-this-in-production-123456
```

**重要**：生产环境请使用强随机密钥，可以用以下命令生成：
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 重启应用

```bash
python -m uvicorn backend.main:app --reload
```

---

## 默认账户信息

### 管理员账户
- **用户名**: `admin`
- **密码**: `admin123`

⚠️ **重要**：首次登录后请立即修改密码！

---

## 使用说明

### 登录

1. 访问 `http://localhost:8000/login`
2. 输入用户名和密码
3. 点击"登录"按钮
4. 登录成功后自动跳转到首页

### 修改密码

1. 登录后，点击右上角用户名
2. 选择"🔒 修改密码"
3. 输入旧密码和新密码
4. 点击"确认修改"

### 登出

1. 点击右上角用户名
2. 选择"🚪 登出"

---

## 安全特性

✅ **密码加密**：使用 bcrypt 哈希加密存储密码
✅ **JWT 认证**：基于 JSON Web Token 的无状态认证
✅ **Token 过期**：Token 有效期 7 天，过期自动登出
✅ **页面保护**：所有页面需要登录才能访问
✅ **API 保护**：所有 API 需要有效 Token 才能调用

---

## 添加新用户

### 方法1：通过数据库添加

在 Supabase SQL Editor 中执行：

```sql
-- 生成密码哈希（使用 Python）
-- python -c "import bcrypt; print(bcrypt.hashpw(b'your_password', bcrypt.gensalt()).decode())"

INSERT INTO users (username, password_hash, is_active)
VALUES (
    'new_username',
    '$2b$12$...your_hashed_password...',
    true
);
```

### 方法2：使用 Python 脚本

创建 `add_user.py`:

```python
import bcrypt
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

username = input("用户名: ")
password = input("密码: ")

# 加密密码
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# 插入数据库
supabase.table("users").insert({
    "username": username,
    "password_hash": hashed.decode(),
    "is_active": True
}).execute()

print(f"用户 {username} 创建成功！")
```

运行：
```bash
python add_user.py
```

---

## 禁用/启用用户

```sql
-- 禁用用户
UPDATE users SET is_active = false WHERE username = 'username';

-- 启用用户
UPDATE users SET is_active = true WHERE username = 'username';
```

---

## 重置密码

如果忘记密码，可以通过数据库重置：

```sql
-- 重置为 admin123
UPDATE users
SET password_hash = '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLhJ5MbS'
WHERE username = 'admin';
```

或者生成新密码：

```bash
# 使用 Python 生成新密码哈希
python -c "import bcrypt; print(bcrypt.hashpw(b'new_password', bcrypt.gensalt()).decode())"
```

然后更新到数据库：

```sql
UPDATE users
SET password_hash = '生成的哈希值'
WHERE username = 'username';
```

---

## 常见问题

### Q1: 登录后被重定向回登录页？
**A**: 检查浏览器控制台，可能是 Token 验证失败。确保后端正常运行且数据库连接正常。

### Q2: 修改密码失败？
**A**: 确认旧密码输入正确，新密码至少 6 个字符。

### Q3: 如何完全禁用认证？
**A**: 不建议禁用认证。如果确实需要，可以在 `auth.js` 中注释掉 `protectPage()` 函数调用。

### Q4: Token 过期时间可以修改吗？
**A**: 可以。在 `backend/auth.py` 中修改 `ACCESS_TOKEN_EXPIRE_HOURS` 变量。

### Q5: 支持多用户吗？
**A**: 支持！按照"添加新用户"部分的说明添加即可。

---

## 部署到 Vercel

1. **设置环境变量**
   - 在 Vercel 项目设置中添加：
     ```
     JWT_SECRET_KEY=your-random-secret-key
     ```

2. **推送代码**
   ```bash
   git push origin main
   ```

3. **执行数据库迁移**
   - 在 Supabase 执行 `migrations/007_add_users_table.sql`

4. **访问网站**
   - 首次访问会跳转到登录页
   - 使用默认账户登录
   - 立即修改密码！

---

## 安全建议

1. ✅ **立即修改默认密码**
2. ✅ **使用强随机 JWT 密钥**
3. ✅ **定期更新依赖包**
4. ✅ **不要在代码中硬编码密码**
5. ✅ **启用 HTTPS（Vercel 自动提供）**
6. ✅ **定期检查用户登录记录**

---

## 技术栈

- **后端认证**: FastAPI + JWT
- **密码加密**: bcrypt
- **Token 存储**: localStorage (前端)
- **认证方式**: Bearer Token
- **Token 有效期**: 7 天

---

## 需要帮助？

如果遇到问题：
1. 查看浏览器控制台错误信息
2. 查看后端日志
3. 确认数据库迁移已执行
4. 确认环境变量已配置

祝你使用愉快！🎉
