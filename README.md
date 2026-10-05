# tictactoe

终端井字棋，和一个**永远输不了**的 AI 对战。

你执 X，AI 执 O。默认难度下 AI 使用带 alpha-beta 剪枝的 minimax 算法——在 3x3 棋盘上这是理论最优解：**你最多只能逼和，永远赢不了**。想体验赢的感觉？用 `--easy` 切到随机模式。

纯标准库，零依赖，离线可玩。

## 用法

```bash
python3 -m tictactoe              # 开始对战（你先手）
python3 -m tictactoe --first ai   # AI 先手
python3 -m tictactoe --easy       # 简单模式：AI 随机落子，可以赢
python3 -m tictactoe --demo       # 演示一局脚本对战（非交互）
python3 -m tictactoe --selfplay   # AI 内战，验证最优对最优必为平局
```

棋盘空位会显示 1-9 的编号，直接输入数字落子。输错、输入已被占用的格子会中文提示重输，不会崩溃。

## 设计取舍

- minimax 搜索整棵博弈树（3x3 最多 9! 种局面，实际剪枝后极小），每一步都是理论最优。
- `--easy` 模式 AI 纯随机，README 明确标注"赢了也别太骄傲"。
- 交互输入用 `parse_human_move` 做校验：非数字、越界、占位都有中文提示。

## 已知局限（诚实版）

- 3x3 井字棋的 minimax 是** trivial 的**：状态空间太小，谈不上什么 AI 技术含量，纯属娱乐。
- 终端交互，没有图形界面；`--demo`/`--selfplay` 是给脚本和 CI 用的非交互入口。
- 没有记分/排行榜：想长期虐 AI 请自己数。

## 许可证

MIT，Copyright (c) 2026 ljiang9。
