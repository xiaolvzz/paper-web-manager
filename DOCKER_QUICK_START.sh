#!/bin/bash
# Docker快速启动脚本

echo "🚀 论文管理系统 - Docker启动"
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    echo "访问: https://www.docker.com/products/docker-desktop"
    exit 1
fi

echo "✅ Docker已安装"
echo ""

# 配置环境变量
export SUPABASE_URL="https://wlslekyepjebnzjmslld.supabase.co"
export SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Indsc2xla3llcGplYm56am1zbGxkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzIwNjIwNTksImV4cCI6MjA4NzYzODA1OX0.Yuq7u2woJAdrnh2RLs06Vi8IObe52FaHMsRqHTRQ14M"

echo "📦 构建Docker镜像..."
docker build -t paper-manager .

echo ""
echo "🚀 启动容器..."
docker run -d \
  -p 8000:8000 \
  -e SUPABASE_URL="$SUPABASE_URL" \
  -e SUPABASE_KEY="$SUPABASE_KEY" \
  --name paper-manager \
  paper-manager

echo ""
echo "✅ 启动成功！"
echo ""
echo "🌐 访问地址: http://localhost:8000"
echo ""
echo "📝 常用命令:"
echo "  查看日志: docker logs -f paper-manager"
echo "  停止服务: docker stop paper-manager"
echo "  启动服务: docker start paper-manager"
echo "  删除容器: docker rm -f paper-manager"
echo ""
