"""Telegram bot message sending functionality."""

import logging
from typing import Optional

import requests

from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

logger = logging.getLogger(__name__)

TELEGRAM_API_BASE_URL = "https://api.telegram.org/bot"


def send_telegram_message(message: str, parse_mode: Optional[str] = None) -> None:
    """
    Send a message to the configured Telegram chat.

    Args:
        message: Text to send.
        parse_mode: Optional Telegram parse mode ("HTML", "MarkdownV2", etc.).
                    If None, message is treated as plain text.
    """
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN is not set")
    if not TELEGRAM_CHAT_ID:
        raise ValueError("TELEGRAM_CHAT_ID is not set")

    url = f"{TELEGRAM_API_BASE_URL}{TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "disable_web_page_preview": False,
    }

    # Nur wenn du später wieder bewusst HTML/Markdown verwenden willst:
    if parse_mode:
        payload["parse_mode"] = parse_mode

    try:
        logger.info(f"Sending Telegram message to chat {TELEGRAM_CHAT_ID}...")
        resp = requests.post(url, json=payload, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if not data.get("ok", False):
            raise RuntimeError(f"Telegram API returned ok=false: {data}")
        logger.info("Telegram message sent successfully!")
    except Exception as e:
        logger.error(f"Unexpected error sending Telegram message: {e}")
        raise
