-- 对话记录表和论文表扩展
-- 在Supabase SQL编辑器中执行此脚本

-- 1. 创建对话记录表
CREATE TABLE IF NOT EXISTS conversations (
    id BIGSERIAL PRIMARY KEY,
    paper_id BIGINT NOT NULL REFERENCES papers(id) ON DELETE CASCADE,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. 扩展papers表以支持PDF处理
ALTER TABLE papers ADD COLUMN IF NOT EXISTS pdf_storage_path TEXT;
ALTER TABLE papers ADD COLUMN IF NOT EXISTS pdf_text_content TEXT;
ALTER TABLE papers ADD COLUMN IF NOT EXISTS arxiv_id TEXT;

-- 3. 创建索引优化查询
CREATE INDEX IF NOT EXISTS idx_conversations_paper_id_time ON conversations(paper_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_papers_arxiv_id ON papers(arxiv_id);

-- 4. 添加注释
COMMENT ON TABLE conversations IS 'AI对话记录表，按论文归档';
COMMENT ON COLUMN conversations.role IS '消息角色：user-用户，assistant-AI，system-系统';
COMMENT ON COLUMN papers.pdf_storage_path IS 'Supabase Storage中的PDF文件路径';
COMMENT ON COLUMN papers.pdf_text_content IS '提取的PDF文本内容，供AI分析使用';
COMMENT ON COLUMN papers.arxiv_id IS 'arXiv论文ID（如2301.12345）';

-- 5. 验证表结构
SELECT
    table_name,
    column_name,
    data_type
FROM information_schema.columns
WHERE table_name IN ('conversations', 'papers')
ORDER BY table_name, ordinal_position;
