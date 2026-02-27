"""Vercel serverless function - 使用Mangum适配器"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入FastAPI应用
from backend.main import app

# 使用Mangum将ASGI应用适配到Serverless Functions
from mangum import Mangum

# Vercel会调用这个handler
handler = Mangum(app, lifespan="off")
