"""LangGraph workflow for documentation modernization."""

from typing import Dict, Any

from langgraph.graph import StateGraph, END

from .state import DocumentState
from .analyzer import analyze_content
from .researcher import research_best_practices
from .generator import generate_modernized_docs
from .quality_checker import check_quality
from ..tools.fetcher import fetch_documentation
from ..utils.logger import get_logger

logger = get_logger(__name__)


def fetch_node(state: DocumentState) -> Dict[str, Any]:
    """
    Fetch documentation from URL.

    Args:
        state: Current workflow state with 'url'

    Returns:
        dict: Updated state with raw_html and original_content
    """
    url = state.get("url", "")
    try:
        html, markdown = fetch_documentation(url)
        return {"raw_html": html, "original_content": markdown}
    except Exception as exc:
        logger.error("Failed to fetch URL %s: %s", url, exc, exc_info=True)
        return {"error": str(exc)}


def error_handler(state: DocumentState) -> Dict[str, Any]:
    """
    Handle errors in the workflow.

    Args:
        state: Current workflow state

    Returns:
        dict: State with error information
    """
    logger.error("Workflow encountered error: %s", state.get("error"))
    return state


def build_workflow() -> Any:
    """
    Build and compile the LangGraph workflow.

    Returns:
        Compiled LangGraph workflow
    """
    graph = StateGraph(DocumentState)

    graph.add_node("fetch", fetch_node)
    graph.add_node("analyze", analyze_content)
    graph.add_node("research", research_best_practices)
    graph.add_node("generate", generate_modernized_docs)
    graph.add_node("quality_check", check_quality)

    graph.set_entry_point("fetch")
    graph.add_edge("fetch", "analyze")
    graph.add_edge("analyze", "research")
    graph.add_edge("research", "generate")
    graph.add_edge("generate", "quality_check")
    graph.add_edge("quality_check", END)

    workflow = graph.compile()
    logger.info("Workflow built successfully")
    return workflow


def run_workflow(url: str) -> Dict[str, Any]:
    """
    Convenience function to run the complete workflow.

    Args:
        url: Documentation URL to process

    Returns:
        dict: Final state after workflow completion
    """
    workflow = build_workflow()
    initial_state: DocumentState = {
        "url": url,
        "raw_html": "",
        "original_content": "",
        "analyzed_sections": [],
        "research_results": [],
        "modernized_markdown": "",
        "quality_report": {},
        "messages": [],
        "error": None,
    }
    return workflow.invoke(initial_state)
