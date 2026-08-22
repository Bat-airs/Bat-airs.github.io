#!/usr/bin/env bash
# 一键新建文章：bash new-post.sh "文章标题"
# 会在 _posts/ 下生成 日期-标题.md 模板，然后用文本编辑器打开
set -e
cd "$(dirname "$0")"

if [ -z "$1" ]; then
  echo "用法: bash new-post.sh \"文章标题\""
  echo "示例: bash new-post.sh \"我的世界服务器搭建记录\""
  exit 1
fi

TITLE="$1"
DATE=$(date +%Y-%m-%d)
TIME=$(date +%H:%M:%S)
SLUG=$(echo "$TITLE" | sed 's/[[:space:]][[:space:]]*/ /g' | tr ' ' '-')
FILE="_posts/${DATE}-${SLUG}.md"

if [ -e "$FILE" ]; then
  echo "[错误] 文件已存在: $FILE"
  exit 1
fi

cat > "$FILE" <<EOF
---
layout: post
title: ${TITLE}
date: ${DATE} ${TIME} +0800
tags: []
---

正文从这里开始写……
EOF

echo ""
echo "已创建: $FILE"
echo "写完正文后运行: bash publish.sh"
echo ""

# 尝试打开文本编辑器（按优先级）
for EDITOR in code kate gedit nano; do
  if command -v "$EDITOR" >/dev/null 2>&1; then
    "$EDITOR" "$FILE" >/dev/null 2>&1 || true
    break
  fi
done
