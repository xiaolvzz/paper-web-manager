"""论文管理API"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query, UploadFile, File
from pydantic import BaseModel
from supabase import Client
from backend.database import get_db
from backend.models import Paper, PaperCreate, PaperUpdate, AutoAnalysisResult, AutoAnalysisResponse
from backend.utils.pdf_processor import process_uploaded_pdf, upload_pdf_to_supabase
from backend.utils.arxiv_helper import fetch_arxiv_paper
from backend.utils.ai_providers import ai_manager
from datetime import datetime
import json
import re

router = APIRouter(prefix="/papers", tags=["papers"])


@router.get("/")
async def get_papers(
    search: Optional[str] = Query(None, description="搜索关键词（标题、作者）"),
    year: Optional[int] = Query(None, description="年份筛选"),
    tags: Optional[str] = Query(None, description="标签筛选"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Client = Depends(get_db)
):
    """获取论文列表（支持搜索和筛选）"""
    try:
        query = db.table("papers").select("*")

        # 搜索
        if search:
            query = query.or_(f"title.ilike.%{search}%,authors.ilike.%{search}%")

        # 年份筛选
        if year:
            query = query.eq("year", year)

        # 标签筛选
        if tags:
            query = query.ilike("tags", f"%{tags}%")

        # 分页和排序
        response = query.order("created_at", desc=True).range(offset, offset + limit - 1).execute()

        # 直接返回数据，不进行Pydantic验证（兼容数据库字段变化）
        papers = response.data

        # 为每个论文补充默认值（如果字段不存在）
        for paper in papers:
            paper.setdefault('source_code_url', None)
            paper.setdefault('main_work', None)
            paper.setdefault('innovations', None)
            paper.setdefault('structured_tags', None)
            paper.setdefault('auto_analyzed', False)
            paper.setdefault('auto_analysis_date', None)

        return papers

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取论文列表失败: {str(e)}")


@router.get("/{paper_id}")
async def get_paper(paper_id: int, db: Client = Depends(get_db)):
    """获取单篇论文详情"""
    try:
        response = db.table("papers").select("*").eq("id", paper_id).execute()

        if not response.data:
            raise HTTPException(status_code=404, detail="论文不存在")

        paper = response.data[0]

        # 补充默认值
        paper.setdefault('source_code_url', None)
        paper.setdefault('main_work', None)
        paper.setdefault('innovations', None)
        paper.setdefault('structured_tags', None)
        paper.setdefault('auto_analyzed', False)
        paper.setdefault('auto_analysis_date', None)

        return paper

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取论文失败: {str(e)}")


@router.post("/", status_code=201)
async def create_paper(paper: PaperCreate, db: Client = Depends(get_db)):
    """创建新论文"""
    try:
        # 过滤掉None值和新字段（如果数据库中不存在）
        paper_data = {k: v for k, v in paper.model_dump().items() if v is not None}

        # 移除可能不存在的新字段
        new_fields = ['source_code_url', 'main_work', 'innovations', 'structured_tags', 'auto_analyzed', 'auto_analysis_date']
        for field in new_fields:
            paper_data.pop(field, None)

        response = db.table("papers").insert(paper_data).execute()

        if not response.data:
            raise HTTPException(status_code=400, detail="创建论文失败")

        return response.data[0]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建论文失败: {str(e)}")


@router.put("/{paper_id}")
async def update_paper(
    paper_id: int,
    paper: PaperUpdate,
    db: Client = Depends(get_db)
):
    """更新论文信息"""
    try:
        # 只更新提供的字段
        update_data = {k: v for k, v in paper.model_dump().items() if v is not None}

        if not update_data:
            raise HTTPException(status_code=400, detail="没有需要更新的字段")

        # 尝试更新，如果字段不存在会自动忽略
        try:
            response = db.table("papers").update(update_data).eq("id", paper_id).execute()
        except Exception as db_error:
            # 如果失败，尝试只更新基本字段
            basic_fields = ['title', 'authors', 'year', 'pdf_path', 'abstract', 'tags',
                          'github_url', 'domain', 'pdf_storage_path', 'pdf_text_content', 'arxiv_id']
            update_data = {k: v for k, v in update_data.items() if k in basic_fields}
            response = db.table("papers").update(update_data).eq("id", paper_id).execute()

        if not response.data:
            raise HTTPException(status_code=404, detail="论文不存在")

        paper_result = response.data[0]

        # 补充默认值
        paper_result.setdefault('source_code_url', None)
        paper_result.setdefault('main_work', None)
        paper_result.setdefault('innovations', None)
        paper_result.setdefault('structured_tags', None)
        paper_result.setdefault('auto_analyzed', False)
        paper_result.setdefault('auto_analysis_date', None)

        return paper_result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新论文失败: {str(e)}")


@router.delete("/{paper_id}", status_code=204)
async def delete_paper(paper_id: int, db: Client = Depends(get_db)):
    """删除论文"""
    try:
        response = db.table("papers").delete().eq("id", paper_id).execute()

        if not response.data:
            raise HTTPException(status_code=404, detail="论文不存在")

        return None

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除论文失败: {str(e)}")


@router.get("/{paper_id}/full")
async def get_paper_with_analysis(paper_id: int, db: Client = Depends(get_db)):
    """获取论文及其分析记录"""
    try:
        # 获取论文
        paper_response = db.table("papers").select("*").eq("id", paper_id).execute()

        if not paper_response.data:
            raise HTTPException(status_code=404, detail="论文不存在")

        paper = paper_response.data[0]

        # 补充默认值
        paper.setdefault('source_code_url', None)
        paper.setdefault('main_work', None)
        paper.setdefault('innovations', None)
        paper.setdefault('structured_tags', None)
        paper.setdefault('auto_analyzed', False)
        paper.setdefault('auto_analysis_date', None)

        # 获取分析记录
        analysis_response = db.table("analysis").select("*").eq("paper_id", paper_id).execute()

        # 获取关联关系
        relations_response = db.table("relations").select("*").or_(
            f"paper_from_id.eq.{paper_id},paper_to_id.eq.{paper_id}"
        ).execute()

        return {
            "paper": paper,
            "analysis": analysis_response.data[0] if analysis_response.data else None,
            "relations": relations_response.data
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取论文详情失败: {str(e)}")


# ========== 新增端点：PDF和arXiv处理 ==========

@router.post("/{paper_id}/upload-pdf")
async def upload_pdf(
    paper_id: int,
    file: UploadFile = File(...),
    db: Client = Depends(get_db)
):
    """
    上传PDF文件到论文

    处理流程：
    1. 验证论文存在
    2. 提取PDF文本
    3. 上传PDF到Supabase Storage
    4. 更新papers表
    """
    try:
        # 验证论文存在
        paper_response = db.table("papers").select("id").eq("id", paper_id).execute()
        if not paper_response.data:
            raise HTTPException(status_code=404, detail="论文不存在")

        # 处理PDF文件
        file_bytes, extracted_text = await process_uploaded_pdf(file)

        # 上传到Supabase Storage
        try:
            storage_path = upload_pdf_to_supabase(db, file_bytes, file.filename, paper_id)
        except Exception as e:
            # 如果上传到云端失败，仍然保存文本内容
            storage_path = None
            print(f"Warning: PDF上传到Storage失败: {e}")

        # 更新papers表
        update_data = {
            "pdf_text_content": extracted_text
        }
        if storage_path:
            update_data["pdf_storage_path"] = storage_path
            # 同时设置pdf_path，这样前端可以显示"有PDF"
            update_data["pdf_path"] = storage_path

        db.table("papers").update(update_data).eq("id", paper_id).execute()

        return {
            "message": "PDF上传成功",
            "text_length": len(extracted_text),
            "storage_path": storage_path,
            "pdf_path": storage_path  # 返回给前端使用
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"上传PDF失败: {str(e)}")


class ArxivImportRequest(BaseModel):
    """arXiv导入请求"""
    arxiv_input: str


@router.post("/{paper_id}/import-from-arxiv")
async def import_from_arxiv(
    paper_id: int,
    request: ArxivImportRequest,
    db: Client = Depends(get_db)
):
    """
    从arXiv导入论文信息

    自动获取标题、作者、摘要、PDF内容等
    """
    try:
        # 验证论文存在
        paper_response = db.table("papers").select("*").eq("id", paper_id).execute()
        if not paper_response.data:
            raise HTTPException(status_code=404, detail="论文不存在")

        # 从arXiv获取论文信息
        arxiv_data = await fetch_arxiv_paper(request.arxiv_input)

        # 更新论文信息
        update_data = {
            "title": arxiv_data["title"],
            "authors": arxiv_data["authors"],
            "year": arxiv_data["year"],
            "abstract": arxiv_data["abstract"],
            "arxiv_id": arxiv_data["arxiv_id"],
            "pdf_path": arxiv_data["pdf_url"]
        }

        # 如果成功提取了PDF文本，也更新
        if arxiv_data.get("pdf_text_content"):
            update_data["pdf_text_content"] = arxiv_data["pdf_text_content"]

        db.table("papers").update(update_data).eq("id", paper_id).execute()

        return {
            "message": "arXiv论文导入成功",
            "arxiv_id": arxiv_data["arxiv_id"],
            "has_pdf_text": bool(arxiv_data.get("pdf_text_content")),
            "error": arxiv_data.get("error")
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导入arXiv论文失败: {str(e)}")


class TextContentRequest(BaseModel):
    """文本内容请求"""
    text_content: str


@router.post("/{paper_id}/add-text-content")
async def add_text_content(
    paper_id: int,
    request: TextContentRequest,
    db: Client = Depends(get_db)
):
    """
    手动添加论文文本内容

    用于用户直接粘贴论文内容的场景
    """
    try:
        # 验证论文存在
        paper_response = db.table("papers").select("id").eq("id", paper_id).execute()
        if not paper_response.data:
            raise HTTPException(status_code=404, detail="论文不存在")

        # 验证文本长度
        if len(request.text_content.strip()) < 50:
            raise HTTPException(status_code=400, detail="文本内容过短，请至少输入50个字符")

        # 更新papers表
        db.table("papers").update({
            "pdf_text_content": request.text_content
        }).eq("id", paper_id).execute()

        return {
            "message": "文本内容已保存",
            "text_length": len(request.text_content)
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"保存文本内容失败: {str(e)}")


# ========== AI自动分析端点 ==========

@router.post("/{paper_id}/auto-analyze", response_model=AutoAnalysisResponse)
async def auto_analyze_paper(
    paper_id: int,
    update_db: bool = Query(True, description="是否更新到数据库"),
    db: Client = Depends(get_db)
):
    """
    AI自动分析论文

    功能：
    1. 读取论文标题、摘要、全文
    2. 使用AI提取：主要工作、创新点、标签、源码链接
    3. 返回结构化结果
    4. 可选：直接更新到数据库

    返回格式：
    {
        "main_work": "这篇论文提出了...",
        "innovations": ["创新点1", "创新点2"],
        "structured_tags": ["Transformer", "NLP", "Attention"],
        "source_code_url": "https://github.com/...",
        "has_code": true
    }
    """
    try:
        # 1. 获取论文信息
        paper_response = db.table("papers").select("*").eq("id", paper_id).execute()
        if not paper_response.data:
            raise HTTPException(status_code=404, detail="论文不存在")

        paper = paper_response.data[0]

        # 2. 构建分析内容
        content_parts = []
        content_parts.append(f"标题: {paper['title']}")

        if paper.get('authors'):
            content_parts.append(f"作者: {paper['authors']}")

        if paper.get('year'):
            content_parts.append(f"年份: {paper['year']}")

        if paper.get('abstract'):
            content_parts.append(f"\n摘要:\n{paper['abstract']}")

        # 如果有全文，添加前5000字
        if paper.get('pdf_text_content'):
            text_content = paper['pdf_text_content'][:5000]
            content_parts.append(f"\n论文内容（前5000字）:\n{text_content}")

        paper_content = "\n\n".join(content_parts)

        # 3. 构建AI提示词
        system_prompt = """你是一位专业的学术论文分析助手。你的任务是分析论文并提取关键信息。

请以JSON格式输出，包含以下字段：
{
  "main_work": "用1-2句话概括论文的主要工作",
  "innovations": ["创新点1", "创新点2", "创新点3"],  // 列出2-5个主要创新点
  "structured_tags": ["标签1", "标签2", "标签3"],  // 3-8个关键技术标签
  "source_code_url": "源码链接或null",  // 如果论文中提到代码链接则提取，否则为null
  "has_code": true/false  // 是否有源码
}

注意事项：
1. main_work要简洁清晰，突出核心贡献
2. innovations每项用简短一句话描述，突出"新"和"不同"
3. structured_tags使用标准技术术语（如Transformer、CNN、BERT等）
4. 仔细在论文中寻找GitHub、代码仓库等关键词来提取source_code_url
5. 只输出JSON，不要其他文字"""

        user_prompt = f"请分析以下论文：\n\n{paper_content}"

        # 4. 调用AI
        try:
            ai_response = await ai_manager.chat(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,  # 较低温度，更稳定的输出
                max_tokens=2000
            )

            # 5. 解析AI返回的JSON
            # 提取JSON（可能被markdown代码块包裹）
            json_match = re.search(r'```json\s*(\{.*?\})\s*```', ai_response, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                # 直接尝试解析
                json_str = ai_response.strip()

            analysis_data = json.loads(json_str)

            # 6. 验证和标准化数据
            analysis_result = AutoAnalysisResult(
                main_work=analysis_data.get("main_work", ""),
                innovations=analysis_data.get("innovations", []),
                structured_tags=analysis_data.get("structured_tags", []),
                source_code_url=analysis_data.get("source_code_url") if analysis_data.get("source_code_url") not in [None, "null", ""] else None,
                has_code=analysis_data.get("has_code", False)
            )

            # 7. 更新数据库（如果需要）
            updated = False
            if update_db:
                update_data = {}

                # 只添加存在的字段（兼容数据库迁移前的情况）
                try:
                    # 尝试更新所有新字段
                    update_data = {
                        "main_work": analysis_result.main_work,
                        "innovations": json.dumps(analysis_result.innovations, ensure_ascii=False),
                        "structured_tags": json.dumps(analysis_result.structured_tags, ensure_ascii=False),
                        "auto_analyzed": True,
                        "auto_analysis_date": datetime.now().isoformat()
                    }

                    if analysis_result.source_code_url:
                        update_data["source_code_url"] = analysis_result.source_code_url

                    db.table("papers").update(update_data).eq("id", paper_id).execute()
                    updated = True
                except Exception as update_error:
                    # 如果新字段不存在，至少尝试更新source_code_url到基本字段
                    print(f"Warning: 更新新字段失败，尝试基本更新: {update_error}")
                    try:
                        if analysis_result.source_code_url:
                            # 尝试只更新github_url作为兼容字段
                            db.table("papers").update({
                                "github_url": analysis_result.source_code_url
                            }).eq("id", paper_id).execute()
                            updated = True
                    except:
                        pass

            return AutoAnalysisResponse(
                success=True,
                analysis=analysis_result,
                message="分析完成",
                updated=updated
            )

        except json.JSONDecodeError as e:
            # JSON解析失败，返回原始响应供调试
            raise HTTPException(
                status_code=500,
                detail=f"AI返回格式错误，无法解析JSON: {str(e)}\n原始响应: {ai_response[:200]}"
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"自动分析失败: {str(e)}")
