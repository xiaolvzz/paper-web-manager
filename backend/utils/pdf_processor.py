"""PDF处理工具"""
import os
import tempfile
from typing import Tuple
from fastapi import UploadFile, HTTPException

# 尝试导入PyMuPDF，如果失败则禁用PDF功能
try:
    import fitz  # PyMuPDF
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    fitz = None


def extract_text_from_pdf(pdf_file_path: str) -> str:
    """
    从PDF文件中提取文本

    Args:
        pdf_file_path: PDF文件路径

    Returns:
        提取的文本内容
    """
    if not PDF_AVAILABLE:
        raise Exception("PDF处理功能在当前环境不可用（PyMuPDF未安装）")

    try:
        doc = fitz.open(pdf_file_path)
        text_content = []

        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            text_content.append(text)

        doc.close()

        return "\n\n".join(text_content)

    except Exception as e:
        raise Exception(f"PDF解析失败: {str(e)}")


async def process_uploaded_pdf(file: UploadFile) -> Tuple[bytes, str]:
    """
    处理上传的PDF文件

    Args:
        file: FastAPI UploadFile对象

    Returns:
        (file_bytes, extracted_text) 元组
    """
    # 验证文件类型
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="只支持PDF文件")

    # 读取文件内容
    file_bytes = await file.read()

    # 检查文件大小（限制50MB）
    max_size = 50 * 1024 * 1024  # 50MB
    if len(file_bytes) > max_size:
        raise HTTPException(status_code=400, detail="PDF文件过大，最大支持50MB")

    # 保存到临时文件进行解析
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        tmp_file.write(file_bytes)
        tmp_file_path = tmp_file.name

    try:
        # 提取文本
        extracted_text = extract_text_from_pdf(tmp_file_path)

        if not extracted_text or len(extracted_text.strip()) < 100:
            raise HTTPException(
                status_code=400,
                detail="PDF文本提取失败或内容过少，可能是扫描版PDF或加密PDF"
            )

        return file_bytes, extracted_text

    finally:
        # 删除临时文件
        if os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)


def upload_pdf_to_supabase(supabase_client, file_bytes: bytes, file_name: str, paper_id: int) -> str:
    """
    上传PDF文件到Supabase Storage

    Args:
        supabase_client: Supabase客户端
        file_bytes: PDF文件字节
        file_name: 文件名
        paper_id: 论文ID

    Returns:
        存储路径
    """
    # 构建存储路径
    storage_path = f"papers/{paper_id}/{file_name}"

    try:
        # 上传到Supabase Storage（假设存储桶名为paper-pdfs）
        # 注意：需要先在Supabase中创建paper-pdfs存储桶
        response = supabase_client.storage.from_('paper-pdfs').upload(
            path=storage_path,
            file=file_bytes,
            file_options={"content-type": "application/pdf"}
        )

        return storage_path

    except Exception as e:
        # 如果上传失败，可能是文件已存在，尝试更新
        try:
            supabase_client.storage.from_('paper-pdfs').update(
                path=storage_path,
                file=file_bytes,
                file_options={"content-type": "application/pdf"}
            )
            return storage_path
        except Exception as e2:
            raise Exception(f"上传PDF到云端失败: {str(e2)}")
