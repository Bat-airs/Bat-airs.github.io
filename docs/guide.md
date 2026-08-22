# 博客管理工具（TUI）使用说明

一个运行在**终端里的图形界面**（TUI），用来管理 [Bat airs 的个人博客](https://bat-airs.github.io/)：看仓库状态、写文章、管项目、一键发布，全部不用离开终端。

---

## 一、启动

```bash
cd ~/Bat-airs.github.io
bash blog.sh
```

- **Windows**：双击 `blog.bat`
- 首次运行会自动创建工具环境（`.venv-tui/`）并安装依赖，之后秒开
- 桌面快捷方式：**「博客管理（TUI）」**（已放在桌面）

## 二、三个界面

| 标签页 | 功能 |
|---|---|
| 📊 **仪表盘** | 仓库状态：分支、未提交改动数、与远端领先/落后、最新提交、GitHub 仓库信息（可见性/Pages/更新时间）、站点链接 |
| 📝 **文章** | 全部文章列表（日期+标题），新建 / 编辑 / 删除 |
| 🚀 **项目** | 首页"项目"区管理：新建 / 编辑 / 删除项目介绍（名称、介绍文字、链接、标签） |

## 三、快捷键

| 按键 | 功能 |
|---|---|
| `Tab` | 切换标签页 |
| `↑` / `↓` | 选择文章 / 项目 |
| `Enter` | 编辑选中项（文章进编辑器，项目进表单） |
| `d` | 删除选中项（有确认提示） |
| `n` | 新建文章 |
| `p` | 发布（git add + commit + push） |
| `q` | 退出 |

## 四、依赖

- Python 3.10+
- `textual`（TUI 框架）、`pyyaml`（项目数据读写）——由 `blog.sh` / `blog.bat` 首次运行自动安装

## 五、文件结构

```
~/Bat-airs.github.io/
├── blog-tui.py        # 主程序（纯 Python）
├── blog.sh            # Linux/macOS 启动脚本
├── blog.bat           # Windows 启动脚本
├── .venv-tui/         # 工具环境（自动创建，已忽略提交）
├── new-post.sh        # 命令行新建文章（可选）
├── publish.sh         # 命令行发布（可选）
├── add-img.sh         # 命令行插图（可选）
├── _posts/            # 文章（Markdown）
├── _data/projects.yml # 项目数据（TUI「项目」页读写）
└── assets/img/        # 图片
```

## 六、常见问题

**Q：启动报错 / 想重装工具环境？**
删除 `.venv-tui` 文件夹后重新运行 `bash blog.sh`，会自动重建。

**Q：仪表盘不显示 GitHub 信息？**
需要 `gh` 已登录（`gh auth status` 查看）。工具会自动查找 `gh`（含 `~/.local/bin/gh`），未登录只是不显示 GitHub 行，不影响其他功能。

**Q：发布后多久生效？**
GitHub Pages 约 1-2 分钟自动构建上线。

**Q：发布被拒绝？**
main 分支开启了保护（禁强推/禁删分支），正常 `git push` 不受影响；如报错请把 TUI 里的提示发出来排查。

**Q：工具能用但想加功能？**
`blog-tui.py` 是单一 Python 文件，`blog.sh` 改环境、`blog-tui.py` 改界面逻辑。

---

管理愉快！🚀
