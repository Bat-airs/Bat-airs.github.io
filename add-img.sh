#!/usr/bin/env bash
# 一键往文章里插图：bash add-img.sh 图片路径 [描述]
# 会把图片复制到 assets/img/ 并输出可直接粘贴进文章的 Markdown
set -e
cd "$(dirname "$0")"

SRC="$1"
DESC="${2:-图片}"
if [ -z "$SRC" ]; then
  echo "用法: bash add-img.sh 图片路径 [描述]"
  echo "示例: bash add-img.sh ~/桌面/照片.jpg 我的世界服务器截图"
  exit 1
fi
if [ ! -f "$SRC" ]; then
  echo "[错误] 找不到文件: $SRC"
  exit 1
fi

mkdir -p assets/img
STAMP=$(date +%Y%m%d-%H%M%S)
DST="assets/img/${STAMP}-$(basename "$SRC")"
cp "$SRC" "$DST"

echo ""
echo "✅ 已复制到: $DST"
echo ""
echo "在文章正文里粘贴这一行："
echo "  ![${DESC}](/assets/img/$(basename "$DST"))"
echo ""
echo "图片文章也可以在文章头部加字段："
echo "  image: /assets/img/$(basename "$DST")      # 封面大图"
echo "  gallery:                                  # 多图相册"
echo "    - /assets/img/$(basename "$DST")"
echo ""
echo "最后运行 bash publish.sh 发布"
