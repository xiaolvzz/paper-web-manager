"""arXiv集成工具"""
import arxiv
import re
import tempfile
import os
from typing import Dict, Optional
from fastapi import HTTPException

from .pdf_processor import extract_text_from_pdf


def extract_arxiv_id(input_str: str) -> str:
    """
    从输入中提取arXiv ID

    支持格式：
    - 2301.12345
    - arXiv:2301.12345
    - https://arxiv.org/abs/2301.12345
    - https://arxiv.org/pdf/2301.12345.pdf
    """
    # 正则匹配arXiv ID格式
    pattern = r'(\d{4}\.\d{4,5})'
    match = re.search(pattern, input_str)

    if match:
        return match.group(1)
    else:
        raise HTTPException(
            status_code=400,
            detail="无效的arXiv ID格式。请输入如：2301.12345 或 https://arxiv.org/abs/2301.12345"
        )


async def fetch_arxiv_paper(arxiv_input: str) -> Dict:
    """
    从arXiv获取论文信息

    Args:
        arxiv_input: arXiv ID或URL

    Returns:
        包含论文元数据和PDF文本的字典
    """
    # 提取arXiv ID
    arxiv_id = extract_arxiv_id(arxiv_input)

    try:
        # 使用arxiv库搜索论文
        search = arxiv.Search(id_list=[arxiv_id])
        paper = next(search.results())

        # 获取元数据
        paper_data = {
            "arxiv_id": arxiv_id,
            "title": paper.title,
            "authors": ", ".join([author.name for author in paper.authors]),
            "year": paper.published.year,
            "abstract": paper.summary,
            "pdf_url": paper.pdf_url,
            "arxiv_url": f"https://arxiv.org/abs/{arxiv_id}"
        }

        # 下载PDF并提取文本
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_pdf_path = tmp_file.name

        try:
            # 下载PDF
            paper.download_pdf(filename=tmp_pdf_path)

            # 提取文本
            pdf_text = extract_text_from_pdf(tmp_pdf_path)
            paper_data["pdf_text_content"] = pdf_text

        except Exception as e:
            # PDF下载或解析失败不影响元数据
            paper_data["pdf_text_content"] = None
            paper_data["error"] = f"PDF下载失败: {str(e)}"

        finally:
            # 删除临时文件
            if os.path.exists(tmp_pdf_path):
                os.unlink(tmp_pdf_path)

        return paper_data

    except StopIteration:
        raise HTTPException(
            status_code=404,
            detail=f"未找到arXiv论文: {arxiv_id}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取arXiv论文失败: {str(e)}"
        )


def is_arxiv_url(url: str) -> bool:
    """判断是否为arXiv URL"""
    return 'arxiv.org' in url.lower()
