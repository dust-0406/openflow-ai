#!/bin/bash
# ==============================================
# 一键推送 openflow-ai 仓库到 GitHub 脚本
# 使用方法：把下面 REMOTE_URL 里的地址改成你自己的 GitHub 仓库地址
# 然后在 Git Bash 里运行：bash push_to_github.sh
# ==============================================

# 👇👇👇 把这里替换成你自己的 GitHub 仓库地址 👇👇👇
REMOTE_URL="https://github.com/dust-0406/openflow-ai.git"
# 👆👆👆 把这里替换成你自己的 GitHub 仓库地址 👆👆👆

echo "=== 1/5 初始化 Git 仓库 ==="
git init

echo "=== 2/5 添加所有文件到暂存区 ==="
git add .

echo "=== 3/5 提交初始代码 ==="
git commit -m "Initial project structure: FastAPI task API + AI summarizer service"

echo "=== 4/5 关联远程仓库 ==="
git remote remove origin 2>/dev/null
git remote add origin $REMOTE_URL

echo "=== 5/5 推送到 GitHub main 分支 ==="
git branch -M main
git push -u origin main

echo ""
echo "✅ 全部完成！刷新你的 GitHub 仓库页面，就能看到完整的目录结构了。"
