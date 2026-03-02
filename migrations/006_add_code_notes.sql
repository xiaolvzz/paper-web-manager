-- 创建代码笔记表（分段式笔记）
CREATE TABLE IF NOT EXISTS code_notes (
    id BIGSERIAL PRIMARY KEY,
    paper_id BIGINT NOT NULL REFERENCES papers(id) ON DELETE CASCADE,
    note_type TEXT NOT NULL DEFAULT 'code' CHECK (note_type IN ('code', 'discussion')),

    -- 笔记内容
    title TEXT NOT NULL,  -- 文件名或主题
    content TEXT,  -- 理解和备注

    -- 图片存储（Supabase Storage路径数组）
    images TEXT[] DEFAULT '{}',

    -- 排序和时间
    order_index INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_code_notes_paper_id ON code_notes(paper_id);
CREATE INDEX IF NOT EXISTS idx_code_notes_type ON code_notes(note_type);
CREATE INDEX IF NOT EXISTS idx_code_notes_order ON code_notes(paper_id, order_index DESC, created_at DESC);

-- 注释
COMMENT ON TABLE code_notes IS '代码阅读笔记表，支持分段式笔记和截图';
COMMENT ON COLUMN code_notes.note_type IS '笔记类型：code=源码笔记, discussion=论文讨论';
COMMENT ON COLUMN code_notes.title IS '文件名或主题标题';
COMMENT ON COLUMN code_notes.content IS '笔记内容';
COMMENT ON COLUMN code_notes.images IS '截图路径数组（Supabase Storage）';
COMMENT ON COLUMN code_notes.order_index IS '排序索引，数字越大越靠前';

-- 自动更新updated_at的触发器
CREATE OR REPLACE FUNCTION update_code_notes_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER code_notes_updated_at
    BEFORE UPDATE ON code_notes
    FOR EACH ROW
    EXECUTE FUNCTION update_code_notes_updated_at();
