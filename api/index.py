"""Vercel Serverless Function Entry Point"""
import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

try:
    from backend.main import app

    # Vercel需要的handler
    app.root_path = "/api"
    handler = app

except Exception as e:
    # 如果导入失败，创建一个简单的错误响应
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse

    error_app = FastAPI()

    @error_app.get("/{full_path:path}")
    async def error_handler(full_path: str):
        return JSONResponse(
            status_code=500,
            content={
                "error": "Backend initialization failed",
                "detail": str(e),
                "path": full_path
            }
        )

    handler = error_app
