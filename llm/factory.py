"""
LLM 工厂模块
根据配置创建 LangChain ChatOpenAI 实例
"""
from langchain_openai import ChatOpenAI

from llm import LLMConfig


def create_llm(config: LLMConfig | None = None) -> ChatOpenAI:
    """
    创建 LLM  实例
    :arg
    :param config: LLM 配置，如果为 None 则使用默认配置
    :return: ChatOpenAI 实例
    """
    if config is None:
        config = LLMConfig()

    llm = ChatOpenAI(
        base_url=config.base_url,
        api_key=config.api_key,
        model=config.model_name,
        temperature=config.temperature,
        max_tokens=config.max_tokens,
        timeout=config.timeout,
        max_retries=config.max_retries,
    )

    return llm


def create_llm_with_params(
        base_url: str | None = None,
        api_key: str | None = None,
        model_name: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
) -> ChatOpenAI:
    """
    使用自定义参数创建 LLM 实例
    :param base_url:
    :param api_key:
    :param model_name:
    :param temperature:
    :param max_tokens:
    :return:
    """
    import os
    config = LLMConfig(
        base_url=base_url or os.getenv("LLM_BASE_URL"),
        api_key=api_key or os.getenv("LLM_API_KEY"),
        model_name=model_name or os.getenv("LLM_MODEL_NAME"),
        temperature=temperature or float(os.getenv("LLM_TEMPERATURE", "0.7")),
        max_tokens=max_tokens or int(os.getenv("LLM_MAX_TOKENS", "2048")),
    )

    return create_llm(config)
