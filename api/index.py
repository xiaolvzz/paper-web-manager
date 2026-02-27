"""Vercel serverless function - 直接导出FastAPI ASGI应用"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 直接导入并导出FastAPI app
# Vercel的@vercel/python运行时会自动检测并运行ASGI应用
from backend.main import app

# Vercel会自动处理ASGI，不需要手动创建handler类
