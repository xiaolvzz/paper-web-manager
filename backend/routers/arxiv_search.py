"""arXiv搜索API"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
import arxiv

router = APIRouter(prefix="/api/arxiv", tags=["arxiv"])


@router.get("/search")
async def search_papers(
    query: str = Query(..., description="搜索关键词（标题、作者等）"),
    max_results: int = Query(10, ge=1, le=50, description="最多返回结果数")
):
    """
    从arXiv搜索论文

    支持的搜索方式：
    - 论文标题：直接输入关键词
    - 作者：输入作者名
    - 精确标题：用引号括起来 "exact title"
    """
    try:
        # 构建搜索
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance,
            sort_order=arxiv.SortOrder.Descending
        )

        # 获取结果
        results = []
        for paper in search.results():
            results.append({
                "arxiv_id": paper.entry_id.split('/')[-1],  # 提取ID
                "title": paper.title,
                "authors": ", ".join([author.name for author in paper.authors]),
                "abstract": paper.summary,
                "published": paper.published.strftime("%Y-%m-%d"),
                "year": paper.published.year,
                "pdf_url": paper.pdf_url,
                "primary_category": paper.primary_category,
                "categories": ", ".join(paper.categories)
            })

        return {
            "query": query,
            "count": len(results),
            "results": results
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"arXiv搜索失败: {str(e)}"
        )


@router.get("/paper/{arxiv_id}")
async def get_paper_by_id(arxiv_id: str):
    """
    通过arXiv ID获取论文详情

    示例ID: 2301.12345 或 1706.03762
    """
    try:
        # 构建完整的arXiv URL
        if not arxiv_id.startswith('http'):
            arxiv_id = f"http://arxiv.org/abs/{arxiv_id}"

        # 搜索
        search = arxiv.Search(id_list=[arxiv_id])
        paper = next(search.results())

        return {
            "arxiv_id": paper.entry_id.split('/')[-1],
            "title": paper.title,
            "authors": ", ".join([author.name for author in paper.authors]),
            "abstract": paper.summary,
            "published": paper.published.strftime("%Y-%m-%d"),
            "year": paper.published.year,
            "pdf_url": paper.pdf_url,
            "primary_category": paper.primary_category,
            "categories": ", ".join(paper.categories)
        }

    except StopIteration:
        raise HTTPException(status_code=404, detail="论文未找到")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取论文失败: {str(e)}"
        )
