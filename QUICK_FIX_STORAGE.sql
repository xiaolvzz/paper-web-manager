-- ==========================================
-- Supabase Storage 快速修复
-- 在 Supabase SQL Editor 中执行
-- ==========================================

-- 1. 创建存储桶（如果不存在）
INSERT INTO storage.buckets (id, name, public, file_size_limit)
VALUES ('paper-pdfs', 'paper-pdfs', true, 52428800)
ON CONFLICT (id) DO UPDATE
SET public = true, file_size_limit = 52428800;

-- 验证存储桶已创建
SELECT 'Bucket configured:' as info, id, name, public, file_size_limit
FROM storage.buckets
WHERE name = 'paper-pdfs';
