"""Vercel Serverless Function Entry Point"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from backend.main import app

# Vercel需要的handler
handler = app
