#!/usr/bin/env bash
# 一键发布：提交并推送博客的全部改动，GitHub Pages 自动构建
set -e
cd "$(dirname "$0")"

git add -A
if git diff --cached --quiet; then
  echo "没有待发布的改动。"
  echo "先运行: bash new-post.sh \"文章标题\"  或 手动在 _posts/ 下新建 .md 文件"
  exit 0
fi

# 用最新改动的文章名生成提交信息
MSG=$(git diff --cached --name-only | grep -m1 '_posts/' | sed 's#_posts/##' || true)
if [ -z "$MSG" ]; then
  MSG="博客更新"
fi

git commit -q -m "发布: ${MSG}"
git push -q origin main

echo ""
echo "✅ 已推送: ${MSG}"
echo "   GitHub Pages 约 1-2 分钟后自动更新"
echo "   博客地址: https://bat-airs.github.io/"
echo "   文章列表: https://bat-airs.github.io/blog/"
