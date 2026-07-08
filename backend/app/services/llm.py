"""LLM service — Anthropic Claude for RAG and advisory."""

from __future__ import annotations

from app.core.config import settings


async def generate_text(system_prompt: str, user_prompt: str) -> str | None:
    """Call Claude when ANTHROPIC_API_KEY is configured; otherwise return None."""
    if not settings.anthropic_api_key:
        return None

    try:
        from langchain_anthropic import ChatAnthropic
        from langchain_core.messages import HumanMessage, SystemMessage

        llm = ChatAnthropic(
            model=settings.llm_model,
            api_key=settings.anthropic_api_key,
            temperature=0.2,
            max_tokens=1024,
        )
        response = await llm.ainvoke(
            [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt),
            ]
        )
        content = response.content
        return content if isinstance(content, str) else str(content)
    except Exception:
        return None


def is_llm_available() -> bool:
    return bool(settings.anthropic_api_key)
