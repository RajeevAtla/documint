"""Markdown utility functions."""

import re
from typing import List, Tuple


def clean_markdown(content: str) -> str:
    """
    Normalize markdown content by trimming whitespace and collapsing blanks.

    Args:
        content: Raw markdown string.

    Returns:
        Cleaned markdown string.
    """
    if not content:
        return ""

    cleaned = re.sub(r"[ \\t]+\\n", "\n", content)
    cleaned = re.sub(r"\\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def extract_code_blocks(content: str) -> List[Tuple[str, str]]:
    """
    Extract code blocks from markdown.

    Args:
        content: Markdown content.

    Returns:
        List of tuples (language, code).
    """
    if not content:
        return []

    pattern = re.compile(r"```(?P<lang>[\\w+-]*)\\n(?P<code>.*?)```", re.DOTALL)
    blocks = []
    for match in pattern.finditer(content):
        lang = match.group("lang") or ""
        code = match.group("code").strip()
        blocks.append((lang, code))
    return blocks
