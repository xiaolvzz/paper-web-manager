"""标签管理API路由"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from supabase import Client
from backend.database import get_db

router = APIRouter(prefix="/tags", tags=["tags"])


class DomainResponse(BaseModel):
    """领域标签响应"""
    id: int
    name: str
    color: str
    icon: str
    description: Optional[str]
    is_predefined: bool


class AddDomainRequest(BaseModel):
    """添加标签到论文"""
    paper_id: int
    domain_ids: List[int]


class RemoveDomainRequest(BaseModel):
    """移除标签"""
    paper_id: int
    domain_id: int


@router.get("/domains")
async def get_all_domains(db: Client = Depends(get_db)) -> List[DomainResponse]:
    """获取所有领域标签"""
    try:
        response = db.table("domains").select("*").order("is_predefined", desc=True).order("name").execute()

        return [
            DomainResponse(
                id=domain["id"],
                name=domain["name"],
                color=domain["color"],
                icon=domain.get("icon", "🏷️"),
                description=domain.get("description"),
                is_predefined=domain.get("is_predefined", False)
            )
            for domain in response.data
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取标签失败: {str(e)}")


@router.get("/paper/{paper_id}/domains")
async def get_paper_domains(paper_id: int, db: Client = Depends(get_db)) -> List[DomainResponse]:
    """获取论文的所有标签"""
    try:
        response = db.table("paper_domains") \
            .select("domain_id, domains(*)") \
            .eq("paper_id", paper_id) \
            .execute()

        domains = []
        for item in response.data:
            domain = item.get("domains")
            if domain:
                domains.append(DomainResponse(
                    id=domain["id"],
                    name=domain["name"],
                    color=domain["color"],
                    icon=domain.get("icon", "🏷️"),
                    description=domain.get("description"),
                    is_predefined=domain.get("is_predefined", False)
                ))

        return domains
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取论文标签失败: {str(e)}")


@router.post("/paper/add-domains")
async def add_domains_to_paper(request: AddDomainRequest, db: Client = Depends(get_db)):
    """为论文添加标签"""
    try:
        # 验证论文是否存在
        paper_response = db.table("papers").select("id").eq("id", request.paper_id).execute()
        if not paper_response.data:
            raise HTTPException(status_code=404, detail="论文不存在")

        # 批量添加标签（使用ON CONFLICT忽略重复）
        for domain_id in request.domain_ids:
            try:
                db.table("paper_domains").insert({
                    "paper_id": request.paper_id,
                    "domain_id": domain_id,
                    "confidence": 1.0
                }).execute()
            except Exception:
                # 忽略重复错误
                pass

        return {"success": True, "message": "标签添加成功"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"添加标签失败: {str(e)}")


@router.delete("/paper/remove-domain")
async def remove_domain_from_paper(
    paper_id: int,
    domain_id: int,
    db: Client = Depends(get_db)
):
    """从论文移除标签"""
    try:
        response = db.table("paper_domains") \
            .delete() \
            .eq("paper_id", paper_id) \
            .eq("domain_id", domain_id) \
            .execute()

        return {"success": True, "message": "标签已移除"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"移除标签失败: {str(e)}")


class CreateDomainRequest(BaseModel):
    """创建标签请求"""
    name: str
    color: str = "#6366f1"
    icon: str = "🏷️"
    description: Optional[str] = None


@router.post("/domains/create")
async def create_custom_domain(
    request: CreateDomainRequest,
    db: Client = Depends(get_db)
) -> DomainResponse:
    """创建自定义领域标签"""
    try:
        # 检查标签名是否已存在
        existing = db.table("domains").select("id").eq("name", request.name).execute()
        if existing.data:
            raise HTTPException(status_code=400, detail="标签名已存在")

        response = db.table("domains").insert({
            "name": request.name,
            "color": request.color,
            "icon": request.icon,
            "description": request.description,
            "is_predefined": False
        }).execute()

        if not response.data:
            raise HTTPException(status_code=500, detail="创建标签失败")

        domain = response.data[0]
        return DomainResponse(
            id=domain["id"],
            name=domain["name"],
            color=domain["color"],
            icon=domain.get("icon", "🏷️"),
            description=domain.get("description"),
            is_predefined=False
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建标签失败: {str(e)}")
