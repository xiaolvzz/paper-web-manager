-- 增强标签和关系系统

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
-- 不使用CHECK约束，允许更灵活的关系类型

COMMENT ON TABLE domains IS '领域标签表，支持预设和自定义领域';
COMMENT ON TABLE paper_domains IS '论文-领域多对多关联表';
COMMENT ON COLUMN paper_domains.confidence IS '置信度，AI自动标注时使用';

-- 4. 添加更多关系类型的示例数据（可选）
-- relations表的relation_type字段现在支持：
-- - method_similar: 方法相似
-- - problem_related: 问题相关
-- - derived_from: 衍生自（A基于B改进）
-- - extends: 扩展（A扩展了B的工作）
-- - compares_with: 对比研究
-- - same_domain: 同领域
-- - baseline: 基线方法
-- - custom: 自定义

-- 5. 迁移现有的tags到新的领域系统（可选）
-- 这个脚本可以分析papers表的tags字段，自动创建对应的领域关联
-- 实际使用时需要根据具体情况调整
