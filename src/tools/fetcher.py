"""Tools for fetching and converting web documentation."""

import re
from typing import Tuple

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

from ..utils.logger import get_logger

logger = get_logger(__name__)


def fetch_documentation(url: str, timeout: int = 30) -> Tuple[str, str]:
    """
    Fetch HTML documentation and convert to markdown.

    Args:
        url: Documentation URL to fetch.
        timeout: Request timeout in seconds.

    Returns:
        tuple: (raw_html, markdown_content)

    Raises:
        requests.RequestException: If fetch fails.
        ValueError: If URL is invalid.
    """
    if not _validate_url(url):
        raise ValueError(f"Invalid URL: {url}")

    logger.info("Fetching documentation from %s", url)
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")
    _remove_unwanted_elements(soup)
    main_content = _extract_main_content(soup)

    html_content = main_content.decode() if hasattr(main_content, "decode") else str(main_content)
    markdown_content = md(html_content, heading_style="ATX")
    markdown_content = markdown_content.replace("\r\n", "\n")

    logger.info("Fetched %s bytes of HTML", len(response.text))
    return response.text, markdown_content


def _validate_url(url: str) -> bool:
    """
    Validate URL format.

    Args:
        url: URL to validate.

    Returns:
        bool: True if valid.

    Raises:
        ValueError: If URL is invalid.
    """
    if not url or not isinstance(url, str):
        raise ValueError("URL must be a non-empty string")

    pattern = re.compile(r"^https?://[\\w.-]+(?:\\.[\\w.-]+)+.*$")
    if not pattern.match(url):
        raise ValueError(f"Invalid URL: {url}")
    return True


def _extract_main_content(soup: BeautifulSoup) -> BeautifulSoup:
    """
    Extract main content from parsed HTML.

    Args:
        soup: BeautifulSoup parsed HTML.

    Returns:
        BeautifulSoup: Main content element.
    """
    for selector in ["main", "article", ".content", ".documentation"]:
        found = soup.select_one(selector)
        if found:
            return found
    return soup.body or soup


def _remove_unwanted_elements(soup: BeautifulSoup) -> None:
    """
    Remove navigation, script, style, and layout elements.

    Args:
        soup: BeautifulSoup parsed HTML.
    """
    for tag_name in ["script", "style", "nav", "header", "footer"]:
        for tag in soup.find_all(tag_name):
            tag.decompose()
