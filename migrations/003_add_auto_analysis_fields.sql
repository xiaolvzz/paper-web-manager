-- 添加自动分析相关字段
-- 在Supabase SQL编辑器中执行此脚本

-- 1. 扩展papers表：添加结构化信息字段
ALTER TABLE papers ADD COLUMN IF NOT EXISTS source_code_url TEXT;
ALTER TABLE papers ADD COLUMN IF NOT EXISTS main_work TEXT;
ALTER TABLE papers ADD COLUMN IF NOT EXISTS innovations JSONB DEFAULT '[]'::jsonb;
ALTER TABLE papers ADD COLUMN IF NOT EXISTS structured_tags JSONB DEFAULT '[]'::jsonb;
ALTER TABLE papers ADD COLUMN IF NOT EXISTS auto_analyzed BOOLEAN DEFAULT FALSE;
ALTER TABLE papers ADD COLUMN IF NOT EXISTS auto_analysis_date TIMESTAMPTZ;

-- 2. 创建索引
CREATE INDEX IF NOT EXISTS idx_papers_source_code ON papers(source_code_url) WHERE source_code_url IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_papers_auto_analyzed ON papers(auto_analyzed);

-- 3. 添加注释
COMMENT ON COLUMN papers.source_code_url IS '源码链接（GitHub等）';
COMMENT ON COLUMN papers.main_work IS '主要工作描述';
COMMENT ON COLUMN papers.innovations IS '创新点列表（JSON数组）';
COMMENT ON COLUMN papers.structured_tags IS '结构化标签（JSON数组）';
COMMENT ON COLUMN papers.auto_analyzed IS '是否已自动分析';
COMMENT ON COLUMN papers.auto_analysis_date IS '自动分析时间';

-- 4. 数据迁移：将现有tags转换为structured_tags
UPDATE papers
SET structured_tags = (
    SELECT jsonb_agg(trim(tag))
    FROM unnest(string_to_array(tags, ',')) AS tag
    WHERE tags IS NOT NULL AND tags != ''
)
WHERE tags IS NOT NULL AND tags != '' AND structured_tags = '[]'::jsonb;

-- 5. 验证
SELECT
    id,
    title,
    source_code_url,
    main_work,
    innovations,
    structured_tags,
    auto_analyzed
FROM papers
LIMIT 5;
