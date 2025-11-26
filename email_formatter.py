"""Email formatting utilities for news digest."""

from datetime import datetime
from typing import Dict, List


def build_email_subject() -> str:
    """
    Build the email subject line.
    
    Returns:
        Subject string like "Your daily Europe news – 2024-01-15"
    """
    today = datetime.now().strftime("%Y-%m-%d")
    return f"Your daily Europe news – {today}"


def build_email_body_plain(articles: List[Dict]) -> str:
    """
    Build plain text email body.
    
    Args:
        articles: List of article dictionaries with title, description, url
        
    Returns:
        Plain text email body
    """
    today = datetime.now().strftime("%Y-%m-%d")
    
    if not articles:
        return f"""Daily Europe News – {today}

No news articles were available today. Please check back tomorrow.
"""
    
    lines = [f"Daily Europe News – {today}\n"]
    lines.append(f"Here are the top {len(articles)} European news stories:\n")
    
    for i, article in enumerate(articles, 1):
        lines.append(f"{i}) {article.get('title', 'No title')}")
        
        description = article.get('description', '')
        if description:
            # Truncate long descriptions
            desc = description[:200] + "..." if len(description) > 200 else description
            lines.append(f"   {desc}")
        
        url = article.get('url', '')
        if url:
            lines.append(f"   {url}")
        
        lines.append("")  # Empty line between articles
    
    return "\n".join(lines)


def build_email_body_html(articles: List[Dict]) -> str:
    """
    Build HTML email body.
    
    Args:
        articles: List of article dictionaries with title, description, url
        
    Returns:
        HTML email body (email-safe, no external CSS)
    """
    today = datetime.now().strftime("%Y-%m-%d")
    
    html_parts = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        "<meta charset='utf-8'>",
        "<style>",
        "  body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }",
        "  h2 { color: #2c3e50; }",
        "  ol { padding-left: 20px; }",
        "  li { margin-bottom: 15px; }",
        "  a { color: #3498db; text-decoration: none; }",
        "  a:hover { text-decoration: underline; }",
        "  .description { color: #666; margin-top: 5px; }",
        "</style>",
        "</head>",
        "<body>",
        f"<h2>Daily Europe News – {today}</h2>",
    ]
    
    if not articles:
        html_parts.append("<p>No news articles were available today. Please check back tomorrow.</p>")
    else:
        html_parts.append(f"<p>Here are the top {len(articles)} European news stories:</p>")
        html_parts.append("<ol>")
        
        for article in articles:
            title = article.get('title', 'No title')
            url = article.get('url', '')
            description = article.get('description', '')
            
            html_parts.append("<li>")
            
            if url:
                html_parts.append(f'<a href="{url}">{title}</a>')
            else:
                html_parts.append(f"<strong>{title}</strong>")
            
            if description:
                # Truncate long descriptions
                desc = description[:300] + "..." if len(description) > 300 else description
                html_parts.append(f'<p class="description">{desc}</p>')
            
            html_parts.append("</li>")
        
        html_parts.append("</ol>")
    
    html_parts.extend([
        "<hr>",
        "<p style='color: #999; font-size: 0.9em;'>This is an automated daily news digest.</p>",
        "</body>",
        "</html>",
    ])
    
    return "\n".join(html_parts)

