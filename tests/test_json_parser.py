import pytest

from src.utils.json_parser import extract_json_from_response, safe_json_parse


def test_extract_json_from_markdown():
    """Test JSON extraction from markdown code blocks."""
    response = 'Here is data: ```json\n{"key": "value"}\n```'
    result = extract_json_from_response(response)
    assert result == {"key": "value"}


def test_extract_json_from_plain_text():
    """Test JSON extraction from plain text."""
    response = 'The result is {"key": "value"} as shown'
    result = extract_json_from_response(response)
    assert result == {"key": "value"}


def test_extract_json_array():
    """Test JSON array extraction."""
    response = '[{"a": 1}, {"b": 2}]'
    result = extract_json_from_response(response)
    assert result == [{"a": 1}, {"b": 2}]


def test_safe_json_parse_valid():
    """Test parsing valid JSON."""
    result = safe_json_parse('{"key": "value"}')
    assert result == {"key": "value"}


def test_safe_json_parse_invalid():
    """Test parsing invalid JSON."""
    result = safe_json_parse("{key: value}")
    assert result is None
