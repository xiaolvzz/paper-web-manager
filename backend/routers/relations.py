"""论文关联关系管理API"""
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from supabase import Client
from backend.database import get_db
from backend.models import Relation, RelationCreate

router = APIRouter(prefix="/relations", tags=["relations"])


@router.get("/", response_model=List[Relation])
async def get_all_relations(db: Client = Depends(get_db)):
    """获取所有关联关系"""
    try:
        response = db.table("relations").select("*").execute()
        return response.data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取关联关系失败: {str(e)}")


@router.get("/paper/{paper_id}")
async def get_paper_relations(paper_id: int, db: Client = Depends(get_db)):
    """获取论文的所有关联关系（包含关联论文的信息）"""
    try:
        # 获取该论文相关的所有关系
        response = db.table("relations").select("*").or_(
            f"paper_from_id.eq.{paper_id},paper_to_id.eq.{paper_id}"
        ).execute()

        relations = response.data

        # 获取所有关联论文的ID
        paper_ids = set()
        for rel in relations:
            paper_ids.add(rel["paper_from_id"])
            paper_ids.add(rel["paper_to_id"])
        paper_ids.discard(paper_id)  # 排除自己

        # 如果有关联论文，批量获取信息
        related_papers = {}
        if paper_ids:
            papers_response = db.table("papers").select("*").in_("id", list(paper_ids)).execute()
            related_papers = {p["id"]: p for p in papers_response.data}

        # 组装结果
        result = []
        for rel in relations:
            rel_with_papers = rel.copy()
            if rel["paper_from_id"] == paper_id:
                rel_with_papers["related_paper"] = related_papers.get(rel["paper_to_id"])
                rel_with_papers["direction"] = "outgoing"
            else:
                rel_with_papers["related_paper"] = related_papers.get(rel["paper_from_id"])
                rel_with_papers["direction"] = "incoming"
            result.append(rel_with_papers)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取论文关联关系失败: {str(e)}")


@router.post("/", response_model=Relation, status_code=201)
async def create_relation(relation: RelationCreate, db: Client = Depends(get_db)):
    """创建关联关系"""
    try:
        # 验证论文存在
        from_paper = db.table("papers").select("id").eq("id", relation.paper_from_id).execute()
        to_paper = db.table("papers").select("id").eq("id", relation.paper_to_id).execute()

        if not from_paper.data:
            raise HTTPException(status_code=404, detail=f"源论文 {relation.paper_from_id} 不存在")
        if not to_paper.data:
            raise HTTPException(status_code=404, detail=f"目标论文 {relation.paper_to_id} 不存在")

        # 验证不能自己关联自己
        if relation.paper_from_id == relation.paper_to_id:
            raise HTTPException(status_code=400, detail="论文不能关联自己")

        # 创建关系
        response = db.table("relations").insert(relation.model_dump()).execute()

        if not response.data:
            raise HTTPException(status_code=400, detail="创建关联关系失败，可能已存在相同关系")

        return response.data[0]

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建关联关系失败: {str(e)}")


@router.delete("/{relation_id}", status_code=204)
async def delete_relation(relation_id: int, db: Client = Depends(get_db)):
    """删除关联关系"""
    try:
        response = db.table("relations").delete().eq("id", relation_id).execute()

        if not response.data:
            raise HTTPException(status_code=404, detail="关联关系不存在")

        return None

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除关联关系失败: {str(e)}")


@router.get("/graph")
async def get_relation_graph(db: Client = Depends(get_db)):
    """获取关系图数据（用于可视化）"""
    try:
        # 获取所有论文
        papers_response = db.table("papers").select("id, title, year, tags").execute()
        papers = papers_response.data

        # 获取所有关系
        relations_response = db.table("relations").select("*").execute()
        relations = relations_response.data

        # 构建图数据（nodes和edges）
        nodes = [
            {
                "id": p["id"],
                "label": p["title"][:50] + "..." if len(p["title"]) > 50 else p["title"],
                "title": p["title"],  # 完整标题（悬停显示）
                "year": p["year"],
                "tags": p["tags"]
            }
            for p in papers
        ]

        edges = [
            {
                "from": r["paper_from_id"],
                "to": r["paper_to_id"],
                "label": r["relation_type"],
                "title": r["description"] or r["relation_type"]
            }
            for r in relations
        ]

        return {"nodes": nodes, "edges": edges}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取关系图数据失败: {str(e)}")
