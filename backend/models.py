"""数据模型定义"""
from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, Field


class PaperBase(BaseModel):
    """论文基础模型"""
    title: str = Field(..., description="论文标题")
    authors: Optional[str] = Field(None, description="作者，逗号分隔")
    year: Optional[int] = Field(None, description="发表年份")
    pdf_path: Optional[str] = Field(None, description="PDF路径（本地或云盘链接）")
    abstract: Optional[str] = Field(None, description="摘要")
    tags: Optional[str] = Field(None, description="标签，逗号分隔（兼容旧数据）")
    github_url: Optional[str] = Field(None, description="GitHub代码仓库链接（兼容字段）")
    domain: Optional[str] = Field(None, description="研究领域（如NLP、CV、RL等）")
    pdf_storage_path: Optional[str] = Field(None, description="Supabase Storage中的PDF文件路径")
    pdf_text_content: Optional[str] = Field(None, description="提取的PDF文本内容")
    arxiv_id: Optional[str] = Field(None, description="arXiv论文ID（如2301.12345）")
    # 新增字段
    source_code_url: Optional[str] = Field(None, description="源码链接")
    main_work: Optional[str] = Field(None, description="主要工作描述")
    innovations: Optional[Any] = Field(None, description="创新点列表（JSONB）")
    structured_tags: Optional[Any] = Field(None, description="结构化标签列表（JSONB）")
    auto_analyzed: Optional[bool] = Field(None, description="是否已自动分析")
    auto_analysis_date: Optional[datetime] = Field(None, description="自动分析时间")


class PaperCreate(PaperBase):
    """创建论文的请求模型"""
    pass


class PaperUpdate(BaseModel):
    """更新论文的请求模型（所有字段可选）"""
    title: Optional[str] = None
    authors: Optional[str] = None
    year: Optional[int] = None
    pdf_path: Optional[str] = None
    abstract: Optional[str] = None
    tags: Optional[str] = None
    github_url: Optional[str] = None
    domain: Optional[str] = None
    pdf_storage_path: Optional[str] = None
    pdf_text_content: Optional[str] = None
    arxiv_id: Optional[str] = None
    # 新增字段
    source_code_url: Optional[str] = None
    main_work: Optional[str] = None
    innovations: Optional[Any] = None
    structured_tags: Optional[Any] = None
    auto_analyzed: Optional[bool] = None
    auto_analysis_date: Optional[datetime] = None


class Paper(PaperBase):
    """论文完整模型（包含数据库字段）"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AnalysisBase(BaseModel):
    """分析记录基础模型"""
    paper_id: int = Field(..., description="关联的论文ID")
    innovation_points: Optional[str] = Field(None, description="创新点分析（富文本）")
    framework_image: Optional[str] = Field(None, description="框架图URL")
    personal_notes: Optional[str] = Field(None, description="个人备注")


class AnalysisCreate(AnalysisBase):
    """创建分析记录的请求模型"""
    pass


class AnalysisUpdate(BaseModel):
    """更新分析记录的请求模型"""
    innovation_points: Optional[str] = None
    framework_image: Optional[str] = None
    personal_notes: Optional[str] = None


class Analysis(AnalysisBase):
    """分析记录完整模型"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class RelationType(str):
    """关联关系类型"""
    METHOD_SIMILAR = "method_similar"
    PROBLEM_RELATED = "problem_related"
    CUSTOM = "custom"


class RelationBase(BaseModel):
    """关联关系基础模型"""
    paper_from_id: int = Field(..., description="源论文ID")
    paper_to_id: int = Field(..., description="目标论文ID")
    relation_type: str = Field(..., description="关系类型: method_similar, problem_related, custom")
    description: Optional[str] = Field(None, description="关系描述")


class RelationCreate(RelationBase):
    """创建关联关系的请求模型"""
    pass


class Relation(RelationBase):
    """关联关系完整模型"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PaperWithAnalysis(Paper):
    """论文及其分析记录"""
    analysis: Optional[Analysis] = None


class RelationWithPapers(Relation):
    """关联关系及关联的论文信息"""
    paper_from: Optional[Paper] = None
    paper_to: Optional[Paper] = None


# ========== 对话相关模型 ==========

class ConversationBase(BaseModel):
    """对话基础模型"""
    paper_id: int = Field(..., description="关联的论文ID")
    role: str = Field(..., description="消息角色: user, assistant, system")
    content: str = Field(..., description="消息内容")


class ConversationCreate(ConversationBase):
    """创建对话记录的请求模型"""
    pass


class Conversation(ConversationBase):
    """对话完整模型（包含数据库字段）"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    """AI对话请求模型"""
    paper_id: int = Field(..., description="关联的论文ID")
    user_message: str = Field(..., description="用户消息", min_length=1)


class ChatResponse(BaseModel):
    """AI对话响应模型"""
    content: str = Field(..., description="AI回复内容")
    conversation_id: int = Field(..., description="对话记录ID")
    created_at: datetime = Field(..., description="创建时间")


# ========== 自动分析相关模型 ==========

class AutoAnalysisResult(BaseModel):
    """AI自动分析结果模型"""
    main_work: str = Field(..., description="主要工作描述")
    innovations: List[str] = Field(..., description="创新点列表")
    structured_tags: List[str] = Field(..., description="结构化标签")
    source_code_url: Optional[str] = Field(None, description="源码链接")
    has_code: bool = Field(False, description="是否有源码")


class AutoAnalysisResponse(BaseModel):
    """自动分析响应模型"""
    success: bool = Field(..., description="是否成功")
    analysis: Optional[AutoAnalysisResult] = Field(None, description="分析结果")
    message: str = Field(..., description="消息")
    updated: bool = Field(False, description="是否已更新到数据库")
