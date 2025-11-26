"""Telegram message formatting utilities for news digest."""

from datetime import datetime
from typing import Dict, List, Optional


def build_telegram_message(articles: List[Dict], fallback_overview: Optional[str] = None) -> str:
    """
    Build a Telegram message from news articles.
    Uses HTML formatting for Telegram.
    
    Args:
        articles: List of article dictionaries with title, description, url
        fallback_overview: Optional overview text to use if no articles available
        
    Returns:
        Formatted Telegram message (HTML)
    """
    today = datetime.now().strftime("%Y-%m-%d")
    
    if not articles:
        if fallback_overview:
            return f"""📰 <b>Daily Europe News – {today}</b>

<i>News API unavailable. Here's an AI-generated overview:</i>

{fallback_overview}
"""
        else:
            return f"""📰 <b>Daily Europe News – {today}</b>

No news articles were available today. Please check back tomorrow.
"""
    
    message_parts = [
        f"📰 <b>Daily Europe News – {today}</b>",
        f"\nHere are the top {len(articles)} European news stories:\n",
    ]
    
    for i, article in enumerate(articles, 1):
        title = article.get("title", "No title")
        url = article.get("url", "")
        description = article.get("description", "")
        
        # Format article with HTML
        if url:
            article_line = f"{i}. <a href=\"{url}\">{title}</a>"
        else:
            article_line = f"{i}. <b>{title}</b>"
        
        message_parts.append(article_line)
        
        if description:
            # Truncate long descriptions
            desc = description[:200] + "..." if len(description) > 200 else description
            message_parts.append(f"   <i>{desc}</i>")
        
        message_parts.append("")  # Empty line between articles
    
    # Telegram has a 4096 character limit, so truncate if needed
    message = "\n".join(message_parts)
    if len(message) > 4000:
        message = message[:4000] + "\n\n... (message truncated)"
    
    return message

