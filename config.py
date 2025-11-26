"""Configuration module for loading environment variables."""

import os
from typing import Optional


def get_env_var(name: str, required: bool = True) -> Optional[str]:
    """
    Get an environment variable.
    
    Args:
        name: The name of the environment variable
        required: If True, raise an error if the variable is missing
        
    Returns:
        The value of the environment variable, or None if not required and missing
        
    Raises:
        ValueError: If required is True and the variable is missing
    """
    value = os.getenv(name)
    if required and not value:
        raise ValueError(
            f"Required environment variable '{name}' is not set. "
            "Please set it in your environment or .env file."
        )
    return value


# News API configuration
NEWS_API_KEY = get_env_var("NEWS_API_KEY")
NEWS_API_BASE_URL = "https://api.worldnewsapi.com"

# Telegram Bot configuration
TELEGRAM_BOT_TOKEN = get_env_var("TELEGRAM_BOT_TOKEN", required=False) or ""
TELEGRAM_CHAT_ID = get_env_var("TELEGRAM_CHAT_ID", required=False) or ""

# Chat API configuration (for fallback news overview)
CHAT_API_KEY = get_env_var("CHAT_API_KEY", required=False) or ""

