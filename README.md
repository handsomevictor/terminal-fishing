# Terminal Fishing Game (终端钓鱼游戏)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Terminal](https://img.shields.io/badge/Interface-CLI%20(curses)-orange.svg)

**Terminal Fishing Game** 是一款完全在终端 (Command Line Interface) 中运行的动态交互式钓鱼游戏。本项目采用纯 Python 编写，利用 `curses` 库实现非阻塞输入与高帧率的终端图形渲染。

## 🌟 核心特性 (Features)

- **动态渲染与平滑动画**：利用 `curses` 内部双缓冲与增量覆盖机制，解决传统终端界面频繁刷新导致的闪烁问题。
- **物理运动模拟**：使用贝塞尔曲线 (Bézier Curve) 模拟鱼钩抛出的自然抛物线轨迹；同时实现水面随机波纹的动态生成。
- **丰富的生态系统**：
  - **多种鱼类与垃圾**：内置普通、罕见、稀有、史诗等多稀有度鱼类，以及"破靴子"、"空易拉罐"等垃圾干扰项。
  - **动态难度系统**：随着玩家分数的增加，鱼群刷新频率会加快，咬钩后的反应时间也会逐渐缩短。
- **连击与高分机制 (Combo & High Score)**：
  - 连续成功钓到鱼会增加 Combo，提供分数乘数加成。
  - 钓到"垃圾"或未及时收杆会重置 Combo。
  - 游戏会自动在本地 `save.json` 保存你的最高分记录。
- **QTE 机制 (Quick Time Event)**：咬钩时会有强烈的屏幕闪烁提示，玩家必须在极短的时间窗口内做出反应。

## 🚀 安装与运行 (Getting Started)

### 环境依赖
- Python 3.8 或更高版本
- 操作系统：macOS / Linux (由于使用了 `curses` 库，Windows 平台可能需要安装 `windows-curses` 包：`pip install windows-curses`)

### 启动游戏
无需额外安装复杂的第三方库，直接通过 Python 运行入口文件即可启动：

```bash
# 启动游戏
python run.py

# 自动化测试模式 (运行 50 帧后自动退出，用于 CI/CD)
python run.py --test
```

## 🎮 游戏指南 (How to Play)

1. **抛竿 (Casting)**：在空闲状态下，按下 **空格键 (Space)**，鱼钩将划过一道弧线落入水中。
2. **等待咬钩 (Waiting)**：观察水面下的鱼群。当有鱼游近鱼钩时，有一定的概率触发咬钩。
3. **收杆 (Reeling)**：当屏幕上方闪烁 **` BITE! `**，并出现红色的 `!` 和进度条时，迅速按下 **回车键 (Enter)** 收杆。
4. **得分与连击 (Scoring & Combo)**：钓上鱼会增加分数和连击数，连击越高分数加成越高；但如果钓到垃圾，不仅会扣分，还会断掉连击！
5. **退出游戏**：随时按下 **`q`** 键可保存最高分并安全退出游戏。

## ⚙️ 游戏配置 (Configuration)

本项目高度可定制。你可以通过修改 `fishing_game/config.py` 来改变游戏核心参数：
- `FPS`：游戏帧率（默认 20）。
- `BITE_CHANCE`：鱼靠近时的基础咬钩概率。
- `REEL_TIME_LIMIT`：QTE 收杆反应时间限制。
- `FISH_TYPES`：可自定义新增鱼类或垃圾，修改其符号、颜色、速度及分值。

## 🤝 参与贡献 (Contributing)

欢迎提交 Issue 和 Pull Request 来帮助完善本项目。具体可参考 [PROGRESS.md](PROGRESS.md) 了解当前项目的开发进度与未来规划。

## 📄 许可证 (License)

本项目基于 [MIT License](LICENSE) 开源，请自由使用、修改和分发。