"""
Utility functions for Telegram bot.
"""

import logging
from typing import Optional


def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """
    Configure logging for the application.

    Args:
        level: Logging level (default: INFO)

    Returns:
        Configured logger
    """
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=level
    )
    return logging.getLogger(__name__)


def format_gif_title(title: Optional[str], index: int) -> str:
    """
    Format the title of a GIF.

    Args:
        title: Original title from API
        index: GIF index

    Returns:
        Formatted title
    """
    if title and title.strip():
        return title.strip()
    return f"GIF #{index + 1}"


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length

    Returns:
        Truncated text
    """
    if len(text) > max_length:
        return text[:max_length - 3] + "..."
    return text


def escape_html(text: str) -> str:
    """
    Escape special HTML characters.

    Args:
        text: Text to escape

    Returns:
        Escaped text
    """
    replacements = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;',
    }
    for char, escaped in replacements.items():
        text = text.replace(char, escaped)
    return text


def get_trending_message() -> str:
    """Return message for trending GIFs."""
    return "🔥 <b>Trending GIFs</b> - You are viewing the most popular GIFs on Giphy"


def get_search_message(query: str, count: int) -> str:
    """
    Return search message.

    Args:
        query: Search term
        count: Number of results

    Returns:
        Search message
    """
    return f"🔍 <b>Results for:</b> <i>{escape_html(query)}</i> ({count} found)"


class RateLimiter:
    """Simple rate limiter implementation."""

    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        """
        Initialize rate limiter.

        Args:
            max_requests: Maximum number of requests
            window_seconds: Time window in seconds
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = {}

    def is_allowed(self, user_id: int) -> bool:
        """
        Check if user has reached limit.

        Args:
            user_id: User ID

        Returns:
            True if request is allowed
        """
        import time

        current_time = time.time()

        if user_id not in self.requests:
            self.requests[user_id] = []

        # Remove old requests
        self.requests[user_id] = [
            req_time for req_time in self.requests[user_id]
            if current_time - req_time < self.window_seconds
        ]

        # Check limit
        if len(self.requests[user_id]) < self.max_requests:
            self.requests[user_id].append(current_time)
            return True

        return False
