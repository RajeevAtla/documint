"""Validate and assess quality of modernized documentation."""

from typing import Dict, Any

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

from ..config import get_model_name
from ..utils.json_parser import extract_json_from_response
from ..utils.logger import get_logger

logger = get_logger(__name__)


def check_quality(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Assess quality of modernized documentation.

    Args:
        state: Current workflow state with original_content and modernized_markdown

    Returns:
        dict: Updated state with 'quality_report' populated
    """
    original = state.get("original_content", "")[:2000]
    modernized = state.get("modernized_markdown", "")[:2000]

    try:
        llm = ChatAnthropic(model=get_model_name())
        prompt = _create_quality_prompt(original, modernized)
        messages = [
            SystemMessage(content="You are a meticulous technical documentation reviewer."),
            HumanMessage(content=prompt),
        ]
        response = llm.invoke(messages)
        parsed = extract_json_from_response(response.content if hasattr(response, "content") else str(response))

        if isinstance(parsed, dict):
            scores = parsed.get("scores", {})
            suggestions = parsed.get("suggestions", [])
        else:
            scores, suggestions = {}, []

        average = _calculate_average_score(scores)
        quality_report = {"scores": scores, "suggestions": suggestions, "average_score": average}
        return {"quality_report": quality_report}
    except Exception as exc:
        logger.error("Quality check failed: %s", exc, exc_info=True)
        return {"quality_report": {"scores": {}, "suggestions": [], "average_score": 0}}


def _create_quality_prompt(original: str, modernized: str) -> str:
    """
    Create quality assessment prompt.

    Args:
        original: Original documentation (truncated)
        modernized: Modernized documentation (truncated)

    Returns:
        str: Formatted quality assessment prompt
    """
    return (
        "Compare the original and modernized documentation snippets.\n"
        "Score each category 0-10 and provide suggestions.\n"
        "Return JSON: {\"scores\": {\"completeness\": int, \"clarity\": int, "
        "\"technical_accuracy\": int, \"modernization_effectiveness\": int}, "
        "\"suggestions\": [\"...\"]}\n\n"
        f"Original:\n{original}\n\nModernized:\n{modernized}"
    )


def _calculate_average_score(scores: Dict[str, float]) -> float:
    """
    Calculate average quality score.

    Args:
        scores: Dict of score name to value

    Returns:
        float: Average score
    """
    if not scores:
        return 0.0
    values = [float(v) for v in scores.values() if isinstance(v, (int, float))]
    if not values:
        return 0.0
    return round(sum(values) / len(values), 1)
