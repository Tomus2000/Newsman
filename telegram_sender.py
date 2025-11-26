"""Telegram bot message sending functionality."""

import logging
from typing import Optional

import requests

from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

logger = logging.getLogger(__name__)

TELEGRAM_API_BASE_URL = "https://api.telegram.org/bot"


def send_telegram_message(message: str, parse_mode: Optional[str] = "HTML") -> None:
    """
    Send a message via Telegram bot.
    
    Args:
        message: The message text to send
        parse_mode: Optional parse mode (HTML or Markdown)
        
    Raises:
        Exception: If message sending fails
    """
    try:
        url = f"{TELEGRAM_API_BASE_URL}{TELEGRAM_BOT_TOKEN}/sendMessage"
        
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": parse_mode,
        }
        
        logger.info(f"Sending Telegram message to chat {TELEGRAM_CHAT_ID}...")
        response = requests.post(url, json=payload, timeout=30)
        
        result = response.json()
        if not result.get("ok"):
            error_msg = result.get("description", "Unknown error")
            error_code = result.get("error_code", "Unknown")
            logger.error(f"Telegram API error {error_code}: {error_msg}")
            raise Exception(f"Telegram API error {error_code}: {error_msg}")
        
        response.raise_for_status()
        logger.info("Telegram message sent successfully!")
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Error sending Telegram message: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error sending Telegram message: {e}")
        raise


def get_bot_info() -> dict:
    """
    Get bot information to verify the token works.
    
    Returns:
        Bot information dictionary
    """
    try:
        url = f"{TELEGRAM_API_BASE_URL}{TELEGRAM_BOT_TOKEN}/getMe"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error getting bot info: {e}")
        return {}


def get_updates() -> list:
    """
    Get recent updates (messages) sent to the bot.
    This can be used to find the chat_id.
    
    Returns:
        List of updates
    """
    try:
        url = f"{TELEGRAM_API_BASE_URL}{TELEGRAM_BOT_TOKEN}/getUpdates"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("result", [])
    except Exception as e:
        logger.error(f"Error getting updates: {e}")
        return []

