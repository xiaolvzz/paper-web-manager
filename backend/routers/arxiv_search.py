"""arXiv搜索API - 使用公开HTTP API"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
import logging
import requests
import re
from xml.etree import ElementTree as ET
from datetime import datetime

# 配置日志
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/arxiv", tags=["arxiv"])


def parse_arxiv_id_from_url(url: str) -> Optional[str]:
    """从arXiv URL中提取论文ID"""
    # 支持多种格式：
    # https://arxiv.org/abs/2301.12345
    # https://arxiv.org/pdf/2301.12345.pdf
    # http://arxiv.org/abs/2301.12345v1
    # 2301.12345
    patterns = [
        r'arxiv\.org/abs/(\d+\.\d+)',
        r'arxiv\.org/pdf/(\d+\.\d+)',
        r'^(\d+\.\d+)',
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None


def fetch_arxiv_metadata(arxiv_id: str) -> dict:
    """通过arXiv公开API获取论文元数据"""
    api_url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"

    try:
        logger.info(f"[fetch_metadata] Fetching from: {api_url}")
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()

        logger.info(f"[fetch_metadata] Response status: {response.status_code}")
        logger.debug(f"[fetch_metadata] Response content (first 500 chars): {response.content[:500]}")

        # 解析XML
        root = ET.fromstring(response.content)

        # arXiv API使用Atom命名空间
        ns = {
            'atom': 'http://www.w3.org/2005/Atom',
            'arxiv': 'http://arxiv.org/schemas/atom'
        }

        entry = root.find('atom:entry', ns)
        if entry is None:
            logger.error(f"[fetch_metadata] No entry found for arXiv ID: {arxiv_id}")
            logger.debug(f"[fetch_metadata] XML content: {ET.tostring(root, encoding='unicode')}")
            raise ValueError(f"论文未找到：arXiv ID {arxiv_id} 不存在或格式错误")

        # 提取信息
        title_elem = entry.find('atom:title', ns)
        if title_elem is None:
            raise ValueError("论文数据不完整：缺少标题")
        title = title_elem.text.strip().replace('\n', ' ')

        summary_elem = entry.find('atom:summary', ns)
        summary = summary_elem.text.strip().replace('\n', ' ') if summary_elem is not None else ""

        # 作者
        authors = []
        for author in entry.findall('atom:author', ns):
            name = author.find('atom:name', ns)
            if name is not None:
                authors.append(name.text)

        # 发布日期
        published_elem = entry.find('atom:published', ns)
        if published_elem is None:
            raise ValueError("论文数据不完整：缺少发布日期")
        published = published_elem.text
        published_date = datetime.fromisoformat(published.replace('Z', '+00:00'))

        # 分类
        categories = []
        for category in entry.findall('atom:category', ns):
            term = category.get('term')
            if term:
                categories.append(term)

        # PDF链接
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"

        result = {
            "arxiv_id": arxiv_id,
            "title": title,
            "authors": ", ".join(authors),
            "abstract": summary,
            "published": published_date.strftime("%Y-%m-%d"),
            "year": published_date.year,
            "pdf_url": pdf_url,
            "primary_category": categories[0] if categories else "",
            "categories": ", ".join(categories)
        }

        logger.info(f"[fetch_metadata] Successfully extracted: {title}")
        return result

    except requests.RequestException as e:
        logger.error(f"[fetch_metadata] Request failed for {arxiv_id}: {e}")
        raise HTTPException(status_code=500, detail=f"无法连接到arXiv API: {str(e)}")
    except ET.ParseError as e:
        logger.error(f"[fetch_metadata] XML parse error for {arxiv_id}: {e}")
        raise HTTPException(status_code=500, detail="解析arXiv响应失败")
    except ValueError as e:
        logger.error(f"[fetch_metadata] Value error for {arxiv_id}: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"[fetch_metadata] Unexpected error for {arxiv_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"获取论文信息失败: {str(e)}")


@router.get("/debug/{arxiv_id}")
async def debug_arxiv_id(arxiv_id: str):
    """调试端点：检查arXiv ID是否有效"""
    try:
        logger.info(f"[debug] Testing arXiv ID: {arxiv_id}")
        paper_data = fetch_arxiv_metadata(arxiv_id)
        return {
            "status": "success",
            "arxiv_id": arxiv_id,
            "paper": paper_data
        }
    except HTTPException as e:
        return {
            "status": "error",
            "arxiv_id": arxiv_id,
            "error": e.detail,
            "status_code": e.status_code
        }
    except Exception as e:
        return {
            "status": "error",
            "arxiv_id": arxiv_id,
            "error": str(e)
        }


@router.get("/health")
async def health_check():
    """检查arXiv服务状态"""
    try:
        # 测试API连接
        response = requests.get("http://export.arxiv.org/api/query?id_list=1706.03762", timeout=5)
        response.raise_for_status()
        return {
            "status": "ok",
            "message": "arXiv API连接正常"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"arXiv API连接失败: {str(e)}"
        }


@router.get("/search")
async def search_papers(
    query: str = Query(..., description="搜索关键词（标题、作者等）"),
    max_results: int = Query(10, ge=1, le=50, description="最多返回结果数")
):
    """
    从arXiv搜索论文（使用公开HTTP API）

    支持的搜索方式：
    - 论文标题：直接输入关键词
    - 作者：输入作者名
    - 使用高级查询语法：ti:title, au:author, abs:abstract
    """
    try:
        logger.info(f"Searching arXiv for: {query}")

        # 智能构建搜索查询
        if not any(prefix in query for prefix in ['ti:', 'au:', 'abs:', 'cat:', 'all:']):
            # 默认在标题和摘要中搜索
            search_query = f'all:{query}'
        else:
            search_query = query

        logger.info(f"Using search query: {search_query}")

        # 调用arXiv API
        api_url = f"http://export.arxiv.org/api/query?search_query={requests.utils.quote(search_query)}&start=0&max_results={max_results}&sortBy=relevance&sortOrder=descending"

        response = requests.get(api_url, timeout=15)
        response.raise_for_status()

        # 解析XML
        root = ET.fromstring(response.content)

        ns = {
            'atom': 'http://www.w3.org/2005/Atom',
            'arxiv': 'http://arxiv.org/schemas/atom'
        }

        results = []
        for entry in root.findall('atom:entry', ns):
            try:
                # 提取arXiv ID
                id_elem = entry.find('atom:id', ns)
                arxiv_id = id_elem.text.split('/')[-1] if id_elem is not None else ""

                # 标题
                title_elem = entry.find('atom:title', ns)
                title = title_elem.text.strip().replace('\n', ' ') if title_elem is not None else ""

                # 摘要
                summary_elem = entry.find('atom:summary', ns)
                summary = summary_elem.text.strip().replace('\n', ' ') if summary_elem is not None else ""

                # 作者
                authors = []
                for author in entry.findall('atom:author', ns):
                    name = author.find('atom:name', ns)
                    if name is not None:
                        authors.append(name.text)

                # 发布日期
                published_elem = entry.find('atom:published', ns)
                if published_elem is not None:
                    published_date = datetime.fromisoformat(published_elem.text.replace('Z', '+00:00'))
                    published = published_date.strftime("%Y-%m-%d")
                    year = published_date.year
                else:
                    published = ""
                    year = 0

                # 分类
                categories = []
                for category in entry.findall('atom:category', ns):
                    term = category.get('term')
                    if term:
                        categories.append(term)

                # PDF链接
                pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"

                results.append({
                    "arxiv_id": arxiv_id,
                    "title": title,
                    "authors": ", ".join(authors),
                    "abstract": summary,
                    "published": published,
                    "year": year,
                    "pdf_url": pdf_url,
                    "primary_category": categories[0] if categories else "",
                    "categories": ", ".join(categories)
                })
            except Exception as e:
                logger.warning(f"Failed to parse entry: {e}")
                continue

        logger.info(f"Found {len(results)} papers")

        return {
            "query": query,
            "search_query": search_query,
            "count": len(results),
            "results": results
        }

    except requests.RequestException as e:
        logger.error(f"Request error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"无法连接到arXiv API: {str(e)}"
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
    try:
        logger.info(f"Getting paper by ID: {arxiv_id}")
        return fetch_arxiv_metadata(arxiv_id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting paper: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"获取论文失败: {str(e)}"
        )


@router.post("/from-pdf-url")
async def add_paper_from_pdf_url(pdf_url: str = Query(..., description="arXiv PDF URL")):
    """
    从PDF URL自动提取论文信息并返回

    支持的URL格式：
    - https://arxiv.org/pdf/2301.12345.pdf
    - https://arxiv.org/abs/2301.12345
    - 2301.12345
    """
    try:
        logger.info(f"[from-pdf-url] Step 1: Received PDF URL: {pdf_url}")

        # 提取arXiv ID
        arxiv_id = parse_arxiv_id_from_url(pdf_url)
        logger.info(f"[from-pdf-url] Step 2: Extracted arXiv ID: {arxiv_id}")

        if not arxiv_id:
            logger.error(f"[from-pdf-url] Failed to extract arXiv ID from: {pdf_url}")
            raise HTTPException(
                status_code=400,
                detail=f"无法从URL中提取arXiv ID，请检查URL格式。输入: {pdf_url}"
            )

        # 获取元数据
        logger.info(f"[from-pdf-url] Step 3: Fetching metadata for arXiv ID: {arxiv_id}")
        paper_data = fetch_arxiv_metadata(arxiv_id)
        logger.info(f"[from-pdf-url] Step 4: Successfully fetched metadata: {paper_data.get('title', 'Unknown')}")

        return {
            "success": True,
            "message": "成功获取论文信息",
            "paper": paper_data
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[from-pdf-url] Error extracting paper from {pdf_url}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"提取论文信息失败: {str(e)}"
        )
