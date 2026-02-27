"""领域标签管理API"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from supabase import Client
from backend.database import get_db

router = APIRouter(prefix="/domains", tags=["domains"])


class Domain(BaseModel):
    """领域模型"""
    id: int
    name: str
    color: str
    icon: str
    description: Optional[str] = None
    is_predefined: bool = False


class DomainCreate(BaseModel):
    """创建领域"""
    name: str
    color: str = "#6366f1"
    icon: str = "🏷️"
    description: Optional[str] = None


class PaperDomainAssign(BaseModel):
    """论文-领域关联"""
    paper_id: int
    domain_ids: List[int]


@router.get("/")
async def get_domains(db: Client = Depends(get_db)):
    """获取所有领域标签"""
    try:
        response = db.table("domains").select("*").order("is_predefined.desc, name").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取领域失败: {str(e)}")


@router.post("/")
async def create_domain(domain: DomainCreate, db: Client = Depends(get_db)):
    """创建自定义领域"""
    try:
        # 检查是否已存在
        existing = db.table("domains").select("id").eq("name", domain.name).execute()
        if existing.data:
            raise HTTPException(status_code=400, detail="该领域已存在")

        response = db.table("domains").insert({
            "name": domain.name,
            "color": domain.color,
            "icon": domain.icon,
            "description": domain.description,
            "is_predefined": False
        }).execute()

        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建领域失败: {str(e)}")


@router.delete("/{domain_id}")
async def delete_domain(domain_id: int, db: Client = Depends(get_db)):
    """删除自定义领域（不能删除预设领域）"""
    try:
        # 检查是否为预设领域
        domain = db.table("domains").select("is_predefined").eq("id", domain_id).execute()
        if not domain.data:
            raise HTTPException(status_code=404, detail="领域不存在")

        if domain.data[0]["is_predefined"]:
            raise HTTPException(status_code=400, detail="不能删除预设领域")

        db.table("domains").delete().eq("id", domain_id).execute()
        return {"message": "删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除领域失败: {str(e)}")


@router.post("/assign")
async def assign_domains_to_paper(assignment: PaperDomainAssign, db: Client = Depends(get_db)):
    """为论文分配领域标签"""
    try:
        paper_id = assignment.paper_id
        domain_ids = assignment.domain_ids

        # 删除现有关联
        db.table("paper_domains").delete().eq("paper_id", paper_id).execute()

        # 添加新关联
        if domain_ids:
            records = [{"paper_id": paper_id, "domain_id": did} for did in domain_ids]
            db.table("paper_domains").insert(records).execute()

        return {"message": "领域分配成功", "count": len(domain_ids)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分配领域失败: {str(e)}")


@router.get("/paper/{paper_id}")
async def get_paper_domains(paper_id: int, db: Client = Depends(get_db)):
    """获取论文的所有领域标签"""
    try:
        response = db.table("paper_domains").select(
            "domain_id, confidence, domains(id, name, color, icon)"
        ).eq("paper_id", paper_id).execute()

        domains = []
        for item in response.data:
            domain_info = item.get("domains")
            if domain_info:
                domains.append({
                    "id": domain_info["id"],
                    "name": domain_info["name"],
                    "color": domain_info["color"],
                    "icon": domain_info["icon"],
                    "confidence": item.get("confidence", 1.0)
                })

        return domains
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取论文领域失败: {str(e)}")


@router.get("/{domain_id}/papers")
async def get_domain_papers(domain_id: int, db: Client = Depends(get_db)):
    """获取某个领域下的所有论文"""
    try:
        response = db.table("paper_domains").select(
            "paper_id, papers(id, title, authors, year, abstract)"
        ).eq("domain_id", domain_id).execute()

        papers = []
        for item in response.data:
            paper_info = item.get("papers")
            if paper_info:
                papers.append(paper_info)

        return papers
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取领域论文失败: {str(e)}")
