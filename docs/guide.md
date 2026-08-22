# 博客使用指南

欢迎！这是 [Bat airs 的个人博客](https://bat-airs.github.io/) 的使用说明。博客基于 **Jekyll + GitHub Pages**，你只需要写 Markdown，剩下的发布和上线全部自动完成。

---

## 一、写文章（三种方式任选）

### 方式 1：网页直接写（最省事）

1. 打开 https://github.com/Bat-airs/Bat-airs.github.io → 进入 `_posts` 文件夹
2. 点 **Add file → Create new file**
3. 文件名：`2026-08-22-文章标题.md`（**日期前缀必须有**）
4. 内容头部粘贴模板，下面写正文：

```markdown
---
layout: post
title: 文章标题
date: 2026-08-22 12:00:00 +0800
tags: [标签1, 标签2]
---

正文在这里写，支持 Markdown：
**加粗**、`代码`、# 标题、![图片](图片地址) 等
```

5. 点 **Commit changes** → 1-2 分钟后自动发布

### 方式 2：本地一键脚本

```bash
cd ~/Bat-airs.github.io
bash new-post.sh "文章标题"   # 自动生成模板并打开编辑器
bash publish.sh              # 写完发布
```

### 方式 3：博客管理 TUI（推荐）

```bash
cd ~/Bat-airs.github.io
bash blog.sh
```

TUI 里有完整的仪表盘、文章列表、编辑器、发布按钮，还有项目管理。

---

## 二、图片文章

在文章头部加两个字段即可：

```markdown
---
layout: post
title: 图片文章示例
date: 2026-08-22 15:00:00 +0800
image: /assets/img/封面图.jpg        # 封面大图（可选）
gallery:                            # 相册（可选，多张）
  - /assets/img/图1.jpg
  - /assets/img/图2.jpg
---
```

正文插图用一键脚本：

```bash
bash add-img.sh ~/桌面/照片.jpg 图片描述
# 会自动复制图片并输出可粘贴的 Markdown
```

---

## 三、项目管理

首页的"项目"区域由 `_data/projects.yml` 驱动。两种改法：

- **TUI**：`bash blog.sh` → 「🚀 项目」标签 → 新建/编辑/删除
- **直接编辑** `_data/projects.yml`：

```yaml
- name: 项目名称
  desc: 一句话介绍
  url: https://github.com/Bat-airs/xxx
  tag: 标签
```

改完记得运行 `bash publish.sh` 或按 `p` 发布。

---

## 四、发布

所有改动（文章/项目/图片）统一发布：

```bash
bash publish.sh
# 或 TUI 里按 p
```

发布后 **GitHub Pages 约 1-2 分钟**自动构建上线。

---

## 五、TUI 快捷键

| 按键 | 功能 |
|---|---|
| `Tab` | 切换标签页（仪表盘/文章/项目） |
| `↑` / `↓` | 选择文章或项目 |
| `Enter` | 编辑选中的文章/项目 |
| `d` | 删除选中的文章/项目（需确认） |
| `n` | 新建文章 |
| `p` | 发布 |
| `q` | 退出 |

---

## 六、常见问题

**Q：文章没显示？**
检查文件名是否是 `YYYY-MM-DD-标题.md` 格式（必须带日期），且头部有 `layout: post`。改完再发布，等 1-2 分钟。

**Q：发布失败 / 推送被拒？**
仓库 main 分支开启了保护（禁止强推、禁止删分支），正常 `git push` 不受影响。如果报错，把 TUI 或终端里的错误信息发出来排查。

**Q：想改网站样式/结构？**
直接改 `assets/css/style.css`（样式）、`_layouts/`（页面模板）、`_includes/`（导航页脚），改完发布即可。深色模式在 style.css 的 `[data-theme="dark"]` 里调整。

**Q：怎么让某个页面（如本指南）出现在导航里？**
编辑 `_includes/header.html`，加一行 `<a href="/guide/">指南</a>`。

---

祝写作愉快！✍️
