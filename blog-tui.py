#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bat-airs 博客管理 TUI
=====================
终端图形界面管理 GitHub Pages 博客：
  - 仪表盘：仓库状态（分支/未提交改动/同步情况/最新提交/Pages 状态）
  - 文章：列表 / 新建 / 编辑 / 删除
  - 发布：一键 git add + commit + push

运行（Linux/macOS）：  bash blog.sh
运行（Windows）：        blog.bat
"""
from __future__ import annotations

import datetime as _dt
import json
import os
import pathlib
import shutil
import subprocess

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.screen import ModalScreen, Screen
from textual.widgets import (
    Button,
    Footer,
    Header,
    Input,
    Label,
    ListItem,
    ListView,
    Markdown,
    Static,
    TabbedContent,
    TabPane,
    TextArea,
)

BASE = pathlib.Path(__file__).resolve().parent
POSTS_DIR = BASE / "_posts"
IMG_DIR = BASE / "assets" / "img"

GITHUB_REPO = "Bat-airs/Bat-airs.github.io"
SITE_URL = "https://bat-airs.github.io"
BLOG_URL = "https://bat-airs.github.io/blog/"


# ============================== 后端逻辑（纯函数） ==============================

def run_cmd(cmd, cwd=None):
    return subprocess.run(
        cmd, shell=False, cwd=cwd or BASE,
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )


def git(args, cwd=None):
    return run_cmd(["git"] + args, cwd=cwd or BASE)


def repo_status() -> dict:
    """仓库状态：分支、改动、最新提交、与远端差异。"""
    info = {}
    b = git(["branch", "--show-current"])
    info["branch"] = b.stdout.strip() or "?"
    st = git(["status", "--short"])
    info["changes"] = [l for l in st.stdout.splitlines() if l.strip()]
    lg = git(["log", "-1", "--format=%h %ad %s", "--date=format:%Y-%m-%d %H:%M"])
    info["last_commit"] = lg.stdout.strip() or "（暂无提交）"
    git(["fetch", "-q"])
    counts = git(["rev-list", "--left-right", "--count", "origin/main...main"]).stdout.strip()
    try:
        behind, ahead = counts.split()
        info["behind"], info["ahead"] = int(behind), int(ahead)
    except Exception:
        info["behind"] = info["ahead"] = 0
    return info


def _find_gh() -> str | None:
    """查找 gh 可执行文件（PATH 或常见位置）。"""
    found = shutil.which("gh")
    if found:
        return found
    for cand in (
        pathlib.Path.home() / ".local" / "bin" / "gh",
        pathlib.Path.home() / ".local" / "share" / "gh" / "bin" / "gh",
    ):
        if cand.exists():
            return str(cand)
    return None


def gh_repo_info():
    """GitHub 仓库信息（需要 gh 已登录；没有则返回 None）。"""
    gh = _find_gh()
    if not gh:
        return None
    r = subprocess.run(
        [gh, "api", f"repos/{GITHUB_REPO}",
         "--jq", "{visibility, updated_at, has_pages}"],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        return None
    try:
        return json.loads(r.stdout)
    except Exception:
        return None


def list_posts() -> list:
    """按时间倒序列出文章。"""
    if not POSTS_DIR.exists():
        return []
    posts = []
    for p in sorted(POSTS_DIR.glob("*.md"), reverse=True):
        title = "（无标题）"
        try:
            for line in p.read_text(encoding="utf-8").splitlines():
                if line.startswith("title:"):
                    title = line.split(":", 1)[1].strip().strip("'\"")
                    break
        except Exception:
            pass
        posts.append({"path": p, "name": p.name, "title": title})
    return posts


def slug_of(title: str) -> str:
    return " ".join(title.split()).replace(" ", "-")


def create_post(title: str) -> pathlib.Path:
    """新建文章模板，返回文件路径。"""
    title = title.strip()
    if not title:
        raise ValueError("标题不能为空")
    now = _dt.datetime.now()
    fname = f"{now:%Y-%m-%d}-{slug_of(title)}.md"
    path = POSTS_DIR / fname
    if path.exists():
        raise FileExistsError(f"已存在: {fname}")
    body = (
        f"---\n"
        f"layout: post\n"
        f"title: {title}\n"
        f"date: {now:%Y-%m-%d %H:%M:%S} +0800\n"
        f"tags: []\n"
        f"---\n\n"
        f"正文从这里开始写……\n"
    )
    path.write_text(body, encoding="utf-8")
    return path


def publish() -> list:
    """提交并推送全部改动，返回输出行列表。"""
    msgs = []
    git(["add", "-A"])
    st = git(["diff", "--cached", "--name-only"])
    names = [l for l in st.stdout.splitlines() if l.strip()]
    if not names:
        return ["没有待发布的改动。", "可以先在「文章」里新建或修改内容。"]
    post = next((n for n in names if n.startswith("_posts/")), None)
    msg = f"发布: {os.path.basename(post)}" if post else "博客更新"
    c = git(["commit", "-q", "-m", msg])
    if c.returncode != 0:
        return ["提交失败:", c.stderr.strip() or c.stdout.strip()]
    msgs.append(f"✔ 提交成功：{msg}")
    p = git(["push", "-q", "origin", "main"])
    if p.returncode != 0:
        msgs.append("推送失败: " + (p.stderr.strip() or p.stdout.strip()))
    else:
        msgs.append("✔ 已推送到 GitHub")
        msgs.append("GitHub Pages 约 1-2 分钟后自动更新")
        msgs.append("博客: " + BLOG_URL)
    return msgs


# ============================== 文本工具 ==============================

def dashboard_text() -> str:
    s = repo_status()
    lines = [
        "# 仓库状态",
        "",
        f"**分支：** `{s['branch']}`",
        f"**未提交改动：** {len(s['changes'])} 项",
        f"**与远端差异：** 领先 {s['ahead']} / 落后 {s['behind']}",
        f"**最新提交：** {s['last_commit']}",
        "",
        f"**仓库：** https://github.com/{GITHUB_REPO}",
        f"**站点：** {SITE_URL}",
    ]
    gh = gh_repo_info()
    if gh:
        lines += [
            f"**GitHub：** 可见性 {gh.get('visibility', '?')} · Pages {'开启' if gh.get('has_pages') else '未开启'}",
            f"**最近更新：** {gh.get('updated_at', '?')}",
        ]
    else:
        lines += ["**GitHub：** 未检测到 gh 登录（可选）"]
    if s["changes"]:
        lines += ["", "**待发布改动：**"]
        lines += [f"- `{c}`" for c in s["changes"][:12]]
    return "\n".join(lines)


# ============================== 界面 ==============================

class EditorScreen(Screen):
    """文章编辑器（整屏）。"""

    def __init__(self, path: pathlib.Path, **kwargs):
        super().__init__(**kwargs)
        self.path = path
        self.content = path.read_text(encoding="utf-8") if path.exists() else ""

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Label(f"📝 编辑：{self.path.name}", id="editor-title")
        yield TextArea(self.content, language="markdown", id="editor")
        with Horizontal(id="editor-bar"):
            yield Button("保存并返回", id="save-btn", variant="success")
            yield Button("放弃返回", id="cancel-btn")
            yield Static(f" {BLOG_URL}", id="editor-hint")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save-btn":
            text = self.query_one("#editor", TextArea).text
            self.path.write_text(text, encoding="utf-8")
            self.notify(f"已保存 {self.path.name}", severity="information", timeout=3)
        self.app.pop_screen()


class NewPostScreen(ModalScreen):
    """新建文章弹窗。"""

    BINDINGS = [Binding("escape", "cancel", "取消")]

    def compose(self) -> ComposeResult:
        with Vertical(id="newpost-box"):
            yield Label("📄 新建文章")
            yield Input(placeholder="输入文章标题，例如：我的世界服务器记录", id="title-input")
            with Horizontal(id="newpost-bar"):
                yield Button("创建", id="create-btn", variant="primary")
                yield Button("取消", id="close-btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "create-btn":
            title = self.query_one("#title-input", Input).value
            try:
                path = create_post(title)
            except (ValueError, FileExistsError) as e:
                self.notify(str(e), severity="error", timeout=4)
                return
            self.notify(f"已创建：{path.name}", severity="information", timeout=3)
            self.app.pop_screen()
            self.app.push_screen(EditorScreen(path))
        else:
            self.app.pop_screen()

    def action_cancel(self) -> None:
        self.app.pop_screen()


class ConfirmScreen(ModalScreen):
    """确认弹窗。"""

    def __init__(self, message: str, on_yes, **kwargs):
        super().__init__(**kwargs)
        self.message = message
        self.on_yes = on_yes

    def compose(self) -> ComposeResult:
        with Vertical(id="confirm-box"):
            yield Label(self.message)
            with Horizontal(id="confirm-bar"):
                yield Button("确认", id="yes-btn", variant="error")
                yield Button("取消", id="no-btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "yes-btn":
            self.on_yes()
        self.app.pop_screen()


class BlogApp(App):
    """博客管理主应用。"""

    TITLE = "Bat-airs 博客管理"
    SUB_TITLE = BLOG_URL
    CSS = """
    Screen { layout: vertical; }
    #dash-scroll { padding: 1 2; }
    #dash-actions { height: auto; padding: 1 0; }
    #dash-actions Button { margin: 0 1 0 0; }
    #post-list { border: round $primary; margin: 1 0; }
    #editor-title { padding: 1 2; text-style: bold; }
    #editor { height: 1fr; border: round $primary; }
    #editor-bar { height: 3; padding: 0 1; align-horizontal: left; align-vertical: middle; }
    #editor-bar Button { margin-right: 1; }
    #editor-hint { color: $text-muted; padding-top: 1; }
    #newpost-box, #confirm-box {
        width: 60; height: auto; padding: 1 2;
        border: thick $primary; background: $surface;
        align-horizontal: center; align-vertical: middle;
    }
    #newpost-box Input { margin: 1 0; }
    #newpost-bar, #confirm-bar { align-horizontal: center; }
    #newpost-bar Button, #confirm-bar Button { margin: 0 1; }
    """
    BINDINGS = [
        Binding("q", "quit", "退出"),
        Binding("n", "new_post", "新建文章"),
        Binding("p", "publish", "发布"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with TabbedContent():
            with TabPane("📊 仪表盘", id="dash"):
                with VerticalScroll(id="dash-scroll"):
                    yield Markdown(id="dash-status")
                    with Horizontal(id="dash-actions"):
                        yield Button("刷新状态", id="refresh-btn")
                        yield Button("新建文章", id="new-btn")
                        yield Button("发布", id="publish-btn", variant="success")
                        yield Button("退出", id="quit-btn")
            with TabPane("📝 文章", id="posts"):
                with Vertical(id="posts-pane"):
                    yield ListView(id="post-list")
                    yield Label("↑↓ 选择 · Enter 编辑 · d 删除 · 快捷键: n 新建 / p 发布", id="posts-hint")
        yield Footer()

    def on_mount(self) -> None:
        self.refresh_dashboard()
        self.refresh_posts()

    # ---------- 工具 ----------
    def refresh_dashboard(self) -> None:
        self.query_one("#dash-status", Markdown).update(dashboard_text())

    def refresh_posts(self) -> None:
        lv = self.query_one("#post-list", ListView)
        lv.clear()
        posts = list_posts()
        if not posts:
            lv.append(ListItem(Label("（还没有文章，按 n 新建）")))
            return
        for p in posts:
            d = p["path"].name[:10]
            lv.append(ListItem(Label(f"{d}  {p['title']}  ·  {p['name']}")))

    # ---------- 事件 ----------
    def on_button_pressed(self, event: Button.Pressed) -> None:
        bid = event.button.id
        if bid == "refresh-btn":
            self.refresh_dashboard()
            self.notify("已刷新", severity="information", timeout=2)
        elif bid == "new-btn":
            self.push_screen(NewPostScreen())
        elif bid == "publish-btn":
            self.action_publish()
        elif bid == "quit-btn":
            self.exit()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        posts = list_posts()
        idx = self.query_one("#post-list", ListView).index
        if idx is not None and idx < len(posts):
            self.push_screen(EditorScreen(posts[idx]["path"]))

    def on_key(self, event) -> None:
        if event.key == "d" and self.screen is self:
            lv = self.query_one("#post-list", ListView)
            idx = lv.index
            posts = list_posts()
            if idx is None or idx >= len(posts):
                return
            post = posts[idx]

            def do_delete():
                try:
                    post["path"].unlink()
                    self.notify(f"已删除 {post['name']}", severity="warning", timeout=3)
                except OSError as e:
                    self.notify(f"删除失败: {e}", severity="error", timeout=4)
                self.refresh_posts()

            self.push_screen(ConfirmScreen(f"确认删除文章：\n{post['title']}\n（{post['name']}）？", do_delete))

    # ---------- 动作 ----------
    def action_new_post(self) -> None:
        self.push_screen(NewPostScreen())

    def action_publish(self) -> None:
        lines = publish()
        text = "# 发布结果\n\n" + "\n".join(f"- {l}" if not l.startswith("#") else l for l in lines)
        self.push_screen(ResultScreen(text))
        self.refresh_dashboard()
        self.refresh_posts()


class ResultScreen(ModalScreen):
    """发布结果弹窗。"""

    BINDINGS = [Binding("escape", "close", "关闭")]

    def __init__(self, text: str, **kwargs):
        super().__init__(**kwargs)
        self.text = text

    def compose(self) -> ComposeResult:
        with Vertical(id="result-box"):
            yield Markdown(self.text)
            yield Button("关闭", id="close-btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.app.pop_screen()

    def action_close(self) -> None:
        self.app.pop_screen()


def main() -> None:
    BlogApp().run()


if __name__ == "__main__":
    main()
