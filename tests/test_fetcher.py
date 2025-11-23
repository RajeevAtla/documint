import pytest

from src.tools.fetcher import fetch_documentation


def test_fetch_documentation_invalid_url():
    """Test with invalid URL."""
    with pytest.raises(ValueError):
        fetch_documentation("not-a-url")


@pytest.mark.skip(reason="Requires network access")
def test_fetch_documentation_success():
    """Test successful fetch (requires network)."""
    html, markdown = fetch_documentation("https://example.com")
    assert len(html) > 0
    assert len(markdown) > 0
    assert "example" in markdown.lower()
