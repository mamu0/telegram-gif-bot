#!/usr/bin/env python3
"""
Test script to verify configuration and connections.
"""

import sys
from config import Config


def test_config():
    """Test configuration."""
    print("🔍 Testing configuration...\n")

    try:
        Config.validate()
        info = Config.get_info()

        print("\n📋 Configuration loaded:")
        for key, value in info.items():
            print(f"   {key}: {value}")

        return True
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        return False


def test_giphy_api():
    """Test Giphy API."""
    print("\n🔍 Testing Giphy API...\n")

    try:
        import requests
        from config import Config

        # Test trending
        params = {
            "api_key": Config.GIPHY_API_KEY,
            "limit": 1,
            "rating": Config.GIPHY_RATING,
        }

        response = requests.get(
            "https://api.giphy.com/v1/gifs/trending",
            params=params,
            timeout=Config.REQUEST_TIMEOUT
        )
        response.raise_for_status()

        data = response.json()
        if data.get("data"):
            print("✅ Giphy API works!")
            print(f"   GIF found: {data['data'][0].get('title', 'Untitled')}")
            return True
        else:
            print("❌ No data from Giphy")
            return False

    except Exception as e:
        print(f"❌ Giphy API error: {e}")
        return False


def test_telegram():
    """Test Telegram connection."""
    print("\n🔍 Testing Telegram Bot...\n")

    try:
        from telegram.ext import Application
        from config import Config

        # Build app without starting it
        app = Application.builder().token(Config.TELEGRAM_BOT_TOKEN).build()

        # If we reach here, token is at least formally valid
        print("✅ Telegram token valid!")
        print("   (Full verification available only during execution)")
        return True

    except Exception as e:
        print(f"❌ Telegram error: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 50)
    print("🤖 TELEGRAM GIPHY BOT TEST")
    print("=" * 50)

    results = []

    # Test 1: Configuration
    results.append(("Configuration", test_config()))

    # Test 2: Giphy API
    results.append(("Giphy API", test_giphy_api()))

    # Test 3: Telegram
    results.append(("Telegram Bot", test_telegram()))

    # Final report
    print("\n" + "=" * 50)
    print("📊 TEST REPORT")
    print("=" * 50)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")

    print(f"\nResult: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! Bot is ready.")
        print("\nTo start the bot, run:")
        print("   python main.py")
        return 0
    else:
        print("\n⚠️  Some tests failed.")
        print("Check the configuration and tokens.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
