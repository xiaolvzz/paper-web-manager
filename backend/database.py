"""数据库连接和初始化"""
import os
from typing import Optional, Dict, Any
from supabase import create_client, Client

# 加载环境变量（仅在本地开发环境）
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Vercel环境中不需要dotenv
    pass


class Database:
    """数据库管理类"""

    def __init__(self):
        self.url: str = os.getenv("SUPABASE_URL", "")
        self.key: str = os.getenv("SUPABASE_KEY", "")
        self.client: Optional[Client] = None

        if self.url and self.key:
            self.client = create_client(self.url, self.key)

    def get_client(self) -> Client:
        """获取Supabase客户端"""
        if not self.client:
            raise Exception("数据库未初始化，请检查环境变量 SUPABASE_URL 和 SUPABASE_KEY")
        return self.client

    async def init_tables(self):
        """初始化数据库表（如果不存在）"""
        # 注意：在Supabase中，通常通过Web控制台或SQL编辑器创建表
        # 这里提供SQL语句供参考
        pass


# 全局数据库实例
db = Database()


def get_db() -> Client:
    """依赖注入：获取数据库客户端"""
    return db.get_client()


def get_supabase_client() -> Client:
    """获取Supabase客户端（非依赖注入版本）"""
    return db.get_client()


# 数据库表创建SQL（在Supabase SQL编辑器中执行）
SQL_SCHEMA = """
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

CREATE TRIGGER update_papers_updated_at
    BEFORE UPDATE ON papers
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
"""
