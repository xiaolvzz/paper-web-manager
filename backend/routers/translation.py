"""翻译API路由"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

from backend.utils.translation_providers import translation_manager

router = APIRouter(prefix="/translate", tags=["translation"])


class TranslateRequest(BaseModel):
    """翻译请求"""
    text: str = Field(..., description="要翻译的文本", min_length=1, max_length=10000)
    source_lang: str = Field("auto", description="源语言（auto=自动检测）")
    target_lang: str = Field("zh", description="目标语言（zh=中文, en=英文）")


class TranslateResponse(BaseModel):
    """翻译响应"""
    translated_text: str = Field(..., description="翻译后的文本")
    source_lang: str = Field(..., description="检测到的源语言")
    target_lang: str = Field(..., description="目标语言")
    provider: str = Field(..., description="使用的翻译服务")


@router.post("/", response_model=TranslateResponse)
async def translate_text(request: TranslateRequest):
    """
    翻译文本

    支持的语言代码：
    - zh: 中文
    - en: 英文
    - ja: 日语
    - ko: 韩语
    - fr: 法语
    - de: 德语
    - es: 西班牙语
    - ru: 俄语
    - auto: 自动检测（推荐）
    """
    try:
        translated = await translation_manager.translate(
            request.text,
            request.source_lang,
            request.target_lang
        )

        return TranslateResponse(
            translated_text=translated,
            source_lang=request.source_lang,
            target_lang=request.target_lang,
            provider=translation_manager.get_provider_name()
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"翻译失败: {str(e)}"
        )


@router.get("/health")
async def translation_health():
    """翻译服务健康检查"""
    return {
        "status": "healthy",
        "provider": translation_manager.get_provider_name(),
        "configured": translation_manager.is_configured()
    }


@router.get("/supported-languages")
async def get_supported_languages():
    """获取支持的语言列表"""
    return {
        "languages": [
            {"code": "auto", "name": "自动检测"},
            {"code": "zh", "name": "中文"},
            {"code": "en", "name": "英文"},
            {"code": "ja", "name": "日语"},
            {"code": "ko", "name": "韩语"},
            {"code": "fr", "name": "法语"},
            {"code": "de", "name": "德语"},
            {"code": "es", "name": "西班牙语"},
            {"code": "ru", "name": "俄语"}
        ]
    }
