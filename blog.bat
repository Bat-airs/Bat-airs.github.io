@echo off
chcp 65001 >nul
title Bat-airs 博客管理
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
  echo [错误] 未找到 Python，请先安装 Python 3.10+ 并勾选 Add to PATH。
  pause
  exit /b 1
)

if not exist .venv-tui (
  echo [首次运行] 创建工具环境并安装 textual...
  python -m venv .venv-tui
  call .venv-tui\Scripts\activate.bat
  python -m pip install --upgrade pip
  pip install textual
) else (
  call .venv-tui\Scripts\activate.bat
)

python blog-tui.py
pause
