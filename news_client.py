"""News client for fetching European news from World News API."""

import logging
from typing import Dict, List

import requests

from config import NEWS_API_BASE_URL, NEWS_API_KEY

logger = logging.getLogger(__name__)


def fetch_top_europe_news(limit: int = 10) -> List[Dict]:
    """
    Fetch top European news articles from World News API.
    
    Args:
        limit: Maximum number of articles to return (default: 10)
        
    Returns:
        List of dictionaries containing article data with keys:
        - title: Article headline
        - description: Article summary/description
        - url: Article URL
        - published_at: Publication timestamp
    """
    try:
        # World News API endpoint - using top-news endpoint
        # API key should be in X-API-KEY header
        url = f"{NEWS_API_BASE_URL}/top-news"
        
        headers = {
            "X-API-KEY": NEWS_API_KEY,
        }
        
        params = {
            "source-country": "eu",  # Use singular form
            "language": "en",
            "number": limit,
        }
        
        logger.info(f"Fetching top {limit} European news articles...")
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract articles from the API response
        # World News API returns articles in a 'news' field
        articles = data.get("news", [])
        
        # Format articles to have consistent structure
        formatted_articles = []
        for article in articles[:limit]:
            formatted_articles.append({
                "title": article.get("title", "No title"),
                "description": article.get("text", article.get("summary", "No description available")),
                "url": article.get("url", ""),
                "published_at": article.get("publish_date", ""),
            })
        
        logger.info(f"Successfully fetched {len(formatted_articles)} articles")
        return formatted_articles
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching news: {e}")
        return []
    except (KeyError, ValueError) as e:
        logger.error(f"Error parsing news response: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error fetching news: {e}")
        return []

