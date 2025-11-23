"""State schema for LangGraph workflow."""

from typing import TypedDict, List, Dict, Any, Optional

from langgraph.graph import add_messages


class DocumentState(TypedDict):
    """
    State schema for the documentation modernization workflow.

    Attributes:
        url: Source documentation URL
        raw_html: Original HTML content
        original_content: Original documentation as markdown
        analyzed_sections: List of identified issues
        research_results: List of research findings for each issue
        modernized_markdown: Final modernized documentation
        quality_report: Quality assessment scores and suggestions
        messages: Conversation history (managed by add_messages)
        error: Optional error message if workflow fails
    """

    url: str
    raw_html: str
    original_content: str
    analyzed_sections: List[Dict[str, Any]]
    research_results: List[Dict[str, Any]]
    modernized_markdown: str
    quality_report: Dict[str, Any]
    messages: List[Any]
    error: Optional[str]


DocumentState.__annotations__["messages"] = add_messages(list)
