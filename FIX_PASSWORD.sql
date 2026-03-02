-- 🔧 快速修复：更新admin账户密码
-- 问题：原密码哈希值错误，导致无法登录
-- 解决：更新为正确的密码哈希值

-- 更新密码哈希（密码仍然是 admin123）
UPDATE users
SET password_hash = '$2b$12$MrLR5OqNH9intbkOOebiZOPPH0kreoraUlU24enojLqtAH2ZDZ7/W'
WHERE username = 'admin';

-- 验证更新结果
SELECT
    username,
    is_active,
    created_at,
    CASE
        WHEN password_hash = '$2b$12$MrLR5OqNH9intbkOOebiZOPPH0kreoraUlU24enojLqtAH2ZDZ7/W'
        THEN '✅ 密码哈希已更新'
        ELSE '❌ 密码哈希未更新'
    END as status
FROM users
WHERE username = 'admin';
