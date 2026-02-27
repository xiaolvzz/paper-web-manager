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
async def get_relation_graph(
    domain_filter: str = None,
    relation_type_filter: str = None,
    db: Client = Depends(get_db)
):
    """获取关系图数据（用于可视化）

    Args:
        domain_filter: 按领域筛选（领域名称）
        relation_type_filter: 按关系类型筛选
    """
    try:
        # 获取所有论文
        papers_response = db.table("papers").select("id, title, year, tags, authors").execute()
        papers = papers_response.data

        # 获取所有论文的领域标签
        paper_domains_response = db.table("paper_domains").select(
            "paper_id, domains(id, name, color, icon)"
        ).execute()

        # 构建论文ID -> 领域列表的映射
        paper_domains_map = {}
        for item in paper_domains_response.data:
            paper_id = item["paper_id"]
            domain_info = item.get("domains")
            if domain_info:
                if paper_id not in paper_domains_map:
                    paper_domains_map[paper_id] = []
                paper_domains_map[paper_id].append(domain_info)

        # 如果指定了领域筛选，只保留该领域的论文
        if domain_filter:
            filtered_paper_ids = set()
            for paper_id, domains in paper_domains_map.items():
                if any(d["name"] == domain_filter for d in domains):
                    filtered_paper_ids.add(paper_id)
            papers = [p for p in papers if p["id"] in filtered_paper_ids]

        # 获取所有关系
        relations_response = db.table("relations").select("*").execute()
        relations = relations_response.data

        # 如果指定了关系类型筛选
        if relation_type_filter:
            relations = [r for r in relations if r["relation_type"] == relation_type_filter]

        # 只保留有效的关系（两端论文都存在）
        paper_ids_set = {p["id"] for p in papers}
        relations = [
            r for r in relations
            if r["paper_from_id"] in paper_ids_set and r["paper_to_id"] in paper_ids_set
        ]

        # 构建图数据（nodes和edges）
        nodes = []
        for p in papers:
            # 获取该论文的领域
            domains = paper_domains_map.get(p["id"], [])

            # 确定节点颜色（使用第一个领域的颜色）
            node_color = domains[0]["color"] if domains else "#6366f1"

            # 构建悬停提示
            hover_text = f"{p['title']}\n{p.get('year', '未知年份')}"
            if p.get("authors"):
                hover_text += f"\n作者: {p['authors'][:100]}"
            if domains:
                domain_names = ", ".join([d["name"] for d in domains])
                hover_text += f"\n领域: {domain_names}"

            nodes.append({
                "id": p["id"],
                "label": p["title"][:40] + "..." if len(p["title"]) > 40 else p["title"],
                "title": hover_text,
                "year": p["year"],
                "tags": p["tags"],
                "domains": domains,
                "color": node_color
            })

        edges = [
            {
                "from": r["paper_from_id"],
                "to": r["paper_to_id"],
                "label": r["relation_type"],
                "title": r["description"] or r["relation_type"],
                "relation_id": r["id"]
            }
            for r in relations
        ]

        # 获取所有可用的领域（用于筛选器）
        all_domains_response = db.table("domains").select("name, color, icon").execute()
        available_domains = all_domains_response.data

        # 统计关系类型
        relation_types = {}
        for r in db.table("relations").select("relation_type").execute().data:
            rt = r["relation_type"]
            relation_types[rt] = relation_types.get(rt, 0) + 1

        return {
            "nodes": nodes,
            "edges": edges,
            "available_domains": available_domains,
            "relation_types": relation_types
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取关系图数据失败: {str(e)}")
