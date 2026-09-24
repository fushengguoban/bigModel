from typing import Dict

from langchain_openai import ChatOpenAI


class AgentManager:
    """agent 管理类"""

    def __init__(self, llm: ChatOpenAI):
        """
        初始化 Agent 管理器
        :param llm:
        """
        self.llm = llm
        self.agents: Dict[int, BaseAgent] = {}
        self.werewolf_teams: Dict[int, list[int]] = {}
