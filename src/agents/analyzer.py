"""Analyze documentation content for outdated information."""

from typing import Dict, Any

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from ..config import get_model_name, get_gemini_api_key
from ..utils.json_parser import extract_json_from_response
from ..utils.logger import get_logger

logger = get_logger(__name__)


def analyze_content(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze documentation content for outdated information and issues.

    Args:
        state: Current workflow state containing 'original_content'

    Returns:
        dict: Updated state with 'analyzed_sections' populated
    """
    content = state.get("original_content", "")
    truncated = content[:8000]

    try:
        llm = ChatOpenAI(
            model=get_model_name(),
            api_key=get_gemini_api_key(),
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )

        prompt = _create_analysis_prompt(truncated)
        messages = [
            SystemMessage(
                content="You are a senior technical writer and software architect. Identify modernization issues."
            ),
            HumanMessage(content=prompt),
        ]

        response = llm.invoke(messages)
        parsed = extract_json_from_response(response.content if hasattr(response, "content") else str(response))
        analyzed_sections = parsed if isinstance(parsed, list) else []

        logger.info("Analysis completed with %d issues", len(analyzed_sections))
        return {"analyzed_sections": analyzed_sections}
    except Exception as exc:
        logger.error("Failed to analyze content: %s", exc, exc_info=True)
        return {"analyzed_sections": []}


def _create_analysis_prompt(content: str) -> str:
    """
    Create the analysis prompt for the LLM.

    Args:
        content: Documentation content to analyze

    Returns:
        str: Formatted prompt
    """
    return (
        "Analyze the following technical documentation for modernization issues.\n"
        "Identify outdated information, missing best practices, unclear structure, and technical debt.\n"
        "Return JSON in the format:\n"
        '[{"section": str, "issue_type": str, "description": str, "severity": "high|medium|low"}]\n\n'
        f"CONTENT:\n{content}"
    )
