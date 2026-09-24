from langchain_openai import ChatOpenAI


class BaseAgent:
    """Ai 智能体基类"""

    def __init__(self, player: Player, llm: ChatOpenAI):
