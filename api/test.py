"""最小化测试 - 验证基础功能"""
from fastapi import FastAPI
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

@app.get("/api/test")
async def test():
    return {"status": "ok", "message": "Test endpoint working"}

@app.get("/api/health")
async def health():
    return {"status": "healthy", "message": "Minimal test app"}

handler = app
