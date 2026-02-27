"""Vercel serverless function - 直接导出FastAPI应用"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入FastAPI应用并直接导出
# Vercel会自动识别并处理ASGI应用
from backend.main import app

# Vercel原生ASGI支持 - 不需要Mangum
__all__ = ['app']
