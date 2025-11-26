"""News client for fetching European news from World News API."""

import logging
from typing import Dict, List

import requests

from config import NEWS_API_BASE_URL, NEWS_API_KEY

logger = logging.getLogger(__name__)


def fetch_top_europe_news(limit: int = 10) -> List[Dict]:
    """
    Fetch top European news articles from World News API.
    Returns a list of dicts: title, description, url, published_at.
    """
    if not NEWS_API_KEY:
        logger.error("NEWS_API_KEY is not set")
        return []

    url = f"{NEWS_API_BASE_URL}/search-news"

    params = {
        # required: at least one filter → '*' = alles
        "text": "*",
        # nur Europa-Quellen
        "source-countries": "eu",
        # nur englische Artikel (sonst wird's wild)
        "language": "en",
        # wie viele Artikel zurückgeben
        "number": limit,
        # neueste zuerst
        "sort": "publish-time",
        "sort-direction": "desc",
        # Auth
        "api-key": NEWS_API_KEY,
    }

    headers = {"Accept": "application/json"}

    try:
        logger.info("Fetching European news from World News API...")
        resp = requests.get(url, params=params, headers=headers, timeout=15)
        resp.raise_for_status()

        data = resp.json()

        articles = data.get("news", [])
        logger.info(
            f"World News API returned {len(articles)} articles (available={data.get('available')})"
        )

        formatted: List[Dict] = []
        for article in articles[:limit]:
            formatted.append(
                {
                    "title": article.get("title", "No title"),
                    "description": article.get("text")
                    or article.get("summary", "No description available"),
                    "url": article.get("url", ""),
                    "published_at": article.get("publish_date", ""),
                }
            )

        return formatted

    except requests.exceptions.HTTPError as e:
        # Typische Fälle: 401 (Key falsch), 429 (Rate Limit)
        logger.error(
            f"HTTP error from World News API: {e} | body={resp.text[:300]}"
        )
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error fetching news: {e}")
    except Exception as e:
        logger.error(f"Unexpected error fetching news: {e}")

    return []
