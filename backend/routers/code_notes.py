"""代码笔记API路由"""
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from pydantic import BaseModel, Field
from typing import List, Optional
from supabase import Client
from backend.database import get_db
from datetime import datetime
import uuid
import os

router = APIRouter(prefix="/code-notes", tags=["code-notes"])


class CodeNoteCreate(BaseModel):
    """创建笔记请求"""
    paper_id: int
    note_type: str = Field(..., pattern="^(code|discussion)$")
    title: str = Field(..., min_length=1, max_length=500)
    content: Optional[str] = None
    images: List[str] = Field(default_factory=list)


class CodeNoteUpdate(BaseModel):
    """更新笔记请求"""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    content: Optional[str] = None
    images: Optional[List[str]] = None


class CodeNoteResponse(BaseModel):
    """笔记响应"""
    id: int
    paper_id: int
    note_type: str
    title: str
    content: Optional[str]
    images: List[str]
    order_index: int
    created_at: str
    updated_at: str


@router.get("/paper/{paper_id}")
async def get_paper_notes(
    paper_id: int,
    note_type: Optional[str] = None,
    db: Client = Depends(get_db)
) -> List[CodeNoteResponse]:
    """获取论文的所有笔记"""
    try:
        query = db.table("code_notes").select("*").eq("paper_id", paper_id)

        if note_type:
            query = query.eq("note_type", note_type)

        # 按order_index降序，created_at降序排序
        query = query.order("order_index", desc=True).order("created_at", desc=True)

        response = query.execute()

        return [
            CodeNoteResponse(
                id=note["id"],
                paper_id=note["paper_id"],
                note_type=note["note_type"],
                title=note["title"],
                content=note.get("content"),
                images=note.get("images") or [],
                order_index=note.get("order_index", 0),
                created_at=note["created_at"],
                updated_at=note["updated_at"]
            )
            for note in response.data
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取笔记失败: {str(e)}")


@router.post("/", status_code=201)
async def create_note(
    note: CodeNoteCreate,
    db: Client = Depends(get_db)
) -> CodeNoteResponse:
    """创建新笔记"""
    try:
        # 验证论文是否存在
        paper_response = db.table("papers").select("id").eq("id", note.paper_id).execute()
        if not paper_response.data:
            raise HTTPException(status_code=404, detail="论文不存在")

        # 创建笔记
        insert_data = {
            "paper_id": note.paper_id,
            "note_type": note.note_type,
            "title": note.title,
            "content": note.content,
            "images": note.images,
            "order_index": 0
        }

        response = db.table("code_notes").insert(insert_data).execute()

        if not response.data:
            raise HTTPException(status_code=500, detail="创建笔记失败")

        created_note = response.data[0]

        return CodeNoteResponse(
            id=created_note["id"],
            paper_id=created_note["paper_id"],
            note_type=created_note["note_type"],
            title=created_note["title"],
            content=created_note.get("content"),
            images=created_note.get("images") or [],
            order_index=created_note.get("order_index", 0),
            created_at=created_note["created_at"],
            updated_at=created_note["updated_at"]
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建笔记失败: {str(e)}")


@router.put("/{note_id}")
async def update_note(
    note_id: int,
    note: CodeNoteUpdate,
    db: Client = Depends(get_db)
) -> CodeNoteResponse:
    """更新笔记"""
    try:
        # 构建更新数据
        update_data = {}
        if note.title is not None:
            update_data["title"] = note.title
        if note.content is not None:
            update_data["content"] = note.content
        if note.images is not None:
            update_data["images"] = note.images

        if not update_data:
            raise HTTPException(status_code=400, detail="没有要更新的数据")

        # 更新笔记
        response = db.table("code_notes").update(update_data).eq("id", note_id).execute()

        if not response.data:
            raise HTTPException(status_code=404, detail="笔记不存在")

        updated_note = response.data[0]

        return CodeNoteResponse(
            id=updated_note["id"],
            paper_id=updated_note["paper_id"],
            note_type=updated_note["note_type"],
            title=updated_note["title"],
            content=updated_note.get("content"),
            images=updated_note.get("images") or [],
            order_index=updated_note.get("order_index", 0),
            created_at=updated_note["created_at"],
            updated_at=updated_note["updated_at"]
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新笔记失败: {str(e)}")


@router.delete("/{note_id}")
async def delete_note(
    note_id: int,
    db: Client = Depends(get_db)
):
    """删除笔记"""
    try:
        # 先获取笔记信息（用于删除图片）
        note_response = db.table("code_notes").select("images").eq("id", note_id).execute()

        if not note_response.data:
            raise HTTPException(status_code=404, detail="笔记不存在")

        # 删除笔记
        db.table("code_notes").delete().eq("id", note_id).execute()

        return {"success": True, "message": "笔记已删除"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除笔记失败: {str(e)}")


@router.post("/upload-image")
async def upload_image(
    file: UploadFile = File(...),
    db: Client = Depends(get_db)
):
    """上传笔记截图"""
    try:
        # 验证文件类型
        allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/gif", "image/webp"]
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail="不支持的图片格式，仅支持: JPG, PNG, GIF, WebP"
            )

        # 验证文件大小（限制5MB）
        contents = await file.read()
        if len(contents) > 5 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="图片大小不能超过5MB")

        # 生成唯一文件名
        file_ext = os.path.splitext(file.filename)[1]
        unique_filename = f"note-images/{uuid.uuid4()}{file_ext}"

        # 上传到Supabase Storage
        try:
            storage_response = db.storage.from_("paper-pdfs").upload(
                path=unique_filename,
                file=contents,
                file_options={"content-type": file.content_type}
            )

            # 获取公开URL
            public_url = db.storage.from_("paper-pdfs").get_public_url(unique_filename)

            return {
                "success": True,
                "url": public_url,
                "filename": file.filename
            }

        except Exception as storage_error:
            raise HTTPException(
                status_code=500,
                detail=f"上传图片到存储失败: {str(storage_error)}"
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"上传图片失败: {str(e)}")


@router.post("/{note_id}/reorder")
async def reorder_note(
    note_id: int,
    new_order: int,
    db: Client = Depends(get_db)
):
    """调整笔记排序"""
    try:
        response = db.table("code_notes").update({
            "order_index": new_order
        }).eq("id", note_id).execute()

        if not response.data:
            raise HTTPException(status_code=404, detail="笔记不存在")

        return {"success": True, "message": "排序已更新"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新排序失败: {str(e)}")
