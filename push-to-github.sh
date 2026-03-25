#!/bin/bash
# 推送到 GitHub 的脚本
# 使用方法：./push-to-github.sh <github-username>

REPO_NAME="hot-movies-recommend"
GITHUB_USER=$1

if [ -z "$GITHUB_USER" ]; then
    echo "用法：$0 <github-username>"
    echo "示例：$0 huanghou"
    exit 1
fi

echo "📦 准备推送到 GitHub..."
echo "仓库名称：$REPO_NAME"
echo "GitHub 用户：$GITHUB_USER"
echo ""

# 初始化 Git 仓库（如果还没有）
if [ ! -d ".git" ]; then
    git init
fi

# 添加文件
git add .

# 提交
git commit -m "Initial commit: 热播影视推荐页面" 2>/dev/null || echo "已有提交"

# 重 重命名分支
main

# 创建 GitHub 仓库并推送
echo ""
echo "🔗 请在 GitHub 创建仓库后，执行以下命令："
echo ""
echo "cd /home/admin/.openclaw/workspace-pm/hot-movies-recommend"
echo "git remote add origin https://github.com/${GITHUB_USER}/${REPO_NAME}.git"
echo "git push -u origin--force origin main"
echo ""
echo "或者，先访问 https://github.com/new 创建空仓库，然后执行上述