# 项目架构与设计规范 (Project Structure & Architecture)

本文档面向开发者，详细阐述 `Terminal Fishing Game` 的目录结构、模块职责以及核心架构设计。理解本文档将有助于你进行二次开发或系统扩展。

## 📁 目录结构 (Directory Tree)

```text
terminal-fishing/
├── run.py                 # 顶层入口脚本，配置 sys.path 并拉起游戏
├── README.md              # 用户手册与项目简介
├── PROGRESS.md            # 开发进度与里程碑规划
├── STRUCTURE.md           # [本文档] 架构与目录说明
├── .gitignore             # Git 忽略配置
└── fishing_game/          # 核心代码包
    ├── __init__.py        
    ├── main.py            # Curses 环境初始化与底层死循环包装
    ├── game.py            # 游戏主逻辑、状态机引擎、事件分发中心
    ├── config.py          # 全局配置、常量、枚举项、颜色对定义
    ├── utils.py           # 无副作用的纯函数工具箱 (绘图保护、物理算法)
    └── entities/          # 游戏内具象化实体 (Entities) 目录
        ├── __init__.py
        ├── water.py       # 水面/背景逻辑封装，波纹动画引擎
        ├── fish.py        # 鱼类 AI、属性(速度/稀有度)与渲染
        └── rod.py         # 鱼竿、鱼线、浮标状态与抛物线动画引擎
```

---

## 🧩 核心模块职责说明 (Module Responsibilities)

### 1. `run.py` & `fishing_game/main.py` (基础设施层)
- **`run.py`**: 提供一个开箱即用的跨平台启动点，处理 Python 模块路径（防止 `ImportError`）。
- **`main.py`**: 负责底层终端环境的初始化与回收（使用 `curses.wrapper`）。它配置了非阻塞输入 (`stdscr.nodelay(1)`)，设定了全局帧率，并驱动着最高层的 `while True` 获取输入、调用 `game.update()` 与 `game.draw()`。

### 2. `fishing_game/game.py` (业务控制层)
- 这是整个游戏的大脑，实例化并持有所有 `Entities`。
- **状态机 (State Machine)** 管理：维护 `self.state`，决定游戏当前处于哪个阶段（菜单、待机、抛竿、等待咬钩、QTE阶段）。
- **生命周期调度**：负责在每一帧统一调用实体层的 `update()` 和 `draw()` 方法。
- **事件中心**：统一处理来自用户的键盘输入 (`handle_input`)，并根据当前状态进行事件路由（如在 `BITING` 状态下按回车触发 `REELING`）。

### 3. `fishing_game/entities/` (实体数据层)
该目录采用面向对象设计 (OOP)，将屏幕上可见的独立物体进行封装：
- **`water.py (Water)`**: 管理一个二维数组来保存水面字符状态，通过随机数引擎制造波浪效果 (`update` 方法)，并在屏幕特定坐标渲染自身。
- **`fish.py (Fish)`**: 包含鱼的数据模型（位置、速度、朝向、价值、颜色），处理自身的越界检测 (`is_out_of_bounds`) 以及自然游动轨迹。
- **`rod.py (Rod)`**: 维护鱼钩 (`hook_x`, `hook_y`) 的实时坐标，管理抛物线动画帧队列，并在不同游戏状态下渲染不同形态的浮标或警告符。

### 4. `fishing_game/config.py` & `utils.py` (公共支撑层)
- **`config.py`**: 集中管理所有"魔法数字" (Magic Numbers)。包括物理碰撞阈值、概率基数 (`FISH_SPAWN_CHANCE`, `BITE_CHANCE`)、配色方案等。修改此文件可直接改变游戏难度和表现。
- **`utils.py`**: 包含与具体业务解耦的纯函数。如：
  - `draw_str`: 封装带有边界安全检查的终端字符串绘制函数，防止因为写入终端右下角导致 `curses.error` 崩溃。
  - `calculate_parabola`: 基于贝塞尔曲线 (Bézier Curve) 的抛物线插值计算器。

---

## 🔄 数据流与核心架构 (Architecture Data Flow)

本游戏采用类似 **ECS (Entity-Component-System) 简化版** 与 **状态模式 (State Pattern)** 结合的架构：

1. **Input (输入阶段)**: `main.py` 捕获键盘中断，传递给 `Game.handle_input(key)`。
2. **Update (更新阶段)**: `Game.update()` 被调用。
   - 环境更新：触发 `water.update()`。
   - 实体状态流转：根据物理帧率更新鱼的坐标 `fish.move()`，更新鱼钩动画 `rod.update_cast()`。
   - 碰撞与规则判定：计算鱼群坐标与鱼钩坐标的曼哈顿距离/欧几里得距离，结合 `config.BITE_CHANCE` 判定是否触发状态切换（进入 `BITING` 状态）。
3. **Render (渲染阶段)**: `Game.draw()` 被调用。
   - 执行 `stdscr.erase()` 清空缓冲区（不使用 `clear` 以避免屏幕闪烁）。
   - 按 Z-Index 深度（自下而上）依次调用 `water.draw()`, `fish.draw()`, `rod.draw()` 和 UI 层的 `draw_str()`。
   - 最终执行 `stdscr.refresh()` 将双缓冲推送到物理终端。
