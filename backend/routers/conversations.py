"""对话路由 - AI对话功能"""
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from datetime import datetime

from backend.database import get_supabase_client
from backend.utils.ai_providers import ai_manager
from backend.models import (
    Conversation,
    ConversationCreate,
    ChatRequest,
    ChatResponse
)

router = APIRouter(prefix="/conversations", tags=["conversations"])


def build_ai_context(paper_data: dict, recent_conversations: List[dict]) -> str:
    """构建AI对话上下文"""
    # 基础论文信息
    title = paper_data.get('title', '未知')
    authors = paper_data.get('authors', '未知')
    abstract = paper_data.get('abstract', '暂无摘要')

    # PDF文本内容（截取前10000字）
    pdf_text = paper_data.get('pdf_text_content', '')
    if pdf_text:
        pdf_text = pdf_text[:10000]
        if len(paper_data.get('pdf_text_content', '')) > 10000:
            pdf_text += "\n\n... (内容过长，已截断)"

    # 构建system prompt
    system_prompt = f"""你是一位专业的学术论文阅读助手。你的任务是帮助用户深入理解论文内容。

当前论文信息：
- 标题：{title}
- 作者：{authors}
- 摘要：{abstract}

{"全文内容（节选）：" + pdf_text if pdf_text else "（用户尚未上传论文全文，请基于摘要回答）"}

请注意：
1. 回答要准确、专业、易懂
2. 主动提炼论文的关键信息（框架、创新点、方法、源码链接等）
3. 当用户询问"有源码吗"、"用了什么方法"等问题时，从论文内容中寻找答案
4. 使用中文回答
5. 如果不确定，诚实说明而不是编造
"""

    return system_prompt


async def call_ai_api(system_prompt: str, user_message: str, conversation_history: List[dict]) -> str:
    """调用AI服务获取回复"""
    if not ai_manager.is_configured():
        raise HTTPException(
            status_code=500,
            detail="AI服务未配置。请配置以下任一API密钥：DEEPSEEK_API_KEY, ZHIPU_API_KEY, QWEN_API_KEY, GROQ_API_KEY"
        )

    # 构建消息列表
    messages = [{"role": "system", "content": system_prompt}]

    # 添加最近10轮对话历史
    for conv in conversation_history[-10:]:
        messages.append({
            "role": conv["role"],
            "content": conv["content"]
        })

    # 添加当前用户消息
    messages.append({"role": "user", "content": user_message})

    # 调用AI API
    try:
        return await ai_manager.chat(messages, temperature=0.7, max_tokens=2048)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI对话失败: {str(e)}"
        )


@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest):
    """
    与AI对话

    发送消息并获取AI回复，对话记录会自动保存
    """
    supabase = get_supabase_client()

    # 1. 获取论文信息
    paper_response = supabase.table('papers').select('*').eq('id', request.paper_id).execute()
    if not paper_response.data:
        raise HTTPException(status_code=404, detail="论文不存在")

    paper_data = paper_response.data[0]

    # 2. 获取最近的对话历史
    conv_response = supabase.table('conversations')\
        .select('*')\
        .eq('paper_id', request.paper_id)\
        .order('created_at', desc=False)\
        .execute()

    conversation_history = conv_response.data if conv_response.data else []

    # 3. 保存用户消息
    user_conv = {
        "paper_id": request.paper_id,
        "role": "user",
        "content": request.user_message
    }
    supabase.table('conversations').insert(user_conv).execute()

    # 4. 构建AI上下文
    system_prompt = build_ai_context(paper_data, conversation_history)

    # 5. 调用AI获取回复
    ai_response = await call_ai_api(system_prompt, request.user_message, conversation_history)

    # 6. 保存AI回复
    assistant_conv = {
        "paper_id": request.paper_id,
        "role": "assistant",
        "content": ai_response
    }
    insert_result = supabase.table('conversations').insert(assistant_conv).execute()

    if not insert_result.data:
        raise HTTPException(status_code=500, detail="保存AI回复失败")

    saved_conv = insert_result.data[0]

    return ChatResponse(
        content=ai_response,
        conversation_id=saved_conv["id"],
        created_at=saved_conv["created_at"]
    )


@router.get("/paper/{paper_id}", response_model=List[Conversation])
async def get_paper_conversations(
    paper_id: int,
    limit: int = 100,
    offset: int = 0
):
    """
    获取某篇论文的对话历史

    按时间正序排列
    """
    supabase = get_supabase_client()

    # 验证论文是否存在
    paper_response = supabase.table('papers').select('id').eq('id', paper_id).execute()
    if not paper_response.data:
        raise HTTPException(status_code=404, detail="论文不存在")

    # 获取对话历史
    response = supabase.table('conversations')\
        .select('*')\
        .eq('paper_id', paper_id)\
        .order('created_at', desc=False)\
        .range(offset, offset + limit - 1)\
        .execute()

    return response.data if response.data else []


@router.delete("/{conversation_id}")
async def delete_conversation(conversation_id: int):
    """删除单条对话记录"""
    supabase = get_supabase_client()

    # 验证对话是否存在
    check_response = supabase.table('conversations').select('id').eq('id', conversation_id).execute()
    if not check_response.data:
        raise HTTPException(status_code=404, detail="对话记录不存在")

    # 删除
    supabase.table('conversations').delete().eq('id', conversation_id).execute()

    return {"message": "删除成功"}


@router.delete("/paper/{paper_id}/all")
async def clear_paper_conversations(paper_id: int):
    """清空某篇论文的所有对话"""
    supabase = get_supabase_client()

    # 验证论文是否存在
    paper_response = supabase.table('papers').select('id').eq('id', paper_id).execute()
    if not paper_response.data:
        raise HTTPException(status_code=404, detail="论文不存在")

    # 删除所有对话
    supabase.table('conversations').delete().eq('paper_id', paper_id).execute()

    return {"message": "对话已清空"}
