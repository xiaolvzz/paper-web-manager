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

-- 注释
COMMENT ON TABLE users IS '用户表，用于认证和授权';
COMMENT ON COLUMN users.username IS '用户名（唯一）';
COMMENT ON COLUMN users.password_hash IS '密码哈希值（使用bcrypt加密）';
COMMENT ON COLUMN users.is_active IS '账户是否激活';

-- 插入默认管理员账户（密码: admin123）
-- 注意：首次登录后请立即修改密码！
INSERT INTO users (username, password_hash, is_active)
VALUES (
    'admin',
    '$2b$12$MrLR5OqNH9intbkOOebiZOPPH0kreoraUlU24enojLqtAH2ZDZ7/W',
    true
)
ON CONFLICT (username) DO UPDATE SET password_hash = EXCLUDED.password_hash;

-- 验证
SELECT 'User created:' as info, username, is_active, created_at
FROM users
WHERE username = 'admin';
