-- Migration: 添加github_url和domain字段到papers表
-- Date: 2026-02-27
-- Description: 为论文管理系统添加GitHub链接和研究领域字段

-- 添加github_url列
ALTER TABLE papers ADD COLUMN IF NOT EXISTS github_url TEXT;

-- 添加domain列
ALTER TABLE papers ADD COLUMN IF NOT EXISTS domain TEXT;

-- 添加列注释
COMMENT ON COLUMN papers.github_url IS 'GitHub repository URL for the paper code';
COMMENT ON COLUMN papers.domain IS 'Research domain (e.g., NLP, CV, RL, ML, Robotics, etc.)';

-- 创建索引以提升按领域查询的性能
CREATE INDEX IF NOT EXISTS idx_papers_domain ON papers(domain);

-- 验证更改
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'papers'
AND column_name IN ('github_url', 'domain');
