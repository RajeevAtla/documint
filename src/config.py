"""Centralized configuration management."""

import os
from typing import Dict

from dotenv import load_dotenv


def load_config() -> Dict[str, str]:
    """
    Load configuration from environment variables.

    Returns:
        dict: Configuration dictionary with keys:
            - gemini_api_key: str
            - log_level: str
            - model_name: str
            - max_tokens: int

    Raises:
        ValueError: If required environment variables are missing
    """
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is required in the environment")

    log_level = os.getenv("LOG_LEVEL", "INFO")
    model_name = os.getenv("MODEL_NAME", "gemini-1.5-pro")
    max_tokens = int(os.getenv("MAX_TOKENS", "4096"))

    return {
        "gemini_api_key": api_key,
        "log_level": log_level,
        "model_name": model_name,
        "max_tokens": max_tokens,
    }


def get_gemini_api_key() -> str:
    """
    Get Gemini API key from environment.

    Returns:
        str: API key

    Raises:
        ValueError: If API key not found
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is required in the environment")
    return api_key


def get_model_name() -> str:
    """
    Get the Gemini model name to use.

    Returns:
        str: Model name (default: gemini-1.5-pro)
    """
    return os.getenv("MODEL_NAME", "gemini-1.5-pro")
