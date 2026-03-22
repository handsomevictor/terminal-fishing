# Terminal Fishing Game (终端钓鱼游戏)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Terminal](https://img.shields.io/badge/Interface-CLI%20(curses)-orange.svg)

**Terminal Fishing Game** 是一款完全在终端 (Command Line Interface) 中运行的动态交互式钓鱼游戏。本项目采用纯 Python 编写，利用 `curses` 库实现非阻塞输入与高帧率的终端图形渲染。

## 🌟 核心特性 (Features)

- **动态渲染与平滑动画**：利用 `curses` 内部双缓冲与增量覆盖机制，解决传统终端界面频繁刷新导致的闪烁问题。
- **物理运动模拟**：使用贝塞尔曲线 (Bézier Curve) 模拟鱼钩抛出的自然抛物线轨迹；同时实现水面随机波纹的动态生成。
- **生态与概率系统**：
  - **多种鱼类**：内置普通、罕见、稀有、史诗等多稀有度鱼类，游动速度、颜色与行为逻辑各不相同。
  - **动态判定**：根据鱼钩落点、鱼类视距进行实时的三维坐标碰撞模拟（在 2D 平面映射）。
- **QTE 机制 (Quick Time Event)**：咬钩时需要玩家在极短的时间窗口内做出反应，增加了游戏的动作性和紧张感。

## 🚀 安装与运行 (Getting Started)

### 环境依赖
- Python 3.8 或更高版本
- 操作系统：macOS / Linux (由于使用了 `curses` 库，Windows 平台可能需要安装 `windows-curses` 包：`pip install windows-curses`)

### 启动游戏
无需额外安装复杂的第三方库，直接通过 Python 运行入口文件即可启动：

```bash
# 克隆仓库 (如适用)
git clone https://github.com/your-username/terminal-fishing.git
cd terminal-fishing

# 启动游戏
python run.py
```

## 🎮 游戏指南 (How to Play)

1. **抛竿 (Casting)**：在空闲状态下，按下 **空格键 (Space)**，鱼钩将划过一道优美的弧线落入水中。
2. **等待咬钩 (Waiting)**：观察水面下的鱼群，当有鱼游近鱼钩时，有一定的概率触发咬钩。
3. **收杆 (Reeling)**：当水面的浮标剧烈抖动，出现红色的 `!` 提示，并在屏幕中央出现 `[####       ]` 收杆进度条时，迅速按下 **回车键 (Enter)** 收杆。
4. **得分 (Scoring)**：成功钓上鱼后将根据鱼的稀有度获得相应的分数。
5. **退出游戏**：随时按下 **`q`** 键可安全退出游戏并恢复终端初始状态。

## ⚙️ 游戏配置 (Configuration)

本项目高度可定制。你可以通过修改 `fishing_game/config.py` 来改变游戏核心参数：
- `FPS`：游戏帧率（默认 20）。
- `BITE_CHANCE`：鱼靠近时的基础咬钩概率。
- `REEL_TIME_LIMIT`：QTE 收杆反应时间限制。
- `FISH_TYPES`：可自定义新增鱼类，修改其符号、颜色、速度及分值。

## 🤝 参与贡献 (Contributing)

欢迎提交 Issue 和 Pull Request 来帮助完善本项目。具体可参考 [PROGRESS.md](PROGRESS.md) 了解当前项目的开发进度与未来规划。

## 📄 许可证 (License)

本项目基于 [MIT License](LICENSE) 开源，请自由使用、修改和分发。
