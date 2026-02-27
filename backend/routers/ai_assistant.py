"""AI助手路由 - 使用Groq API提供论文摘要和分析功能"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import os
import httpx
from typing import Optional

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

    使用Groq的快速LLM生成中文摘要
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="AI服务未配置。请联系管理员配置GROQ_API_KEY环境变量。"
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
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.2-90b-text-preview",
                    "messages": [
                        {
                            "role": "system",
                            "content": "你是一位专业的学术论文助手，擅长提炼论文核心内容和创新点。"
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.7,
                    "max_tokens": 512
                }
            )

            if response.status_code != 200:
                error_detail = response.text
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"AI API调用失败: {error_detail}"
                )

            result = response.json()
            summary = result["choices"][0]["message"]["content"]

            return AIResponse(
                content=summary,
                model="llama-3.2-90b-text-preview"
            )

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="AI服务超时，请稍后重试"
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
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="AI服务未配置。请联系管理员配置GROQ_API_KEY环境变量。"
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
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.2-90b-text-preview",
                    "messages": [
                        {
                            "role": "system",
                            "content": "你是一位专业的学术论文分析师，擅长识别和总结论文的核心创新点。"
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.5,
                    "max_tokens": 512
                }
            )

            if response.status_code != 200:
                error_detail = response.text
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"AI API调用失败: {error_detail}"
                )

            result = response.json()
            innovations = result["choices"][0]["message"]["content"]

            return AIResponse(
                content=innovations,
                model="llama-3.2-90b-text-preview"
            )

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="AI服务超时，请稍后重试"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"提取创新点时出错: {str(e)}"
        )


@router.get("/health")
async def ai_health():
    """AI服务健康检查"""
    api_key = os.getenv("GROQ_API_KEY")
    return {
        "status": "healthy" if api_key else "not_configured",
        "provider": "Groq",
        "model": "llama-3.2-90b-text-preview",
        "configured": bool(api_key)
    }
