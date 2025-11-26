"""Telegram message formatting utilities for news digest."""

from datetime import datetime
from typing import Dict, List, Optional
from html import escape  # wichtig: HTML-Sonderzeichen escapen


def build_telegram_message(
    articles: List[Dict], fallback_overview: Optional[str] = None
) -> str:
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

    # Kein Artikel → Fallback
    if not articles:
        if fallback_overview:
            safe_overview = escape(fallback_overview)
            return (
                f"📰 <b>Daily Europe News – {today}</b>\n\n"
                f"<i>News API unavailable. Here's an AI-generated overview:</i>\n\n"
                f"{safe_overview}"
            )
        else:
            return (
                f"📰 <b>Daily Europe News – {today}</b>\n\n"
                "No news articles were available today. Please check back tomorrow."
            )

    message_parts: List[str] = [
        f"📰 <b>Daily Europe News – {today}</b>",
        "",
        f"Here are the top {len(articles)} European news stories:",
        "",
    ]

    for i, article in enumerate(articles, 1):
        raw_title = article.get("title", "No title") or "No title"
        raw_url = article.get("url", "") or ""
        raw_description = article.get("description", "") or ""

        # Titel & Beschreibung HTML-sicher machen
        title = escape(raw_title)
        if raw_description:
            short_desc = (
                raw_description[:200] + "..."
                if len(raw_description) > 200
                else raw_description
            )
            desc = escape(short_desc)
        else:
            desc = ""

        # URL in href-Attribut escapen (inkl. Anführungszeichen)
        if raw_url:
            safe_url = escape(raw_url, quote=True)
            article_line = f'{i}. <a href="{safe_url}">{title}</a>'
        else:
            article_line = f"{i}. <b>{title}</b>"

        message_parts.append(article_line)

        if desc:
            message_parts.append(f"   <i>{desc}</i>")

        message_parts.append("")  # Leerzeile zwischen Artikeln

    # Telegram hat 4096 Zeichen Limit
    message = "\n".join(message_parts)
    if len(message) > 4000:
        message = message[:4000] + "\n\n... (message truncated)"

    return message



