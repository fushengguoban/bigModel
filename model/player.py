from dataclasses import dataclass, field
from typing import Optional

from model.enums import Role


@dataclass
class Player:
    """玩家基类"""
    player_id: int  # 玩家ID
    name: str  # 玩家姓名
    role: Role  # 角色身份
    is_alive: bool = True  # 是否存活
    team: str = ""  # 阵营

    # 游戏状态相关
    checked_by_seer: bool = False  # 是否被预言家验证过
    seer_result: Optional[Role] = None  # 如果被查验，查验结果
    witch_saved: bool = False  # 是否被女巫拯救过
    hunter_triggered: bool = False  # 是否已发动过猎人技能

    # 记忆和上下文
    memory: list[str] = field(default_factory=list)  # 记忆列表
    known_info: dict = field(default_factory=dict)  # 已知信息

    # 关键游戏事件记录
    important_events: list[dict] = field(default_factory=list)  # 重要事件列表

    def __post_init__(self):
        """初始化阵营"""
        if self.role == Role.WEREWOLF:
            self.team = "狼人阵营"
        else:
            self.team = "好人阵营"

    def add_memory(self, memory: str):
        """添加记忆"""
        self.memory.append(memory)

    def get_last_memories(self, count: int = 10) -> list[str]:
        """获取最近的记忆"""
        return self.memory[-count:] if len(self.memory) > count else self.memory

    def eliminate(self):
        """标记玩家死亡/出局 """
        self.is_alive = False

    def add_important_event(self, event_type: str, round_number: int, details: str):
        """
        添加重要事件记录
        :param event_type: 事件类型（如 'seer_check', 'witch_save', 'vote_eliminated'）
        :param round_number: 发生的轮次
        :param details:
        :return:
        """
        self.important_events.append({
            'type': event_type,
            'round': round_number,
            'details': details
        })


