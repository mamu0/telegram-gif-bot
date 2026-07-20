# 🎬 Telegram GIF Bot

A **serverless, event-driven** Telegram bot that allows you to search and share GIFs from Giphy directly in chats using **inline queries**. 

Runs as **webhooks** - only processes requests when users interact with it. No polling, no continuous server running.

## ✨ Features

- 🔍 **Inline Searand CI setupch**: Search for GIFs while typing in chat
- 🎯 **Giphy Integration**: Full access to Giphy's API
- 📱 **Mobile Friendly**: Works perfectly on mobile devices
- 🚀 **Easy to Use**: Simple and intuitive interface
- 📊 **Trending**: Shows trending GIFs when no search is specified
- 🌐 **Serverless**: Runs your web service
- ⚡ **Event-Driven**: Webhook-based, no polling or continuous connections

## 🛠️ Requirements

- Telegram Bot Token (from [BotFather](https://t.me/BotFather))
- Giphy API Key (free from [developers.giphy.com](https://developers.giphy.com))
- GitHub account (to deploy from GitHub)
- A hosting platform for the webhook

## 📦 Quick Start

### 1. Fork the Repository

Fork this repo to your GitHub account.

### 2. Get Your Credentials

1. **Telegram Token**: See step 1 in [INSTALLATION.md](./INSTALLATION.md)
2. **Giphy API Key**: See step 2 in [INSTALLATION.md](./INSTALLATION.md)

### 3. Deploy on Web Service

1. Create a new **Web Service**
2. Select your forked repository
3. Fill in the settings:
   - **Name**: `telegram-gif-bot`
   - **Runtime**: `Python 3.11`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn main:app`
4. Add **Environment Variables**:
   - `TELEGRAM_BOT_TOKEN` = Your token from BotFather
   - `GIPHY_API_KEY` = Your Giphy API key
   - `WEBHOOK_URL` = Your app URL (e.g., `https://telegram-gif-bot-xxx.com`)
   - `WEBHOOK_SECRET_TOKEN` = A random secret string (recommended, prevents spoofed webhook calls)
   - `RESULTS_LIMIT` = `10`
   - `GIPHY_RATING` = `pg-13` for broader results, or `g` for stricter filtering
   - `GIPHY_LANGUAGE` = Optional language code such as `en` or `it`
5. Click **Deploy**

### 4. Set Bot Webhook in Telegram

Run this command locally or use an HTTP client (like Postman):

```bash
curl -X POST "https://api.telegram.org/bot<YOUR_TOKEN>/setWebhook?url=<YOUR_WEBHOOK_URL>/webhook"
```

Replace:
- `<YOUR_TOKEN>` with your Telegram bot token
- `<YOUR_WEBHOOK_URL>` with your web service URL (e.g., `https://telegram-gif-bot-xxx.com`)

Done! Your bot is now live and event-driven 🎉

Note: on free hosting plans the service may sleep or restart when idle, which can look like the machine turning off. If you need it always available, use a plan that stays online.

## 🚀 Usage

### Inline Search

Type in any Telegram chat:

```
@gif_bot search_term
```

### Examples

- `@gif_bot cat` - Shows cat GIFs
- `@gif_bot dancing` - Shows dancing GIFs
- `@gif_bot` - Shows trending GIFs

### Commands

| Command | Description |
|---------|------------|
| `/start` | Show welcome message |
| `/help` | Show usage guide |

## 📝 Project Structure

```
.
├── main.py                # Flask webhook handler + GiphyAPI client
├── tests/                 # Pytest unit tests
│   ├── conftest.py        # Test fixtures
│   └── test_bot.py        # GiphyAPI and endpoint tests
├── requirements.txt       # Python dependencies
├── Procfile               # Web service start command
├── .env.example           # Example environment variables
├── .github/workflows/     # GitHub Actions CI
├── .gitignore
├── README.md
├── CHANGELOG.md
├── INSTALLATION.md        # Detailed setup guide
├── Dockerfile             # Docker configuration (optional)
├── docker-compose.yml     # Docker Compose (optional)
└── LICENSE
```

## 🔐 Security Notes

- **DO NOT** commit your `.env` file — use environment variables on web services instead.
- Keep your bot token secret.
- Set `WEBHOOK_SECRET_TOKEN` to a random string: the bot will verify every incoming webhook request against the `X-Telegram-Bot-Api-Secret-Token` header sent by Telegram, blocking spoofed payloads.
- The webhook endpoint is public but protected by the secret token.

## 🔧 How It Works

1. **User Types**: `@gif_bot query` in any chat
2. **Telegram Sends**: HTTP POST request to your webhook URL
3. **Wakes Up**: Processes the request (fast cold start)
4. **Bot Responds**: Returns matching GIFs
5. **Sleeps**: Goes dormant until next request

No polling, no continuous connections, no charges! ✨

## 🌐 Deployment Alternatives

- **Docker**: Run locally with `docker-compose up`
- **Ngrok**: Use locally for testing webhooks
- **AWS Lambda**: Alternative serverless platform
- **Google Cloud Functions**: Alternative serverless platform

See [INSTALLATION.md](./INSTALLATION.md) for details.

## 🤝 Contributing

You are invited to contribute! If you find bugs or have suggestions:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is distributed under the MIT License. See the `LICENSE` file for more details.

## 💬 Support

If you have questions or issues:

1. Check the [python-telegram-bot documentation](https://python-telegram-bot.readthedocs.io/)
2. Read the [Giphy API documentation](https://developers.giphy.com/docs)
3. Open an issue in the repository

## 🙏 Acknowledgments

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Telegram library
- [Giphy API](https://www.giphy.com/) - GIF database
- [Flask](https://flask.palletsprojects.com/) - Web framework