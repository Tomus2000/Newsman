"""Main entry point for the daily Europe news Telegram bot."""

import logging
import sys

from dotenv import load_dotenv

from config import TELEGRAM_CHAT_ID
from chat_api_client import generate_news_overview
from news_client import fetch_top_europe_news
from telegram_formatter import build_telegram_message
from telegram_sender import send_telegram_message

# Load environment variables from .env file if it exists (for local development)
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Main function to fetch news and send Telegram message."""
    logger.info("Starting daily Europe news Telegram bot...")
    
    try:
        # Fetch articles
        articles = fetch_top_europe_news(limit=10)
        logger.info(f"Fetched {len(articles)} articles")
        
        # If no articles, try fallback with chat API
        fallback_overview = None
        if not articles:
            logger.info("No articles fetched, attempting fallback with chat API...")
            try:
                fallback_overview = generate_news_overview()
                logger.info("Generated fallback overview successfully")
            except Exception as e:
                logger.warning(f"Fallback overview generation failed: {e}")
        
        # Build Telegram message
        message = build_telegram_message(articles, fallback_overview=fallback_overview)
        
        # Send Telegram message
        send_telegram_message(message)
        
        logger.info(f"Successfully sent daily news to Telegram chat {TELEGRAM_CHAT_ID}")
        
    except Exception as e:
        logger.error(f"Failed to send daily news: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

