from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime

from model import Player
from model.enums import GamePhase, Role


@dataclass
class NightAction:
    """夜晚行动记录"""
    actor_id: int
    action_type: str
    target_id: Optional[int] = None
    result: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class DayDiscussion:
    """白天发炎记录"""
    round_number: int
    speaker_id: int
    speech_text: str
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class VoteRecord:
    """投票记录"""
    round_number: int
    voter_id: int
    vote_target: Optional[int]
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class GameState:
    """
    游戏状态类
    """
    current_phase: GamePhase = GamePhase.NOT_STARTED
    current_round: int = 0
    game_log: list[str] = field(default_factory=list)

    players: dict[int, Player] = field(default_factory=dict)
    alive_players: list[int] = field(default_factory=list)
    werewolf_players: list[int] = field(default_factory=list)

    night_actions: list[NightAction] = field(default_factory=list)
    night_kill_target: Optional[int] = None
    seer_check_target: Optional[int] = None
    seer_check_result: Optional[Role] = None  # 预言家查验结果
    witch_used_save: bool = False  # 女巫是否使用解药
    witch_used_poison: bool = False  # 女巫是否使用毒药
    witch_save_target: Optional[int] = None  # 女巫救的目标
    witch_poison_target: Optional[int] = None  # 女巫毒的目标

    # 白天流程
    discussion_order: list[int] = field(default_factory=list)  # 发言顺序
    current_speaker_index: int = 0  # 当前发言者索引
    day_discussions: list[DayDiscussion] = field(default_factory=list)  # 发言记录
    vote_records: list[VoteRecord] = field(default_factory=list)  # 投票记录
    vote_eliminated: Optional[int] = None  # 被投票放逐的玩家

    # 死亡信息
    deaths_this_night: list[int] = field(default_factory=list)  # 今晚死亡玩家
    deaths_today: list[int] = field(default_factory=list)  # 今天死亡玩家
    eliminated_players: list[int] = field(default_factory=list)  # 被放逐玩家

    # 游戏结束信息
    winner: Optional[str] = None  # 获胜阵营
    game_end_reason: Optional[str] = None  # 游戏结束原因

    def add_player(self, player: Player):
        """添加玩家"""
        self.players[player.player_id] = player
        if player.is_alive:
            self.alive_players.append(player.player_id)

        if player.role == Role.WEREWOLF:
            self.werewolf_players.append(player.player_id)

    def get_player(self, player_id: int) -> Optional[Player]:
        """获取玩家"""
        return self.players.get(player_id)

    def get_alive_player(self, player_id: int) -> Optional[Player]:
        """获取存活玩家"""
        player = self.players.get(player_id)
        if player and player.is_alive:
            return player
        return None

    def remove_player(self, play_id: int):
        """移除死亡玩家"""
        if play_id in self.alive_players:
            self.alive_players.remove(play_id)
        if play_id in self.werewolf_players:
            self.werewolf_players.remove(play_id)
        player = self.players.get(play_id)
        if player:
            player.eliminate()

    def add_game_log(self, message: str):
        """添加游戏日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.game_log.append(f"[{timestamp}] {message}")

    def get_werewolf_team(self) -> list[Player]:
        """获取狼人团队"""
        return [
            self.players[wid] for wid in self.werewolf_players if wid in self.alive_players
        ]

    def to_dict(self) -> dict:
        return {
            "current_phase": self.current_phase.value,
            "current_round": self.current_round,
            "alive_players": self.alive_players,
            "werewolf_players": self.werewolf_players,
            "deaths_this_night": self.deaths_this_night,
            "eliminated_players": self.eliminated_players,
            "winner": self.winner,
            "game_end_reason": self.game_end_reason,
        }


