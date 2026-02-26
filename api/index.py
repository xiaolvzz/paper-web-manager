from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# 添加项目根目录
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 导入路由
try:
    from backend.routers import papers, analysis, relations, arxiv_search

    app.include_router(papers.router)
    app.include_router(analysis.router)
    app.include_router(relations.router)
    app.include_router(arxiv_search.router)

    status = "loaded"
except Exception as e:
    status = f"error: {e}"

@app.get("/api/health")
def health():
    return {"status": "ok", "backend": status}
