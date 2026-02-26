#!/bin/bash
# 推送代码到GitHub的脚本
# 使用方法：将YOUR_TOKEN替换为你的GitHub Personal Access Token

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== 推送代码到GitHub ===${NC}"
echo ""
echo "请将YOUR_TOKEN替换为您的Personal Access Token后执行："
echo ""
echo -e "${GREEN}git remote set-url origin https://YOUR_TOKEN@github.com/xiaolvzz/paper-web-manager.git${NC}"
echo -e "${GREEN}git push -u origin main${NC}"
echo ""
echo "示例："
echo "git remote set-url origin https://ghp_abc123xyz@github.com/xiaolvzz/paper-web-manager.git"
echo "git push -u origin main"
