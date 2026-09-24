from cli.game_viewer import GameViewer

"""
狼人杀AI游戏，
用户只控制：开始，投票，下一轮
其余全部AI自动运行
"""


def main():
    """主函数"""
    print("=" * 70)
    print("狼人杀 AI 游戏系统 - 上帝视角观测模式")
    print("=" * 70)
    print()
    print("游戏说明:")
    print("  - 9 个 AI 玩家自动进行对局")
    print("  - 您以上帝视角观测完整流程")
    print("  - 您可以控制：开始游戏、开启投票、进入下一轮")
    print()

    # 检查环境变量
    import os
    if not os.getenv("LLM_API_KEY"):
        print("[提示] 未设置 LLM_API_KEY 环境变量")
        print("将进入测试模式（跳过 AI 调用）")
        print()

    # 创建游戏查看器
    viewer = GameViewer()
    print("正在初始化游戏...")
    viewer.setup_game()


if __name__ == "__main__":
    main()
