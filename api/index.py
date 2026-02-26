"""Vercel Serverless Function Entry Point"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# 创建基础app
app = FastAPI(title="论文管理系统API")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 尝试导入backend模块
backend_loaded = False
backend_error = None

try:
    from backend.routers import papers, analysis, relations, arxiv_search

    # 注册路由
    app.include_router(papers.router)
    app.include_router(analysis.router)
    app.include_router(relations.router)
    app.include_router(arxiv_search.router)

    backend_loaded = True

except Exception as e:
    backend_error = str(e)
    import traceback
    backend_traceback = traceback.format_exc()

    # 添加错误端点
    @app.get("/api/error-info")
    async def error_info():
        return JSONResponse(
            status_code=500,
            content={
                "backend_loaded": False,
                "error": backend_error,
                "traceback": backend_traceback,
                "sys_path": sys.path,
                "project_root": project_root
            }
        )

# 健康检查端点
@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy" if backend_loaded else "degraded",
        "backend_loaded": backend_loaded,
        "backend_error": backend_error if not backend_loaded else None,
        "environment": "vercel",
        "python_version": sys.version
    }

# 通用错误处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc),
            "path": request.url.path
        }
    )

# Vercel需要的handler
handler = app
