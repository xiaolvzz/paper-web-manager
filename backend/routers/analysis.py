"""分析记录管理API"""
from typing import List
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from supabase import Client
from backend.database import get_db
from backend.models import Analysis, AnalysisCreate, AnalysisUpdate
import os
import uuid

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.get("/paper/{paper_id}", response_model=Analysis)
async def get_analysis(paper_id: int, db: Client = Depends(get_db)):
    """获取论文的分析记录"""
    try:
        response = db.table("analysis").select("*").eq("paper_id", paper_id).execute()

        if not response.data:
            raise HTTPException(status_code=404, detail="分析记录不存在")

        return response.data[0]

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取分析记录失败: {str(e)}")


@router.post("/", response_model=Analysis, status_code=201)
async def create_analysis(analysis: AnalysisCreate, db: Client = Depends(get_db)):
    """创建分析记录"""
    try:
        # 检查论文是否存在
        paper_response = db.table("papers").select("id").eq("id", analysis.paper_id).execute()
        if not paper_response.data:
            raise HTTPException(status_code=404, detail="论文不存在")

        # 检查是否已有分析记录
        existing = db.table("analysis").select("id").eq("paper_id", analysis.paper_id).execute()
        if existing.data:
            raise HTTPException(status_code=400, detail="该论文已有分析记录，请使用更新接口")

        response = db.table("analysis").insert(analysis.model_dump()).execute()

        if not response.data:
            raise HTTPException(status_code=400, detail="创建分析记录失败")

        return response.data[0]

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建分析记录失败: {str(e)}")


@router.put("/{analysis_id}", response_model=Analysis)
async def update_analysis(
    analysis_id: int,
    analysis: AnalysisUpdate,
    db: Client = Depends(get_db)
):
    """更新分析记录"""
    try:
        # 只更新提供的字段
        update_data = {k: v for k, v in analysis.model_dump().items() if v is not None}

        if not update_data:
            raise HTTPException(status_code=400, detail="没有需要更新的字段")

        response = db.table("analysis").update(update_data).eq("id", analysis_id).execute()

        if not response.data:
            raise HTTPException(status_code=404, detail="分析记录不存在")

        return response.data[0]

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新分析记录失败: {str(e)}")


@router.put("/paper/{paper_id}", response_model=Analysis)
async def upsert_analysis(
    paper_id: int,
    analysis: AnalysisUpdate,
    db: Client = Depends(get_db)
):
    """更新或创建分析记录（如果不存在则创建）"""
    try:
        # 检查论文是否存在
        paper_response = db.table("papers").select("id").eq("id", paper_id).execute()
        if not paper_response.data:
            raise HTTPException(status_code=404, detail="论文不存在")

        # 尝试获取现有记录
        existing = db.table("analysis").select("*").eq("paper_id", paper_id).execute()

        update_data = {k: v for k, v in analysis.model_dump().items() if v is not None}

        if existing.data:
            # 更新
            response = db.table("analysis").update(update_data).eq("paper_id", paper_id).execute()
        else:
            # 创建
            update_data["paper_id"] = paper_id
            response = db.table("analysis").insert(update_data).execute()

        if not response.data:
            raise HTTPException(status_code=400, detail="保存分析记录失败")

        return response.data[0]

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"保存分析记录失败: {str(e)}")


@router.delete("/{analysis_id}", status_code=204)
async def delete_analysis(analysis_id: int, db: Client = Depends(get_db)):
    """删除分析记录"""
    try:
        response = db.table("analysis").delete().eq("id", analysis_id).execute()

        if not response.data:
            raise HTTPException(status_code=404, detail="分析记录不存在")

        return None

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除分析记录失败: {str(e)}")


@router.post("/upload-image")
async def upload_framework_image(
    file: UploadFile = File(...),
    db: Client = Depends(get_db)
):
    """上传框架图到Supabase Storage"""
    try:
        # 验证文件类型
        allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="只支持图片格式（JPEG, PNG, GIF, WebP）")

        # 生成唯一文件名
        ext = os.path.splitext(file.filename)[1]
        filename = f"{uuid.uuid4()}{ext}"

        # 读取文件内容
        content = await file.read()

        # 上传到Supabase Storage
        storage = db.storage.from_("framework-images")
        storage.upload(filename, content)

        # 获取公开URL
        url = storage.get_public_url(filename)

        return {"url": url, "filename": filename}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"上传图片失败: {str(e)}")
