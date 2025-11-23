"""JSON parsing utilities for LLM responses."""

import json
import re
from typing import Any, Optional

from .logger import get_logger

logger = get_logger(__name__)


def extract_json_from_response(response: str) -> Optional[Any]:
    """
    Extract JSON content from an LLM response string.

    Supports JSON inside code fences, inline objects, and arrays.

    Args:
        response: Raw LLM response text.

    Returns:
        Parsed JSON object or None if parsing fails.
    """
    if not response:
        return None

    # Prefer fenced code blocks labeled as json
    fenced = re.findall(r"```(?:json)?\\s*(\\{.*?\\}|\\[.*?\\])\\s*```", response, re.DOTALL)
    candidates = fenced or re.findall(r"(\\{.*\\}|\\[.*\\])", response, re.DOTALL)

    for candidate in candidates:
        cleaned = candidate.strip()
        parsed = safe_json_parse(cleaned)
        if parsed is not None:
            return parsed

    logger.warning("Failed to extract JSON from response")
    return None


def safe_json_parse(text: str) -> Optional[Any]:
    """
    Safely parse a JSON string.

    Args:
        text: JSON string to parse.

    Returns:
        Parsed JSON object or None if invalid.
    """
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None
