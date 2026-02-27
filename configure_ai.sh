#!/bin/bash

# AI模型配置助手
# 快速添加API密钥到.env文件

echo "========================================="
echo "  🤖 AI模型配置助手"
echo "========================================="
echo ""
echo "这个脚本会帮你配置AI模型的API密钥"
echo ""

# 检查.env文件是否存在
if [ ! -f ".env" ]; then
    echo "❌ 找不到.env文件"
    echo "正在从.env.example创建..."
    cp .env.example .env
fi

echo "请选择要配置的模型（可多选）："
echo ""
echo "免费模型："
echo "  1) Google Gemini (完全免费，推荐)"
echo "  2) 智谱AI GLM-4 (完全免费，国内可用)"
echo "  3) Groq (免费)"
echo ""
echo "付费模型："
echo "  4) Anthropic Claude (质量最高)"
echo "  5) DeepSeek (极低成本)"
echo "  6) OpenAI GPT"
echo ""
echo "  0) 完成配置"
echo ""

# 配置函数
add_gemini() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  配置 Google Gemini"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "获取API密钥："
    echo "1. 访问：https://ai.google.dev/"
    echo "2. 点击 'Get API Key'"
    echo "3. 复制API密钥"
    echo ""
    read -p "请输入Gemini API密钥: " gemini_key

    if [ ! -z "$gemini_key" ]; then
        # 检查是否已存在
        if grep -q "GEMINI_API_KEY=" .env; then
            # 更新已存在的密钥
            sed -i "s|GEMINI_API_KEY=.*|GEMINI_API_KEY=$gemini_key|" .env
        else
            # 添加新密钥
            echo "" >> .env
            echo "# Google Gemini 配置" >> .env
            echo "GEMINI_API_KEY=$gemini_key" >> .env
            echo "GEMINI_MODEL=gemini-2.0-flash-exp" >> .env
        fi
        echo "✅ Gemini配置成功！"
    fi
}

add_claude() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  配置 Anthropic Claude"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "获取API密钥："
    echo "1. 访问：https://console.anthropic.com/"
    echo "2. Settings → API Keys"
    echo "3. Create Key"
    echo ""
    read -p "请输入Claude API密钥: " claude_key

    if [ ! -z "$claude_key" ]; then
        if grep -q "CLAUDE_API_KEY=" .env; then
            sed -i "s|CLAUDE_API_KEY=.*|CLAUDE_API_KEY=$claude_key|" .env
        else
            echo "" >> .env
            echo "# Anthropic Claude 配置" >> .env
            echo "CLAUDE_API_KEY=$claude_key" >> .env
            echo "CLAUDE_MODEL=claude-3-5-haiku-20241022" >> .env
        fi
        echo "✅ Claude配置成功！"
    fi
}

add_deepseek() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  配置 DeepSeek"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "获取API密钥："
    echo "1. 访问：https://platform.deepseek.com/"
    echo "2. API Keys → Create API Key"
    echo ""
    read -p "请输入DeepSeek API密钥: " deepseek_key

    if [ ! -z "$deepseek_key" ]; then
        if grep -q "DEEPSEEK_API_KEY=" .env; then
            sed -i "s|DEEPSEEK_API_KEY=.*|DEEPSEEK_API_KEY=$deepseek_key|" .env
        else
            echo "" >> .env
            echo "# DeepSeek 配置" >> .env
            echo "DEEPSEEK_API_KEY=$deepseek_key" >> .env
        fi
        echo "✅ DeepSeek配置成功！"
    fi
}

add_zhipu() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  配置 智谱AI"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "获取API密钥："
    echo "1. 访问：https://open.bigmodel.cn/"
    echo "2. 创建API Key"
    echo ""
    read -p "请输入智谱AI API密钥: " zhipu_key

    if [ ! -z "$zhipu_key" ]; then
        if grep -q "ZHIPU_API_KEY=" .env; then
            sed -i "s|ZHIPU_API_KEY=.*|ZHIPU_API_KEY=$zhipu_key|" .env
        else
            echo "" >> .env
            echo "# 智谱AI 配置" >> .env
            echo "ZHIPU_API_KEY=$zhipu_key" >> .env
            echo "ZHIPU_MODEL=glm-4-flash" >> .env
        fi
        echo "✅ 智谱AI配置成功！"
    fi
}

add_openai() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  配置 OpenAI GPT"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "获取API密钥："
    echo "1. 访问：https://platform.openai.com/"
    echo "2. API keys → Create new secret key"
    echo ""
    read -p "请输入OpenAI API密钥: " openai_key

    if [ ! -z "$openai_key" ]; then
        if grep -q "OPENAI_API_KEY=" .env; then
            sed -i "s|OPENAI_API_KEY=.*|OPENAI_API_KEY=$openai_key|" .env
        else
            echo "" >> .env
            echo "# OpenAI 配置" >> .env
            echo "OPENAI_API_KEY=$openai_key" >> .env
            echo "OPENAI_MODEL=gpt-4o-mini" >> .env
        fi
        echo "✅ OpenAI配置成功！"
    fi
}

add_groq() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  配置 Groq"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "获取API密钥："
    echo "1. 访问：https://console.groq.com/"
    echo "2. 创建API Key"
    echo ""
    read -p "请输入Groq API密钥: " groq_key

    if [ ! -z "$groq_key" ]; then
        if grep -q "GROQ_API_KEY=" .env; then
            sed -i "s|GROQ_API_KEY=.*|GROQ_API_KEY=$groq_key|" .env
        else
            echo "" >> .env
            echo "# Groq 配置" >> .env
            echo "GROQ_API_KEY=$groq_key" >> .env
        fi
        echo "✅ Groq配置成功！"
    fi
}

# 主循环
while true; do
    echo ""
    read -p "请选择要配置的模型（输入数字）: " choice

    case $choice in
        1) add_gemini ;;
        2) add_zhipu ;;
        3) add_groq ;;
        4) add_claude ;;
        5) add_deepseek ;;
        6) add_openai ;;
        0) break ;;
        *) echo "❌ 无效选择" ;;
    esac
done

echo ""
echo "========================================="
echo "  ✅ 配置完成！"
echo "========================================="
echo ""
echo "下一步："
echo "1. 重启应用以加载新配置"
echo "2. 查看日志确认使用的模型"
echo ""
echo "推荐阅读：AI_CONFIG_GUIDE.md"
echo ""
