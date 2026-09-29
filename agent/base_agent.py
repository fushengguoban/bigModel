import json
from typing import Optional

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI

from model.player import Player
from prompts.role_prompts import get_role_system_prompt


class BaseAgent:
    """Ai 智能体基类"""

    def __init__(self, player: Player, llm: ChatOpenAI):
        """初始化 Agent

        """
        self.player = player
        self.llm = llm
        self.system_prompt = get_role_system_prompt(player.role)

    async def invoke(self, prompt: str, system_prompt: Optional[str] = None, show_debug: bool = False) -> str:
        """
        调用 LLM
        :param prompt:    用户提示词
        :param system_prompt: 系统提示词
        :param show_debug: 是否显示调试信息
        :return:
        """
        messages = [
            SystemMessage(content=system_prompt or self.system_prompt),
            HumanMessage(content=prompt)
        ]

        if show_debug:
            print(f"\n[DEBUG] {self.player.name} 的 LLM 输入:")
            print(f"  系统提示：{self.system_prompt[:100]}...")
            print(f"  用户提示：{prompt[:200]}...")

        response = await self.llm.ainvoke(messages)

        if show_debug:
            print(f"\n[DEBUG] {self.player.name} 的 LLM 原始输出:")
            print(f"  {response.content[:500]}...")

        return response.content

    async def invoke_json(self, prompt: str, system_prompt: Optional[str] = None, show_debug: bool = False) -> dict:
        """
         调用 LLM 并解析 JSON 响应

        Args:
            prompt: 用户提示词
            system_prompt: 系统提示词
            show_debug: 是否显示调试信息

        Returns:
            解析后的字典
        """
        response_text = await self.invoke(prompt, system_prompt, show_debug)

        try:
            # 查找 JSON 块
            start_idx = response_text.find("{")
            end_ind = response_text.find("}") + 1
            if start_idx >= 0 and end_ind > start_idx:
                json_str = response_text[start_idx:end_ind]
                result = json.loads(json_str)

                if show_debug:
                    print(f"\n[DEBUG] JSON 解析结果:")
                    print(f"  {result}")
                return result
            else:
                return {"error": "无法解析 JSON", "raw_response": response_text}

        except json.JSONDecodeError as e:
            return {
                "error": f"JSON 解析失败：{str(e)}",
                "raw_response": response_text,
            }

    def add_memory(self, memory: str):
        """添加记忆"""
        self.player.add_memory(memory)

    def get_memories(self, count: int = 5) -> list[str]:
        """获取最近的记忆"""
        return self.player.get_last_memories(count)

    def clear_memories(self):
        """清空记忆"""
        self.player.memory = []


class WerewolfAgent(BaseAgent):
    """狼人 AI 智能体"""

    def __init__(self, player: Player, llm: ChatOpenAI, teammate_ids: list[int]):
        super().__init__(player, llm)
        self.teammate_ids = teammate_ids


class SeerAgent(BaseAgent):
    """预言家 AI 智能体"""

    def __int__(self, player: Player, llm: ChatOpenAI):
        super().__int__(player, llm)
        self.checked_players: list[int] = []

    def add_checked_record(self, player_id: int):
        """添加查验记录"""
        if player_id not in self.checked_players:
            self.checked_players.append(player_id)


class VillagerAgent(BaseAgent):
    """村民智能体"""
    pass


class WitchAgent(BaseAgent):
    """女巫智能体"""

    def __init__(self, player: Player, llm: ChatOpenAI, has_save_potion: bool = True, has_poison_potion: bool = True):
        super().__init__(player, llm)
        self.has_save_potion = has_save_potion
        self.has_poison_potion = has_poison_potion


class HunterAgent(BaseAgent):
    pass
