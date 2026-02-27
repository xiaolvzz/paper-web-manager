"""论文管理API"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query, UploadFile, File
from pydantic import BaseModel
from supabase import Client
from backend.database import get_db
from backend.models import Paper, PaperCreate, PaperUpdate
from backend.utils.pdf_processor import process_uploaded_pdf, upload_pdf_to_supabase
from backend.utils.arxiv_helper import fetch_arxiv_paper

router = APIRouter(prefix="/papers", tags=["papers"])


@router.get("/", response_model=List[Paper])
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

        return response.data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取论文列表失败: {str(e)}")


@router.get("/{paper_id}", response_model=Paper)
async def get_paper(paper_id: int, db: Client = Depends(get_db)):
    """获取单篇论文详情"""
    try:
        response = db.table("papers").select("*").eq("id", paper_id).execute()

        if not response.data:
            raise HTTPException(status_code=404, detail="论文不存在")

        return response.data[0]

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取论文失败: {str(e)}")


@router.post("/", response_model=Paper, status_code=201)
async def create_paper(paper: PaperCreate, db: Client = Depends(get_db)):
    """创建新论文"""
    try:
        response = db.table("papers").insert(paper.model_dump()).execute()

        if not response.data:
            raise HTTPException(status_code=400, detail="创建论文失败")

        return response.data[0]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建论文失败: {str(e)}")


@router.put("/{paper_id}", response_model=Paper)
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

        response = db.table("papers").update(update_data).eq("id", paper_id).execute()

        if not response.data:
            raise HTTPException(status_code=404, detail="论文不存在")

        return response.data[0]

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

        db.table("papers").update(update_data).eq("id", paper_id).execute()

        return {
            "message": "PDF上传成功",
            "text_length": len(extracted_text),
            "storage_path": storage_path
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
