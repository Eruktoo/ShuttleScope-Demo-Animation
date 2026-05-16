# ShuttleScope Demo Animation

用 Manim (3Blue1Brown 动画引擎) 制作的羽毛球数据分析介绍视频。

## 工作流

1. `plan.md` — 叙事大纲
2. `script.py` — Manim Python 动画脚本
3. `manim -ql script.py SceneName` — 服务器渲染 480p 草稿
4. `manim -qh script.py SceneName` — 本地渲染 1080p 成品

## 依赖

```bash
pip install manim
# 还需要 ffmpeg
```

## 渲染命令

```bash
cd shuttlescope-video

# 草稿 (快)
source ../.venv-manim/bin/activate && manim -ql script.py Scene3_Resilience

# 成品
manim -qh script.py Scene1 Scene2 ...
```
