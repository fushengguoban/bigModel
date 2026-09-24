from typing import Dict

from model.enums import Role




ROLE_PROMPTS:Dict[Role,str]={

}


def get_role_system_prompt(role:Role)->str:
    """
    获取角色的系统提示词

    Args:
        role: 角色类型

    Returns:
        系统提示词字符串
    """
    return ROLE_PROMPTS.get(
        role, f"你是一个狼人杀游戏中的{role.value}玩家。请根据游戏规则进行游戏。"
    )