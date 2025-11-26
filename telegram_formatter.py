"""Telegram message formatting utilities for news digest."""

from datetime import datetime
from typing import Dict, List, Optional


def build_telegram_message(
    articles: List[Dict], fallback_overview: Optional[str] = None
) -> str:
    """
    Build a Telegram message from news articles.
    Plain text only (no HTML), so Telegram can't choke on formatting.
    """
    today = datetime.now().strftime("%Y-%m-%d")

    lines: List[str] = []
    lines.append(f"📰 Daily Europe News – {today}")
    lines.append("")

    if not articles:
        if fallback_overview:
            lines.append("News API unavailable. Here's an AI-generated overview:")
            lines.append("")
            lines.append(fallback_overview)
        else:
            lines.append(
                "No news articles were available today. Please check back tomorrow."
            )

        msg = "\n".join(lines)
        return msg[:4000] + "\n\n... (message truncated)" if len(msg) > 4000 else msg

    lines.append(f"Here are the top {len(articles)} European news stories:")
    lines.append("")

    for i, article in enumerate(articles, 1):
        title = (article.get("title") or "No title").strip()
        url = (article.get("url") or "").strip()
        desc = (article.get("description") or "").strip()

        if len(desc) > 200:
            desc = desc[:200] + "..."

        # Titel
        lines.append(f"{i}. {title}")

        # Kurzbeschreibung
        if desc:
            lines.append(f"   {desc}")

        # Link
        if url:
            lines.append(f"   {url}")

        lines.append("")  # Leerzeile zwischen Artikeln

    msg = "\n".join(lines)
    if len(msg) > 4000:
        msg = msg[:4000] + "\n\n... (message truncated)"

    return msg




