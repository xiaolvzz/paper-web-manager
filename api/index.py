"""Vercel Serverless Function Entry Point"""
import sys
import os
import traceback

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# 尝试导入主应用
app = None
import_error = None

try:
    from backend.main import app as main_app

    # 配置根路径用于API路由
    main_app.root_path = "/api"
    app = main_app

except Exception as e:
    import_error = {
        "error": str(e),
        "traceback": traceback.format_exc(),
        "sys_path": sys.path,
        "project_root": project_root,
        "current_dir": os.getcwd(),
        "files": os.listdir(project_root) if os.path.exists(project_root) else []
    }

# 如果导入失败，创建错误响应app
if app is None:
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    from fastapi.middleware.cors import CORSMiddleware

    app = FastAPI()

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/api/{full_path:path}")
    async def error_handler(full_path: str):
        return JSONResponse(
            status_code=500,
            content={
                "error": "Backend initialization failed",
                "detail": import_error
            }
        )

    @app.post("/api/{full_path:path}")
    async def error_handler_post(full_path: str):
        return JSONResponse(
            status_code=500,
            content={
                "error": "Backend initialization failed",
                "detail": import_error
            }
        )

# Vercel handler
handler = app
