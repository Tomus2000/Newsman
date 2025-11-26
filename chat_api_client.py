"""Chat API client for generating news overview as fallback."""

import logging
from typing import Optional

import requests

from config import CHAT_API_KEY

logger = logging.getLogger(__name__)

CHAT_API_BASE_URL = "https://api.openai.com/v1"


def generate_news_overview(api_key: Optional[str] = None) -> str:
    """
    Generate a European news overview using the chat API as a fallback.
    
    Args:
        api_key: Optional API key (defaults to CHAT_API_KEY from config)
        
    Returns:
        Generated news overview text
    """
    if not api_key:
        api_key = CHAT_API_KEY
    
    if not api_key:
        logger.warning("No chat API key available for fallback")
        return "Unable to generate news overview - no API key available."
    
    try:
        url = f"{CHAT_API_BASE_URL}/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        
        prompt = """Please provide a brief overview of the most important European news stories from today. 
Focus on major political, economic, and social developments in Europe. 
Keep it concise (3-5 key points) and informative. 
Format it as a brief news summary suitable for a daily digest."""
        
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful news assistant that provides concise, accurate summaries of European news."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 500,
            "temperature": 0.7,
        }
        
        logger.info("Generating news overview using chat API...")
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        overview = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        if overview:
            logger.info("Successfully generated news overview")
            return overview
        else:
            logger.warning("Chat API returned empty response")
            return "Unable to generate news overview at this time."
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Error calling chat API: {e}")
        return "Unable to generate news overview due to API error."
    except (KeyError, ValueError) as e:
        logger.error(f"Error parsing chat API response: {e}")
        return "Unable to generate news overview due to parsing error."
    except Exception as e:
        logger.error(f"Unexpected error with chat API: {e}")
        return "Unable to generate news overview due to unexpected error."

