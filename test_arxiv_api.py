#!/usr/bin/env python3
"""测试arXiv API"""
import requests
import re
from xml.etree import ElementTree as ET
from datetime import datetime

def parse_arxiv_id_from_url(url: str):
    """从arXiv URL中提取论文ID"""
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

def fetch_arxiv_metadata(arxiv_id: str):
    """通过arXiv公开API获取论文元数据"""
    api_url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"

    print(f"\n{'='*60}")
    print(f"测试arXiv ID: {arxiv_id}")
    print(f"API URL: {api_url}")
    print(f"{'='*60}\n")

    try:
        response = requests.get(api_url, timeout=10)
        print(f"✓ HTTP状态码: {response.status_code}")

        # 解析XML
        root = ET.fromstring(response.content)

        # arXiv API使用Atom命名空间
        ns = {
            'atom': 'http://www.w3.org/2005/Atom',
            'arxiv': 'http://arxiv.org/schemas/atom'
        }

        entry = root.find('atom:entry', ns)
        if entry is None:
            print(f"\n❌ 错误: 论文未找到")
            print(f"   arXiv ID '{arxiv_id}' 不存在或格式错误")
            print(f"\n提示: 请在arXiv网站搜索论文并复制正确的ID")
            return None

        # 提取信息
        title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
        summary = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')

        # 作者
        authors = []
        for author in entry.findall('atom:author', ns):
            name = author.find('atom:name', ns)
            if name is not None:
                authors.append(name.text)

        # 发布日期
        published = entry.find('atom:published', ns).text
        published_date = datetime.fromisoformat(published.replace('Z', '+00:00'))

        # 分类
        categories = []
        for category in entry.findall('atom:category', ns):
            term = category.get('term')
            if term:
                categories.append(term)

        result = {
            "arxiv_id": arxiv_id,
            "title": title,
            "authors": ", ".join(authors),
            "abstract": summary[:200] + "...",
            "published": published_date.strftime("%Y-%m-%d"),
            "year": published_date.year,
            "pdf_url": f"https://arxiv.org/pdf/{arxiv_id}.pdf",
            "categories": ", ".join(categories)
        }

        print(f"✓ 论文找到！\n")
        print(f"标题: {result['title']}")
        print(f"作者: {result['authors']}")
        print(f"年份: {result['year']}")
        print(f"分类: {result['categories']}")
        print(f"摘要: {result['abstract']}")
        print(f"PDF: {result['pdf_url']}")

        return result

    except requests.RequestException as e:
        print(f"❌ 网络错误: {e}")
        return None
    except Exception as e:
        print(f"❌ 解析错误: {e}")
        return None

if __name__ == "__main__":
    # 测试用户提供的ID
    print("\n" + "="*60)
    print("测试1: 用户提供的arXiv ID")
    print("="*60)
    user_id = "2602.06521"
    fetch_arxiv_metadata(user_id)

    # 测试已知存在的ID
    print("\n\n" + "="*60)
    print("测试2: 已知存在的论文 (Attention Is All You Need)")
    print("="*60)
    test_id = "1706.03762"
    fetch_arxiv_metadata(test_id)

    # 测试URL解析
    print("\n\n" + "="*60)
    print("测试3: URL解析功能")
    print("="*60)
    test_urls = [
        "https://arxiv.org/pdf/2602.06521",
        "https://arxiv.org/abs/1706.03762",
        "2301.12345"
    ]
    for url in test_urls:
        arxiv_id = parse_arxiv_id_from_url(url)
        print(f"URL: {url:50} → ID: {arxiv_id}")
