"""
Configuration for Telegram bot with Giphy API.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Bot configuration class."""

    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError(
            "❌ TELEGRAM_BOT_TOKEN not configured!\n"
            "Add the token to the .env file\n"
            "Get it from: https://t.me/BotFather"
        )

    # Giphy API
    GIPHY_API_KEY = os.getenv('GIPHY_API_KEY')
    if not GIPHY_API_KEY:
        raise ValueError(
            "❌ GIPHY_API_KEY not configured!\n"
            "Add the key to the .env file\n"
            "Get it from: https://developers.giphy.com"
        )

    # Limits and configurations
    RESULTS_LIMIT = int(os.getenv('RESULTS_LIMIT', '10'))
    CACHE_TIME = 300  # 5 minutes
    REQUEST_TIMEOUT = 5  # seconds

    # Giphy rating (g = general audience)
    GIPHY_RATING = os.getenv('GIPHY_RATING', 'g')

    # Language for Giphy
    GIPHY_LANG = os.getenv('GIPHY_LANG', 'it')

    @classmethod
    def validate(cls) -> bool:
        """Validate the configuration."""
        required = [
            ('TELEGRAM_BOT_TOKEN', cls.TELEGRAM_BOT_TOKEN),
            ('GIPHY_API_KEY', cls.GIPHY_API_KEY),
        ]

        all_valid = True
        for name, value in required:
            if not value:
                print(f"❌ {name} missing!")
                all_valid = False

        if all_valid:
            print("✅ Configuration valid!")

        return all_valid

    @classmethod
    def get_info(cls) -> dict:
        """Return configuration information."""
        return {
            'telegram_token': cls.TELEGRAM_BOT_TOKEN[:10] + '...',
            'giphy_key': cls.GIPHY_API_KEY[:10] + '...',
            'results_limit': cls.RESULTS_LIMIT,
            'cache_time': cls.CACHE_TIME,
            'timeout': cls.REQUEST_TIMEOUT,
        }
