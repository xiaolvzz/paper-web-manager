"""论文管理API"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from supabase import Client
from backend.database import get_db
from backend.models import Paper, PaperCreate, PaperUpdate

router = APIRouter(prefix="/api/papers", tags=["papers"])


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
