"""Vercel serverless function - uvicorn方式"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入app
from backend.main import app

# 使用mangum作为ASGI到Lambda/Vercel的桥接
try:
    from mangum import Mangum
    handler = Mangum(app, lifespan="off", api_gateway_base_path="/api")
except ImportError:
    # 如果mangum不可用，直接导出app
    handler = app

# 同时导出app供Vercel直接使用
__all__ = ['app', 'handler']
