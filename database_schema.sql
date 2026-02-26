-- 论文管理系统数据库Schema
-- 在Supabase SQL编辑器中执行此脚本

-- 论文表
CREATE TABLE IF NOT EXISTS papers (
    id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    authors TEXT,
    year INTEGER,
    pdf_path TEXT,
    abstract TEXT,
    tags TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 分析记录表
CREATE TABLE IF NOT EXISTS analysis (
    id BIGSERIAL PRIMARY KEY,
    paper_id BIGINT NOT NULL REFERENCES papers(id) ON DELETE CASCADE,
    innovation_points TEXT,
    framework_image TEXT,
    personal_notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(paper_id)
);

-- 关联关系表
CREATE TABLE IF NOT EXISTS relations (
    id BIGSERIAL PRIMARY KEY,
    paper_from_id BIGINT NOT NULL REFERENCES papers(id) ON DELETE CASCADE,
    paper_to_id BIGINT NOT NULL REFERENCES papers(id) ON DELETE CASCADE,
    relation_type TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    CHECK (paper_from_id != paper_to_id),
    UNIQUE(paper_from_id, paper_to_id, relation_type)
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_papers_title ON papers(title);
CREATE INDEX IF NOT EXISTS idx_papers_year ON papers(year);
CREATE INDEX IF NOT EXISTS idx_papers_created_at ON papers(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_analysis_paper_id ON analysis(paper_id);
CREATE INDEX IF NOT EXISTS idx_relations_from ON relations(paper_from_id);
CREATE INDEX IF NOT EXISTS idx_relations_to ON relations(paper_to_id);

-- 自动更新updated_at的触发器
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS update_papers_updated_at ON papers;
CREATE TRIGGER update_papers_updated_at
    BEFORE UPDATE ON papers
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- 插入示例数据（可选）
INSERT INTO papers (title, authors, year, abstract, tags) VALUES
(
    'Attention Is All You Need',
    'Ashish Vaswani, Noam Shazeer, Niki Parmar',
    2017,
    'The dominant sequence transduction models are based on complex recurrent or convolutional neural networks...',
    'Transformer, NLP, Deep Learning'
),
(
    'BERT: Pre-training of Deep Bidirectional Transformers',
    'Jacob Devlin, Ming-Wei Chang, Kenton Lee',
    2018,
    'We introduce a new language representation model called BERT...',
    'BERT, NLP, Pre-training'
);

COMMENT ON TABLE papers IS '论文表';
COMMENT ON TABLE analysis IS '分析记录表';
COMMENT ON TABLE relations IS '论文关联关系表';
