"""Vercel serverless function - 备用方案"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.main import app

# 方案A: 使用标准ASGI callable
async def handler(scope, receive, send):
    """ASGI3 handler"""
    await app(scope, receive, send)

# 方案B: 导出app
__all__ = ['app', 'handler']
