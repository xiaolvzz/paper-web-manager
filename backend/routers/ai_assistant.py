"""AI助手路由 - 支持多个AI提供商"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import json
from typing import Optional, List

from backend.database import get_supabase_client
from backend.utils.ai_providers import ai_manager

router = APIRouter(prefix="/ai", tags=["ai"])


class SummarizeRequest(BaseModel):
    """摘要请求模型"""
    text: str = Field(..., description="要摘要的文本（如论文摘要）")
    max_length: int = Field(200, description="最大摘要长度（字数）", ge=50, le=500)


class InnovationRequest(BaseModel):
    """创新点提取请求模型"""
    abstract: str = Field(..., description="论文摘要")
    title: Optional[str] = Field(None, description="论文标题（可选，提供更准确的分析）")


class AIResponse(BaseModel):
    """AI响应模型"""
    content: str = Field(..., description="AI生成的内容")
    model: str = Field(..., description="使用的模型名称")


@router.post("/summarize", response_model=AIResponse)
async def summarize_text(request: SummarizeRequest):
    """
    生成论文摘要

    支持多个AI提供商（DeepSeek, 智谱AI, 通义千问, Groq等）
    """
    if not ai_manager.is_configured():
        raise HTTPException(
            status_code=500,
            detail="AI服务未配置。请配置以下任一API密钥：DEEPSEEK_API_KEY, ZHIPU_API_KEY, QWEN_API_KEY, GROQ_API_KEY"
        )

    # 构建prompt
    prompt = f"""请用简洁的中文总结以下论文摘要，突出关键内容：

论文摘要：
{request.text}

要求：
1. 使用中文
2. 不超过{request.max_length}字
3. 突出核心贡献和创新点
4. 使用简洁的学术语言"""

    try:
        messages = [
            {
                "role": "system",
                "content": "你是一位专业的学术论文助手，擅长提炼论文核心内容和创新点。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        summary = await ai_manager.chat(messages, temperature=0.7, max_tokens=512)

        return AIResponse(
            content=summary,
            model=f"{ai_manager.get_provider_name()} - {ai_manager.get_model_name()}"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"生成摘要时出错: {str(e)}"
        )


@router.post("/extract-innovations", response_model=AIResponse)
async def extract_innovations(request: InnovationRequest):
    """
    提取论文创新点

    分析论文摘要，提取主要创新点和贡献
    """
    if not ai_manager.is_configured():
        raise HTTPException(
            status_code=500,
            detail="AI服务未配置。请配置以下任一API密钥：DEEPSEEK_API_KEY, ZHIPU_API_KEY, QWEN_API_KEY, GROQ_API_KEY"
        )

    # 构建prompt
    title_part = f"论文标题：{request.title}\n\n" if request.title else ""
    prompt = f"""{title_part}论文摘要：
{request.abstract}

请以条目形式列出这篇论文的主要创新点和贡献，使用中文：

要求：
1. 每个创新点独立成行，使用"- "开头
2. 3-5个创新点
3. 简洁明了，每个创新点不超过50字
4. 突出技术贡献和实际价值"""

    try:
        messages = [
            {
                "role": "system",
                "content": "你是一位专业的学术论文分析师，擅长识别和总结论文的核心创新点。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        innovations = await ai_manager.chat(messages, temperature=0.5, max_tokens=512)

        return AIResponse(
            content=innovations,
            model=f"{ai_manager.get_provider_name()} - {ai_manager.get_model_name()}"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"提取创新点时出错: {str(e)}"
        )


@router.get("/health")
async def ai_health():
    """AI服务健康检查"""
    return {
        "status": "healthy" if ai_manager.is_configured() else "not_configured",
        "provider": ai_manager.get_provider_name(),
        "model": ai_manager.get_model_name(),
        "configured": ai_manager.is_configured()
    }


@router.get("/models")
async def get_available_models():
    """获取所有AI模型列表和配置状态"""
    models = ai_manager.get_all_providers_status()
    current_provider_id = ai_manager.get_provider_id()

    return {
        "models": models,
        "current_provider": current_provider_id,
        "any_configured": ai_manager.is_configured()
    }


class SelectModelRequest(BaseModel):
    """选择模型请求"""
    provider_id: str = Field(..., description="模型提供商ID (gemini, claude, deepseek等)")


@router.post("/select-model")
async def select_model(request: SelectModelRequest):
    """选择使用指定的AI模型"""
    success = ai_manager.use_provider(request.provider_id)

    if not success:
        raise HTTPException(
            status_code=400,
            detail=f"模型 {request.provider_id} 未配置，请先在环境变量中配置相应的API密钥"
        )

    return {
        "success": True,
        "provider": ai_manager.get_provider_name(),
        "model": ai_manager.get_model_name(),
        "provider_id": request.provider_id
    }


class AnalyzePaperRequest(BaseModel):
    """一键分析论文请求"""
    paper_id: int = Field(..., description="论文ID")


class AnalyzePaperResponse(BaseModel):
    """一键分析论文响应"""
    framework: str = Field(..., description="论文框架描述")
    innovations: List[str] = Field(..., description="创新点列表")
    methods: List[str] = Field(..., description="使用的方法列表")
    source_code: Optional[str] = Field(None, description="源码链接")
    has_code: bool = Field(..., description="是否有开源代码")


@router.post("/analyze-paper", response_model=AnalyzePaperResponse)
async def analyze_paper(request: AnalyzePaperRequest):
    """
    一键分析论文

    使用AI自动提取论文的关键信息：
    - 框架结构
    - 创新点
    - 使用方法
    - 源码链接
    """
    if not ai_manager.is_configured():
        raise HTTPException(
            status_code=500,
            detail="AI服务未配置。请配置以下任一API密钥：DEEPSEEK_API_KEY, ZHIPU_API_KEY, QWEN_API_KEY, GROQ_API_KEY"
        )

    # 获取论文信息
    supabase = get_supabase_client()
    paper_response = supabase.table('papers').select('*').eq('id', request.paper_id).execute()

    if not paper_response.data:
        raise HTTPException(status_code=404, detail="论文不存在")

    paper = paper_response.data[0]

    # 构建分析prompt
    title = paper.get('title', '未知')
    abstract = paper.get('abstract', '')
    pdf_text = paper.get('pdf_text_content', '')

    # 截取PDF内容（前5000字）
    content_for_analysis = pdf_text[:5000] if pdf_text else abstract

    prompt = f"""请详细分析以下论文，提取关键信息。以JSON格式返回结果。

论文标题：{title}

论文内容：
{content_for_analysis}

请提取以下信息并以JSON格式返回：
{{
    "framework": "论文的整体框架和方法架构描述（100-200字）",
    "innovations": ["创新点1", "创新点2", "创新点3"],
    "methods": ["使用的方法1", "方法2", "方法3"],
    "source_code": "GitHub源码链接（如果论文中提到）或null",
    "has_code": true或false
}}

要求：
1. innovations: 提取3-5个主要创新点，每个不超过50字
2. methods: 列出论文使用的主要技术方法
3. source_code: 如果论文中提到GitHub链接、代码仓库等，提取完整URL；否则为null
4. has_code: 根据论文内容判断是否有开源代码
5. 必须返回有效的JSON格式"""

    try:
        messages = [
            {
                "role": "system",
                "content": "你是一位专业的学术论文分析师，擅长提取论文的关键信息。请严格按照JSON格式返回结果。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        ai_output = await ai_manager.chat(messages, temperature=0.3, max_tokens=2048)

        # 尝试解析JSON
        try:
            # 提取JSON部分（AI可能会在JSON前后加说明文字）
            json_start = ai_output.find('{')
            json_end = ai_output.rfind('}') + 1
            json_str = ai_output[json_start:json_end]

            analysis_data = json.loads(json_str)

            return AnalyzePaperResponse(
                framework=analysis_data.get("framework", "暂无框架描述"),
                innovations=analysis_data.get("innovations", ["暂无创新点"]),
                methods=analysis_data.get("methods", ["暂无方法信息"]),
                source_code=analysis_data.get("source_code"),
                has_code=analysis_data.get("has_code", False)
            )

        except json.JSONDecodeError:
            # 如果JSON解析失败，返回默认值
            raise HTTPException(
                status_code=500,
                detail="AI返回格式错误，请重试"
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"分析论文时出错: {str(e)}"
        )
