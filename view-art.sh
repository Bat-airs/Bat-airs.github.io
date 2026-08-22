#!/usr/bin/env bash
# 在终端里查看博客的全部字符画（Unicode 正确排版；ANSI 码显示彩色）
cd "$(dirname "$0")"
exec ./.venv-tui/bin/python - <<'EOF'
import importlib.util

spec = importlib.util.spec_from_file_location("blogtui", "blog-tui.py")
bt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bt)

from rich.console import Console
from rich.text import Text

console = Console()
arts = bt.load_ascii_arts()
if not arts:
    console.print("[yellow]还没有字符画[/]")
    raise SystemExit

for i, a in enumerate(arts, 1):
    console.print(f"[bold cyan]{i}. {a.get('title') or '（无标题）'}[/]")
    art = a.get("art", "")
    if a.get("ansi"):
        console.print(Text.from_ansi(art))
    else:
        console.print(Text(art))
    console.print()
EOF
