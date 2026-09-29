from typing import Dict

from langchain_openai import ChatOpenAI
from agent.base_agent import (
    BaseAgent,
    WerewolfAgent,
    SeerAgent,
    VillagerAgent,
    WitchAgent,
    HunterAgent,
)
from model import Player
from model.enums import Role


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

    def register_player(self, player: Player):
        """
        注册玩家对应的 agent
        :param player:
        :return:
        """
        if player.role == Role.WEREWOLF:
            agent = WerewolfAgent(player, self.llm, [])
        elif player.role == Role.SEER:
            agent = SeerAgent(player, self.llm)
        elif player.role == Role.WITCH:
            agent = WitchAgent(player, self.llm)
        elif player.role == Role.HUNTER:
            agent = HunterAgent(player, self.llm)
        else:
            agent = VillagerAgent(player, self.llm)

        self.agents[player.player_id] = agent

    def setup_werewolf_teams(self, werewolf_ids: list[int]):
        """
        设置狼人团队关系
        :param werewolf_ids:
        :return:
        """


