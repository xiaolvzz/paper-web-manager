"""arXiv搜索API"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
import logging

# 配置日志
logger = logging.getLogger(__name__)

try:
    import arxiv
    ARXIV_AVAILABLE = True
except ImportError as e:
    logger.error(f"Failed to import arxiv: {e}")
    ARXIV_AVAILABLE = False

router = APIRouter(prefix="/api/arxiv", tags=["arxiv"])


@router.get("/health")
async def health_check():
    """检查arXiv服务状态"""
    return {
        "status": "ok" if ARXIV_AVAILABLE else "error",
        "arxiv_available": ARXIV_AVAILABLE,
        "message": "arXiv库已加载" if ARXIV_AVAILABLE else "arXiv库未安装或导入失败"
    }


@router.get("/search")
async def search_papers(
    query: str = Query(..., description="搜索关键词（标题、作者等）"),
    max_results: int = Query(10, ge=1, le=50, description="最多返回结果数")
):
    """
    从arXiv搜索论文

    支持的搜索方式：
    - 论文标题：直接输入关键词（会自动在标题中搜索）
    - 作者：输入作者名
    - 精确标题：用引号括起来 "exact title"
    """
    # 检查arxiv库是否可用
    if not ARXIV_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="arXiv库未安装或导入失败，请联系管理员"
        )

    try:
        logger.info(f"Searching arXiv for: {query}")

        # 智能构建搜索查询
        # 如果用户没有指定搜索字段，默认在标题和摘要中搜索
        if not any(prefix in query for prefix in ['ti:', 'au:', 'abs:', 'cat:', 'all:']):
            # 尝试多种搜索策略：标题搜索 OR 摘要搜索 OR 全文搜索
            search_query = f'ti:{query} OR abs:{query} OR all:{query}'
        else:
            search_query = query

        logger.info(f"Using search query: {search_query}")

        # 构建搜索，增加返回数量以提高匹配率
        search = arxiv.Search(
            query=search_query,
            max_results=max_results * 2,  # 获取更多结果后再过滤
            sort_by=arxiv.SortCriterion.Relevance,
            sort_order=arxiv.SortOrder.Descending
        )

        # 获取结果
        results = []
        count = 0
        for paper in search.results():
            # 限制返回数量
            if count >= max_results:
                break

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
            count += 1

        logger.info(f"Found {len(results)} papers")

        return {
            "query": query,
            "search_query": search_query,  # 返回实际使用的查询
            "count": len(results),
            "results": results
        }

    except ImportError as e:
        logger.error(f"Import error: {e}")
        raise HTTPException(
            status_code=503,
            detail=f"arXiv库导入失败: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Search error: {e}", exc_info=True)
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
    # 检查arxiv库是否可用
    if not ARXIV_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="arXiv库未安装或导入失败，请联系管理员"
        )

    try:
        logger.info(f"Getting paper by ID: {arxiv_id}")

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
        logger.warning(f"Paper not found: {arxiv_id}")
        raise HTTPException(status_code=404, detail="论文未找到")
    except Exception as e:
        logger.error(f"Error getting paper: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"获取论文失败: {str(e)}"
        )
