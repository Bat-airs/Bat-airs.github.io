---
layout: post
title: AsciiCraft-GUI 使用指南
date: 2026-08-22 11:00:00 +0800
tags: [教程, 工具]
---

[AsciiCraft-GUI](https://github.com/Bat-airs/AsciiCraft-GUI) 是我做的一个把图片/视频转成 ASCII 艺术的本地图形界面。这篇记录一下它的用法。

## 支持的转换类型

- 图片 → 文本
- 图片 → ASCII 图（黑白 / 彩色）
- 视频 → ASCII 视频（黑白 / 彩色）

## 快速开始

需要 Python 3.10+，然后：

```bash
# Windows
双击 gui\start.bat

# Linux
cd gui && bash start.sh
```

浏览器打开 `http://127.0.0.1:5050` 即可使用。

## 小技巧

- **宽度（字符列数）**：越大越精细但越慢，图片建议 150-300，视频建议 60-120
- **语言**：支持中文、日文平假名/片假名、韩文等 12 种字符
- 完全本地运行，不需要联网

Enjoy! ✨
