"""FastAPI主应用"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

from backend.routers import papers, analysis, relations, arxiv_search

# 创建FastAPI应用
app = FastAPI(
    title="论文管理系统",
    description="个人论文阅读和管理系统，支持关联关系和AI分析",
    version="1.0.0"
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

# 挂载静态文件
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
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


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "message": "论文管理系统运行正常"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
