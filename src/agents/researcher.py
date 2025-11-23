"""Research best practices for identified issues."""

from datetime import datetime
from typing import Dict, Any, List

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage

from ..config import get_model_name
from ..utils.logger import get_logger

logger = get_logger(__name__)


def research_best_practices(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Research current best practices for identified documentation issues.

    Args:
        state: Current workflow state containing 'analyzed_sections'

    Returns:
        dict: Updated state with 'research_results' populated
    """
    issues = state.get("analyzed_sections", [])
    prioritized = _prioritize_issues(issues)
    results: List[Dict[str, Any]] = []

    try:
        llm = ChatAnthropic(model=get_model_name())
    except Exception as exc:
        logger.error("Failed to initialize LLM for research: %s", exc, exc_info=True)
        return {"research_results": []}

    for issue in prioritized:
        prompt = _create_research_prompt(issue)
        try:
            response = llm.invoke([HumanMessage(content=prompt)])
            current_practices = response.content if hasattr(response, "content") else str(response)
            results.append(
                {
                    "original_issue": issue,
                    "current_practices": current_practices,
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                }
            )
        except Exception as exc:
            logger.warning("Research failed for issue %s: %s", issue, exc, exc_info=True)
            continue

    logger.info("Research completed for %d issues", len(results))
    return {"research_results": results}


def _prioritize_issues(analyzed_sections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Sort issues by severity and return top 5.

    Args:
        analyzed_sections: List of analyzed issues

    Returns:
        List[Dict]: Top 5 issues sorted by severity
    """
    severity_order = {"high": 3, "medium": 2, "low": 1}
    sorted_issues = sorted(
        analyzed_sections,
        key=lambda issue: severity_order.get(issue.get("severity", "").lower(), 0),
        reverse=True,
    )
    return sorted_issues[:5]


def _create_research_prompt(issue: Dict[str, Any]) -> str:
    """
    Create research prompt for a specific issue.

    Args:
        issue: Single issue dict from analyzed_sections

    Returns:
        str: Formatted research prompt
    """
    section = issue.get("section", "Unknown section")
    description = issue.get("description", "No description provided")

    return (
        f"Provide current best practices to address the following documentation issue:\n"
        f"Section: {section}\n"
        f"Issue: {description}\n"
        "Include modern tools/frameworks, recommended approaches, and key references. Keep the answer concise."
    )
