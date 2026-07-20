#!/usr/bin/env python3
"""
Manual integration check — verifies credentials and API connectivity.
Run with: python test_setup.py

For automated unit tests see: pytest tests/
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GIPHY_API_KEY = os.getenv("GIPHY_API_KEY")
GIPHY_RATING = os.getenv("GIPHY_RATING", "pg-13")
REQUEST_TIMEOUT = 5


def test_config():
    """Verify required environment variables are set."""
    print("🔍 Checking configuration...\n")

    all_valid = True
    for name, value in [
        ("TELEGRAM_BOT_TOKEN", TELEGRAM_BOT_TOKEN),
        ("GIPHY_API_KEY", GIPHY_API_KEY),
    ]:
        if not value:
            print(f"  ❌ {name} missing in .env")
            all_valid = False
        else:
            print(f"  ✅ {name} = {value[:10]}...")

    return all_valid


def test_giphy_api():
    """Test Giphy API connectivity."""
    print("\n🔍 Testing Giphy API...\n")

    if not GIPHY_API_KEY:
        print("  ⚠️  Skipped — GIPHY_API_KEY not set")
        return False

    try:
        import requests

        params = {
            "api_key": GIPHY_API_KEY,
            "limit": 1,
            "rating": GIPHY_RATING,
        }
        response = requests.get(
            "https://api.giphy.com/v1/gifs/trending",
            params=params,
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()

        if data.get("data"):
            title = data["data"][0].get("title", "Untitled")
            print(f"  ✅ Giphy API OK — first trending: {title!r}")
            return True

        print("  ❌ Giphy returned empty data")
        return False

    except Exception as e:
        print(f"  ❌ Giphy API error: {e}")
        return False


def test_telegram():
    """Test Telegram bot token (format check only — no network call)."""
    print("\n🔍 Testing Telegram token...\n")

    if not TELEGRAM_BOT_TOKEN:
        print("  ⚠️  Skipped — TELEGRAM_BOT_TOKEN not set")
        return False

    try:
        from telegram.ext import Application

        Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        print("  ✅ Telegram token format valid")
        print("     (Full connectivity verified at runtime)")
        return True

    except Exception as e:
        print(f"  ❌ Telegram error: {e}")
        return False


def main():
    """Run all checks and print a summary."""
    print("=" * 50)
    print("🤖  TELEGRAM GIF BOT — SETUP CHECK")
    print("=" * 50)

    results = [
        ("Configuration", test_config()),
        ("Giphy API", test_giphy_api()),
        ("Telegram Bot", test_telegram()),
    ]

    print("\n" + "=" * 50)
    print("📊 RESULTS")
    print("=" * 50)

    passed = sum(ok for _, ok in results)
    total = len(results)

    for name, ok in results:
        print(f"  {'✅' if ok else '❌'}  {name}")

    print(f"\n{passed}/{total} checks passed")

    if passed == total:
        print("\n🎉  All checks passed. Start the bot with: gunicorn main:app")
    else:
        print("\n⚠️   Fix the issues above, then re-run this script.")

    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
