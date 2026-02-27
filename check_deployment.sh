#!/bin/bash
# 快速检查Vercel部署状态

echo "🔍 论文管理系统部署诊断工具"
echo "================================"
echo ""

# 检查Vercel URL
read -p "请输入你的Vercel URL（如 https://paper-web-manager.vercel.app）: " VERCEL_URL

# 去除末尾的斜杠
VERCEL_URL=${VERCEL_URL%/}

echo ""
echo "开始测试 $VERCEL_URL ..."
echo ""

# 测试1: 健康检查
echo "📍 测试1: 健康检查 (/api/health)"
response=$(curl -s -w "\nHTTP_CODE:%{http_code}" "$VERCEL_URL/api/health")
http_code=$(echo "$response" | grep "HTTP_CODE" | cut -d: -f2)
body=$(echo "$response" | sed '/HTTP_CODE/d')

if [ "$http_code" = "200" ]; then
    echo "✅ 成功 (200)"
    echo "$body" | python3 -m json.tool 2>/dev/null || echo "$body"
else
    echo "❌ 失败 (HTTP $http_code)"
    echo "$body"
fi
echo ""

# 测试2: 论文列表
echo "📍 测试2: 获取论文列表 (/api/papers)"
response=$(curl -s -w "\nHTTP_CODE:%{http_code}" "$VERCEL_URL/api/papers")
http_code=$(echo "$response" | grep "HTTP_CODE" | cut -d: -f2)
body=$(echo "$response" | sed '/HTTP_CODE/d')

if [ "$http_code" = "200" ]; then
    # 检查是否是JSON
    if echo "$body" | python3 -c "import sys, json; json.load(sys.stdin)" 2>/dev/null; then
        echo "✅ 成功 (200) - 返回JSON"
        paper_count=$(echo "$body" | python3 -c "import sys, json; print(len(json.load(sys.stdin)))")
        echo "论文数量: $paper_count"
    else
        echo "⚠️  返回200但不是JSON格式"
        echo "响应内容（前200字符）:"
        echo "$body" | head -c 200
    fi
else
    echo "❌ 失败 (HTTP $http_code)"
    echo "$body" | head -c 500
fi
echo ""

# 测试3: AI健康检查
echo "📍 测试3: AI服务健康检查 (/api/ai/health)"
response=$(curl -s -w "\nHTTP_CODE:%{http_code}" "$VERCEL_URL/api/ai/health")
http_code=$(echo "$response" | grep "HTTP_CODE" | cut -d: -f2)
body=$(echo "$response" | sed '/HTTP_CODE/d')

if [ "$http_code" = "200" ]; then
    echo "✅ 成功 (200)"
    echo "$body" | python3 -m json.tool 2>/dev/null || echo "$body"
else
    echo "❌ 失败 (HTTP $http_code)"
    echo "$body"
fi
echo ""

# 测试4: 创建论文（POST）
echo "📍 测试4: 创建论文 (POST /api/papers/)"
response=$(curl -s -w "\nHTTP_CODE:%{http_code}" -X POST "$VERCEL_URL/api/papers/" \
    -H "Content-Type: application/json" \
    -d '{"title":"Test Paper from Diagnostic","authors":"Claude","year":2026,"domain":"AI","github_url":"https://github.com/test/test"}')
http_code=$(echo "$response" | grep "HTTP_CODE" | cut -d: -f2)
body=$(echo "$response" | sed '/HTTP_CODE/d')

if [ "$http_code" = "201" ] || [ "$http_code" = "200" ]; then
    echo "✅ 成功 (HTTP $http_code)"
    created_id=$(echo "$body" | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', 'unknown'))" 2>/dev/null)
    echo "创建的论文ID: $created_id"

    # 清理测试数据
    if [ "$created_id" != "unknown" ] && [ "$created_id" != "" ]; then
        echo "🧹 清理测试数据..."
        curl -s -X DELETE "$VERCEL_URL/api/papers/$created_id" > /dev/null
        echo "测试论文已删除"
    fi
else
    echo "❌ 失败 (HTTP $http_code)"
    echo "$body" | head -c 500
fi
echo ""

# 总结
echo "================================"
echo "📊 诊断总结"
echo "================================"
echo ""
echo "如果所有测试都显示 ✅，说明部署成功！"
echo "如果有 ❌，请查看 TROUBLESHOOTING.md 了解解决方案。"
echo ""
echo "常见问题："
echo "- 返回HTML而不是JSON → 路由配置问题"
echo "- 404错误 → handler未正确导出"
echo "- 500错误 → 检查环境变量和Vercel日志"
echo ""
