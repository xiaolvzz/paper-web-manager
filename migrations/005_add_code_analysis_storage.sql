-- 添加代码分析结果存储字段

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
