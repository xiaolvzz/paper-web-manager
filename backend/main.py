"""FastAPI主应用"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

from backend.routers import papers, analysis, relations, arxiv_search, ai_assistant, conversations, translation, code_analysis, domains, code_notes

# 创建FastAPI应用
app = FastAPI(
    title="论文管理系统",
    description="个人论文阅读和管理系统，支持关联关系、AI分析和翻译",
    version="1.3.0",
    root_path="/api"  # Vercel部署时所有路由都在/api下
)

# CORS配置（开发环境）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该设置具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(papers.router)
app.include_router(analysis.router)
app.include_router(relations.router)
app.include_router(arxiv_search.router)
app.include_router(ai_assistant.router)
app.include_router(conversations.router)
app.include_router(translation.router)
app.include_router(code_analysis.router)
app.include_router(domains.router)
app.include_router(code_notes.router)

# 检测是否在Vercel环境中
IS_VERCEL = os.getenv("VERCEL", False)

# 只在非Vercel环境中挂载静态文件
if not IS_VERCEL:
    # 挂载静态文件（本地开发环境）
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
    try:
        app.mount("/assets", StaticFiles(directory=os.path.join(frontend_path, "assets")), name="assets")

        @app.get("/")
        async def root():
            """首页"""
            return FileResponse(os.path.join(frontend_path, "index.html"))

        @app.get("/paper/{paper_id}")
        async def paper_page(paper_id: int):
            """论文详情页"""
            return FileResponse(os.path.join(frontend_path, "paper.html"))

        @app.get("/graph")
        async def graph_page():
            """关系图页面"""
            return FileResponse(os.path.join(frontend_path, "graph.html"))
    except Exception as e:
        print(f"Warning: Could not mount static files: {e}")


@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "message": "论文管理系统运行正常",
        "environment": "vercel" if IS_VERCEL else "local"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
