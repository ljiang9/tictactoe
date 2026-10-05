"""tictactoe —— 终端井字棋，和一个永远输不了的 AI 对战。

你执 X，AI 执 O。默认难度下 AI 使用带 alpha-beta 剪枝的 minimax，
在 3x3 棋盘上这是理论最优的：你最多只能逼和，永远赢不了。
想要赢？用 --easy 切到随机模式（但赢了也别太骄傲）。
"""

import argparse
import random
import sys

EMPTY = " "
HUMAN = "X"
AI = "O"

WIN_LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # 行
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # 列
    (0, 4, 8), (2, 4, 6),            # 对角线
)


def winner(board):
    """返回获胜者 ('X'/'O')，平局或未结束返回 None。"""
    for a, b, c in WIN_LINES:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]
    return None


def game_over(board):
    return winner(board) is not None or EMPTY not in board


def minimax(board, is_max, alpha, beta):
    """minimax + alpha-beta。返回 (分数, 最佳落子)。AI(O) 为最大化方。"""
    w = winner(board)
    if w == AI:
        return 1, None
    if w == HUMAN:
        return -1, None
    if EMPTY not in board:
        return 0, None

    best_move = None
    if is_max:
        best = -2
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = AI
                score, _ = minimax(board, False, alpha, beta)
                board[i] = EMPTY
                if score > best:
                    best, best_move = score, i
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
        return best, best_move
    else:
        best = 2
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = HUMAN
                score, _ = minimax(board, True, alpha, beta)
                board[i] = EMPTY
                if score < best:
                    best, best_move = score, i
                beta = min(beta, best)
                if beta <= alpha:
                    break
        return best, best_move


def ai_move(board, easy=False):
    empties = [i for i in range(9) if board[i] == EMPTY]
    if easy:
        return random.choice(empties)
    _, move = minimax(board, True, -2, 2)
    return move


def render(board, show_numbers=False):
    """打印棋盘。show_numbers 时空位显示 1-9 方便输入。"""
    cells = []
    for i, v in enumerate(board):
        if v == EMPTY and show_numbers:
            cells.append(str(i + 1))
        else:
            cells.append(v if v != EMPTY else " ")
    rows = []
    for r in range(3):
        rows.append(" " + " | ".join(cells[r * 3:(r + 1) * 3]) + " ")
    return "\n-----------\n".join(rows)


def parse_human_move(text, board):
    """解析人类输入。返回 (落子位置, 错误信息)。"""
    text = text.strip()
    if not text.isdigit():
        return None, f"请输入 1-9 的数字，你输入了：{text!r}"
    pos = int(text) - 1
    if not 0 <= pos <= 8:
        return None, "数字必须在 1-9 之间"
    if board[pos] != EMPTY:
        return None, f"第 {pos + 1} 格已经被占了，换一个"
    return pos, None


def play_interactive(first="human", easy=False):
    board = [EMPTY] * 9
    turn = HUMAN if first == "human" else AI
    print("井字棋：你是 X，AI 是 O。" + ("AI 先手。" if turn == AI else "你先手。"))
    print("输入 1-9 落子（对应下面的格子编号）。Ctrl-C 退出。\n")
    while not game_over(board):
        print(render(board, show_numbers=True))
        print()
        if turn == HUMAN:
            while True:
                try:
                    text = input("你的回合（1-9）：")
                except (EOFError, KeyboardInterrupt):
                    print("\n已退出。")
                    return
                pos, err = parse_human_move(text, board)
                if err:
                    print("⚠️ " + err)
                    continue
                board[pos] = HUMAN
                break
        else:
            pos = ai_move(board, easy=easy)
            board[pos] = AI
            print(f"AI 落子：第 {pos + 1} 格")
        turn = AI if turn == HUMAN else HUMAN
    print(render(board))
    print()
    w = winner(board)
    if w == HUMAN:
        print("🎉 你赢了！（easy 模式不算数）" if easy else "🎉 你赢了？！这不应该发生，快截图！")
    elif w == AI:
        print("🤖 AI 获胜。minimax 是不可战胜的，再接再厉。")
    else:
        print("🤝 平局！面对最优 AI，这已经是最好的结果了。")


def play_demo():
    """演示一局脚本对战（人类走固定招式，展示流程不卡死）。"""
    board = [EMPTY] * 9
    human_script = [4, 0, 8, 2, 6]  # 中心、角……AI 会见招拆招
    turn, si = HUMAN, 0
    print("=== 演示对局（脚本走子）===\n")
    while not game_over(board):
        if turn == HUMAN:
            pos = human_script[si] if si < len(human_script) else next(
                i for i in range(9) if board[i] == EMPTY)
            si += 1
            if board[pos] != EMPTY:  # 脚本撞车就换空位
                pos = next(i for i in range(9) if board[i] == EMPTY)
            board[pos] = HUMAN
            print(f"你（脚本）落子：第 {pos + 1} 格")
        else:
            pos = ai_move(board)
            board[pos] = AI
            print(f"AI 落子：第 {pos + 1} 格")
        print(render(board))
        print()
        turn = AI if turn == HUMAN else HUMAN
    w = winner(board)
    print("结果：" + ("你赢" if w == HUMAN else "AI 赢" if w == AI else "平局"))
    return w


def selfplay():
    """AI 内战：双方最优，结果必然是平局。"""
    board = [EMPTY] * 9
    turn = HUMAN
    while not game_over(board):
        if turn == HUMAN:
            _, move = minimax(board, False, -2, 2)
            board[move] = HUMAN
        else:
            _, move = minimax(board, True, -2, 2)
            board[move] = AI
        turn = AI if turn == HUMAN else HUMAN
    return winner(board)


def main(argv=None):
    p = argparse.ArgumentParser(prog="tictactoe", description="终端井字棋：挑战永远输不了的 minimax AI。")
    p.add_argument("--first", choices=["human", "ai"], default="human", help="谁先手（默认 human）")
    p.add_argument("--easy", action="store_true", help="简单模式：AI 随机落子，可以赢")
    p.add_argument("--demo", action="store_true", help="演示一局脚本对战（非交互）")
    p.add_argument("--selfplay", action="store_true", help="AI 内战（非交互），验证最优对最优必为平局")
    args = p.parse_args(argv)

    if args.selfplay:
        w = selfplay()
        print("AI 内战结果：" + ("平局" if w is None else f"{w} 获胜"))
        if w is not None:
            print("error: 最优对最优出现了胜负，minimax 实现有 bug", file=sys.stderr)
            return 1
        return 0
    if args.demo:
        play_demo()
        return 0
    play_interactive(first=args.first, easy=args.easy)
    return 0


if __name__ == "__main__":
    sys.exit(main())
