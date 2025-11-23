"""Generate modernized markdown documentation."""

from typing import Dict, Any

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from ..config import get_model_name, get_gemini_api_key
from ..utils.logger import get_logger

logger = get_logger(__name__)


def generate_modernized_docs(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate modernized markdown documentation.

    Args:
        state: Current workflow state with original_content, analyzed_sections, research_results

    Returns:
        dict: Updated state with 'modernized_markdown' populated
    """
    try:
        llm = ChatOpenAI(
            model=get_model_name(),
            api_key=get_gemini_api_key(),
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )
        prompt = _create_generation_prompt(state)
        messages = [
            SystemMessage(content="You are an expert technical writer producing clean, modern markdown."),
            HumanMessage(content=prompt),
        ]
        response = llm.invoke(messages)
        raw_content = response.content if hasattr(response, "content") else str(response)
        modernized = _clean_markdown_output(raw_content)
        return {"modernized_markdown": modernized}
    except Exception as exc:
        logger.error("Failed to generate modernized docs: %s", exc, exc_info=True)
        return {"modernized_markdown": ""}


def _create_generation_prompt(state: Dict[str, Any]) -> str:
    """
    Create the generation prompt combining all context.

    Args:
        state: Current workflow state

    Returns:
        str: Formatted generation prompt
    """
    original = state.get("original_content", "")
    analyzed = state.get("analyzed_sections", [])
    research = state.get("research_results", [])

    original_snippet = original[:12000]

    analysis_lines = []
    for issue in analyzed:
        section = issue.get("section", "Unknown")
        description = issue.get("description", "")
        severity = issue.get("severity", "unknown")
        analysis_lines.append(f"- [{severity}] {section}: {description}")

    research_lines = []
    for item in research:
        issue = item.get("original_issue", {})
        section = issue.get("section", "Unknown")
        practices = item.get("current_practices", "")
        research_lines.append(f"- {section}: {practices}")

    return (
        "Rewrite the documentation using modern best practices.\n"
        "Requirements:\n"
        "- Use clear markdown with proper headings and lists.\n"
        "- Update outdated info and include modern tools/frameworks.\n"
        "- Provide improved structure and concise explanations.\n"
        "- Include code examples where helpful.\n"
        "- Add a 'Last Updated' section.\n"
        "- Include cross-references where relevant.\n\n"
        f"Original Documentation (truncated):\n{original_snippet}\n\n"
        f"Issues Identified:\n" + "\n".join(analysis_lines) + "\n\n"
        "Research Findings:\n" + "\n".join(research_lines)
    )


def _clean_markdown_output(content: str) -> str:
    """
    Clean and normalize markdown output.

    Args:
        content: Raw markdown from LLM

    Returns:
        str: Cleaned markdown
    """
    if not content:
        return ""

    cleaned = content.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        cleaned = cleaned.replace("markdown", "", 1).strip()
    return cleaned.strip()
