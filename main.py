#!/usr/bin/env python3
"""
Telegram bot for inline GIF search using Giphy API.

Event-driven webhook-based bot.
Receives requests only when users interact with inline queries.
"""

import os
import logging
import asyncio
import requests
from typing import List
from dotenv import load_dotenv

from flask import Flask, request, jsonify
from telegram import Update, InlineQueryResultGif, Bot
from telegram.request import HTTPXRequest
from telegram.error import BadRequest

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def run_async(coro):
    """Run a Telegram coroutine from synchronous Flask code."""
    return asyncio.run(coro)

# Environment variables
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
GIPHY_API_KEY = os.getenv('GIPHY_API_KEY')
RESULTS_LIMIT = int(os.getenv('RESULTS_LIMIT', '10'))
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
PORT = int(os.getenv('PORT', 8000))

# Validate tokens
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is not configured in .env")
if not GIPHY_API_KEY:
    raise ValueError("GIPHY_API_KEY is not configured in .env")

# Initialize Flask app
app = Flask(__name__)
telegram_request = HTTPXRequest(
    connection_pool_size=int(os.getenv('TELEGRAM_CONNECTION_POOL_SIZE', '8')),
    pool_timeout=float(os.getenv('TELEGRAM_POOL_TIMEOUT', '10.0')),
)
bot = Bot(token=TELEGRAM_BOT_TOKEN, request=telegram_request)


class GiphyAPI:
    """Interface for Giphy API."""

    BASE_URL = "https://api.giphy.com/v1/gifs"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def search(self, query: str, limit: int = 10) -> List[dict]:
        """
        Search GIFs on Giphy.

        Args:
            query: Search term
            limit: Maximum number of results

        Returns:
            List of found GIFs
        """
        try:
            params = {
                "api_key": self.api_key,
                "q": query,
                "limit": limit,
                "offset": 0,
                "rating": "g",
                "lang": "it"
            }

            response = requests.get(
                f"{self.BASE_URL}/search",
                params=params,
                timeout=5
            )
            response.raise_for_status()

            data = response.json()
            return data.get("data", [])

        except requests.exceptions.RequestException as e:
            logger.error(f"Error searching Giphy: {e}")
            return []

    def trending(self, limit: int = 10) -> List[dict]:
        """
        Get trending GIFs.

        Args:
            limit: Maximum number of results

        Returns:
            List of trending GIFs
        """
        try:
            params = {
                "api_key": self.api_key,
                "limit": limit,
                "offset": 0,
                "rating": "g"
            }

            response = requests.get(
                f"{self.BASE_URL}/trending",
                params=params,
                timeout=5
            )
            response.raise_for_status()

            data = response.json()
            return data.get("data", [])

        except requests.exceptions.RequestException as e:
            logger.error(f"Error loading trending: {e}")
            return []


# Initialize Giphy API
giphy_api = GiphyAPI(GIPHY_API_KEY)


@app.route('/webhook', methods=['POST'])
def handle_webhook():
    """Handle incoming webhook requests from Telegram."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'ok': False, 'error': 'No data received'}), 400

        update = Update.de_json(data, bot)
        
        # Handle inline queries
        if update.inline_query:
            handle_inline_query(update.inline_query)
        
        # Handle commands
        if update.message:
            if update.message.text == '/start':
                handle_start(update)
            elif update.message.text == '/help':
                handle_help(update)

        return jsonify({'ok': True}), 200

    except Exception as e:
        logger.error(f"Error handling webhook: {e}")
        return jsonify({'ok': False, 'error': str(e)}), 500


def handle_inline_query(inline_query):
    """Handle inline queries for GIF search."""
    try:
        query = inline_query.query.strip()

        # If no text, show trending GIFs
        if not query:
            gifs = giphy_api.trending(limit=RESULTS_LIMIT)
        else:
            gifs = giphy_api.search(query, limit=RESULTS_LIMIT)

        # Build results
        results = []
        for i, gif in enumerate(gifs):
            result = InlineQueryResultGif(
                id=gif['id'],
                gif_url=gif['images']['original']['url'],
                thumbnail_url=gif['images']['fixed_height_small']['url'],
                title=gif.get('title', f'GIF {i+1}'),
                caption=gif.get('title', ''),
            )
            results.append(result)

        # Log query
        logger.info(f"Inline query '{query}' - {len(results)} results for user {inline_query.from_user.id}")

        # Send results to Telegram
        run_async(inline_query.answer(results, cache_time=300))

    except Exception as e:
        logger.error(f"Error in inline query handler: {e}")
        try:
            run_async(inline_query.answer([], cache_time=10))
        except:
            pass


def handle_start(update):
    """Handle /start command."""
    try:
        run_async(update.message.reply_text(
            "👋 Welcome to GIF Bot!\n\n"
            "Use the bot inline by typing my username followed by your search.\n\n"
            "Example: @gif_bot hello\n\n"
            "Type /help for more information."
        ))
    except Exception as e:
        logger.error(f"Error in start handler: {e}")


def handle_help(update):
    """Handle /help command."""
    try:
        help_text = (
            "🎬 <b>How to use GIF Bot</b>\n\n"
            "1️⃣ <b>Inline Search:</b>\n"
            "   Type in chat: <code>@gif_bot search_term</code>\n\n"
            "2️⃣ <b>Results:</b>\n"
            "   GIFs related to your search will be displayed\n\n"
            "3️⃣ <b>Share:</b>\n"
            "   Click on a GIF to share it in the chat\n\n"
            "4️⃣ <b>No text:</b>\n"
            "   Search without typing to see trending GIFs\n\n"
            "<b>Commands:</b>\n"
            "/start - Show welcome message\n"
            "/help - Show this guide"
        )
        run_async(update.message.reply_text(help_text, parse_mode="HTML"))
    except Exception as e:
        logger.error(f"Error in help handler: {e}")


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'ok', 'bot': 'telegram-gif-bot'}), 200


@app.route('/', methods=['GET'])
def index():
    """Root endpoint."""
    return jsonify({
        'bot': 'Telegram GIF Bot',
        'status': 'running',
        'webhook': '/webhook',
        'health': '/health'
    }), 200


def set_webhook():
    """Set webhook URL in Telegram."""
    try:
        if WEBHOOK_URL:
            url = f"{WEBHOOK_URL}/webhook"
            bot.set_webhook(url=url, drop_pending_updates=True)
            logger.info(f"Webhook set to {url}")
        else:
            logger.warning("WEBHOOK_URL not set, webhook may not work")
    except Exception as e:
        logger.error(f"Error setting webhook: {e}")


if __name__ == '__main__':
    # Set webhook on startup
    set_webhook()
    
    # Start Flask server
    logger.info(f"🚀 Starting bot server on port {PORT}...")
    app.run(host='0.0.0.0', port=PORT, debug=False)
