-- ============================================
-- 合并迁移脚本：004 + 005
-- 请在Supabase SQL编辑器中执行此脚本
-- ============================================

-- ===== Migration 004: 领域标签和关系系统 =====

-- 1. 创建领域标签表（预设+自定义）
CREATE TABLE IF NOT EXISTS domains (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    color TEXT NOT NULL DEFAULT '#6366f1',  -- 显示颜色
    icon TEXT DEFAULT '🏷️',  -- 图标emoji
    description TEXT,
    is_predefined BOOLEAN DEFAULT FALSE,  -- 是否为预设领域
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 插入预设领域
INSERT INTO domains (name, color, icon, description, is_predefined) VALUES
('VLA (视觉-语言-动作)', '#8b5cf6', '🤖', 'Vision-Language-Action模型', true),
('强化学习', '#10b981', '🎮', 'Reinforcement Learning', true),
('计算机视觉', '#3b82f6', '👁️', 'Computer Vision', true),
('自然语言处理', '#f59e0b', '💬', 'Natural Language Processing', true),
('自动驾驶', '#ef4444', '🚗', 'Autonomous Driving', true),
('具身智能', '#ec4899', '🦾', 'Embodied AI', true),
('世界模型', '#06b6d4', '🌍', 'World Models', true),
('Transformer', '#6366f1', '⚡', 'Transformer架构', true),
('扩散模型', '#a855f7', '🌊', 'Diffusion Models', true),
('多模态', '#f97316', '🎨', 'Multi-modal Learning', true)
ON CONFLICT (name) DO NOTHING;

-- 2. 创建论文-领域关联表（多对多）
CREATE TABLE IF NOT EXISTS paper_domains (
    id BIGSERIAL PRIMARY KEY,
    paper_id BIGINT NOT NULL REFERENCES papers(id) ON DELETE CASCADE,
    domain_id BIGINT NOT NULL REFERENCES domains(id) ON DELETE CASCADE,
    confidence FLOAT DEFAULT 1.0,  -- 相关度置信度 (0-1)，用于AI自动标注
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(paper_id, domain_id)
);

CREATE INDEX IF NOT EXISTS idx_paper_domains_paper ON paper_domains(paper_id);
CREATE INDEX IF NOT EXISTS idx_paper_domains_domain ON paper_domains(domain_id);

-- 3. 扩展关系类型
ALTER TABLE relations DROP CONSTRAINT IF EXISTS relations_relation_type_check;

COMMENT ON TABLE domains IS '领域标签表，支持预设和自定义领域';
COMMENT ON TABLE paper_domains IS '论文-领域多对多关联表';
COMMENT ON COLUMN paper_domains.confidence IS '置信度，AI自动标注时使用';

-- ===== Migration 005: 代码分析结果存储 =====

-- 扩展papers表，添加代码分析相关字段
ALTER TABLE papers ADD COLUMN IF NOT EXISTS code_analysis_result TEXT;
ALTER TABLE papers ADD COLUMN IF NOT EXISTS code_analysis_date TIMESTAMPTZ;
ALTER TABLE papers ADD COLUMN IF NOT EXISTS code_analysis_model TEXT;  -- 记录使用的AI模型

COMMENT ON COLUMN papers.code_analysis_result IS 'AI代码架构分析结果（Markdown格式）';
COMMENT ON COLUMN papers.code_analysis_date IS '代码分析时间';
COMMENT ON COLUMN papers.code_analysis_model IS '使用的AI模型（如：Claude Haiku, Gemini 2.0）';

-- 可选：如果想更详细地记录，也可以扩展analysis表
ALTER TABLE analysis ADD COLUMN IF NOT EXISTS code_structure TEXT;  -- 代码结构说明
ALTER TABLE analysis ADD COLUMN IF NOT EXISTS usage_guide TEXT;     -- 代码使用指南

COMMENT ON COLUMN analysis.code_structure IS '代码结构和架构说明';
COMMENT ON COLUMN analysis.usage_guide IS '代码使用、安装、运行指南';

-- ============================================
-- 执行完成后，刷新应用页面即可看到效果
-- ============================================
