#!/usr/bin/env bash
# 博客管理 TUI 启动脚本（Linux/macOS）
set -e
cd "$(dirname "$0")"

if [ ! -d .venv-tui ]; then
  echo "[首次运行] 创建工具环境并安装 textual..."
  python3 -m venv .venv-tui
  ./.venv-tui/bin/pip install -q --upgrade pip
  ./.venv-tui/bin/pip install -q textual
fi

exec ./.venv-tui/bin/python blog-tui.py "$@"
