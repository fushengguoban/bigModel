from typing import Optional

from llm import LLMConfig, create_llm


class GameViewer:
    """游戏查看器--上帝视角"""

    def __init__(
            self,
            llm_config: Optional[LLMConfig] = None,
            log_level: str = "INFO",
            show_model_debug: bool = False
    ):
        """初始化游戏查看器"""
        if llm_config is None:
            llm_config = LLMConfig()
        self.llm = create_llm(llm_config)
        self.show_model_debug = show_model_debug

        # 初始化组件
        self.agent_manager = AgentManager()
        print("初始化游戏查看器")
