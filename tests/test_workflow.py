
from src.agents.workflow import build_workflow, fetch_node


def test_build_workflow():
    """Test workflow construction."""
    workflow = build_workflow()
    assert workflow is not None


def test_fetch_node_with_invalid_url():
    """Test fetch node error handling."""
    state = {"url": "invalid-url"}
    result = fetch_node(state)
    assert "error" in result
