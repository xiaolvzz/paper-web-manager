"""Vercel serverless function entry point"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入FastAPI应用
from backend.main import app

# 使用Mangum将ASGI应用转换为Vercel兼容的handler
from mangum import Mangum

# Vercel需要的handler
handler = Mangum(app, lifespan="off")
