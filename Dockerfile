# Python 3.10基础镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 复制requirements
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir fastapi==0.109.0 uvicorn[standard]==0.27.0 \
    python-dotenv==1.0.0 supabase==2.3.4 pydantic==2.5.3 python-multipart==0.0.6

# 复制项目文件
COPY backend ./backend
COPY frontend ./frontend
COPY .env .env

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
