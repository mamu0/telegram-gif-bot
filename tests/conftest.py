"""
Pytest configuration — sets required env vars before any module is imported.
"""
import os

# Provide fake-but-format-valid credentials so main.py can be imported
# without a real .env file during testing.
os.environ.setdefault("TELEGRAM_BOT_TOKEN", "1234567890:AABBCCddEEFFggHHIIJJkkLLmmNNoo12345")
os.environ.setdefault("GIPHY_API_KEY", "test_giphy_api_key_for_unit_tests")
