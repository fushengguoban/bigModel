from typing import Optional

from llm.config import LLMConfig


class GameViewer:
    """游戏查看器--上帝视角"""

    def __init__(self,
                 llm_config: Optional[LLMConfig] = None,
                 log_level: str = "INFO",
                 show_model_debug: bool = False):
        print("初始化游戏查看器")
