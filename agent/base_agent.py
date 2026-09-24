from langchain_openai import ChatOpenAI

from model.player import Player


class BaseAgent:
    """Ai 智能体基类"""

    def __init__(self, player: Player, llm: ChatOpenAI):
        """初始化 Agent

        """
        self.player=player
        self.llm=llm
        self.system_prompt= get_role_system_prompt()
