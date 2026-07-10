# 📋 Installation Guide - Telegram Giphy Bot

This guide covers both deployment on **Render** (recommended, serverless) and local development.

## Quick Start: Deploy on Render (Recommended)

### Phase 1: Get Your Credentials (5 minutes)

#### 1.1 Get Telegram Bot Token

1. Open Telegram and go to [@BotFather](https://t.me/BotFather)
2. Type `/newbot`
3. Follow the instructions:
   - Enter a name for your bot (e.g., "My GIF Bot")
   - Enter a unique username ending with `_bot` (e.g., `mygif_bot_2024`)
4. **Save the token** - it looks like:
   ```
   123456789:ABCdefGHIjklmnoPQRstuvWXYZ_1234567
   ```

#### 1.2 Get Giphy API Key

1. Visit [developers.giphy.com](https://developers.giphy.com)
2. Click "Sign up" (or login)
3. Create a new app
4. Accept the terms
5. **Save the API Key**

### Phase 2: Deploy on Render (5 minutes)

1. **Fork this repository** to your GitHub account
   - Click "Fork" on GitHub

2. **Sign up on Render**
   - Go to [render.com](https://render.com)
   - Click "Sign up" and select "Continue with GitHub"
   - Authorize Render to access your GitHub

3. **Create a Web Service on Render**
   - Click "New +"
   - Select "Web Service"
   - Select your forked repository
   - Click "Connect"

4. **Configure the Service**
   - **Name**: `telegram-gif-bot`
   - **Runtime**: `Python 3.11`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn main:app`
   - **Free Plan**: Select it

5. **Add Environment Variables**
   - Click "Add Environment Variable" for each:
   
   | Key | Value |
   |-----|-------|
   | `TELEGRAM_BOT_TOKEN` | Your token from BotFather |
   | `GIPHY_API_KEY` | Your Giphy API key |
   | `WEBHOOK_URL` | `https://telegram-gif-bot-xxx.onrender.com` (you'll get this URL) |
   | `RESULTS_LIMIT` | `10` |

   **Note**: After you click "Create Web Service", you'll get a URL like `https://telegram-gif-bot-xxxxx.onrender.com`. Use this for `WEBHOOK_URL`.

6. **Click "Create Web Service"**
   - Render will start deploying (takes ~2-3 minutes)
   - Wait for the status to say "Live"

7. **Set the Webhook**
   - Once Render shows your URL, run this command locally or in your terminal:
   
   ```bash
   curl -X POST "https://api.telegram.org/bot<YOUR_TOKEN>/setWebhook?url=<YOUR_WEBHOOK_URL>/webhook"
   ```
   
   Replace:
   - `<YOUR_TOKEN>` with your Telegram bot token
   - `<YOUR_WEBHOOK_URL>` with your Render URL
   
   **Example**:
   ```bash
   curl -X POST "https://api.telegram.org/bot123456789:ABCdef/setWebhook?url=https://telegram-gif-bot-abc123.onrender.com/webhook"
   ```

8. **Test the Bot**
   - Open Telegram
   - Search for your bot by username (e.g., `@mygif_bot_2024`)
   - Type `/start`
   - Try: `@mygif_bot_2024 cat`
   - GIFs should appear! 🎉

---

## Local Development (Optional)

### Phase 1: Setup Local Environment

#### 1.1 Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/telegram-gif-bot.git
cd telegram-gif-bot
```

#### 1.2 Create Virtual Environment

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

#### 1.3 Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Phase 2: Local Configuration

#### 2.1 Create `.env` File

```bash
cp .env.example .env
```

#### 2.2 Edit `.env`

Open `.env` and add:
```
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklmnoPQRstuvWXYZ_1234567
GIPHY_API_KEY=abc123def456ghi789jkl012
WEBHOOK_URL=http://localhost:8000
RESULTS_LIMIT=10
PORT=8000
```

### Phase 3: Testing Locally with Ngrok

For local testing with real Telegram updates, use **Ngrok**:

1. **Install Ngrok**:
   ```bash
   # On macOS with Homebrew:
   brew install ngrok
   
   # Or download from: https://ngrok.com/download
   ```

2. **Start the Bot Locally**:
   ```bash
   python main.py
   ```

3. **In Another Terminal, Start Ngrok**:
   ```bash
   ngrok http 8000
   ```

4. **Copy the Ngrok URL** (looks like `https://abc123.ngrok.io`)

5. **Set Webhook** (update the URL in `.env`):
   ```bash
   WEBHOOK_URL=https://abc123.ngrok.io
   ```

6. **Set Telegram Webhook**:
   ```bash
   curl -X POST "https://api.telegram.org/bot<YOUR_TOKEN>/setWebhook?url=https://abc123.ngrok.io/webhook"
   ```

---

## 🔧 Troubleshooting

### Error: "Webhook doesn't work"

**Solution:**
1. Make sure Render URL is accessible: `https://yourdomain.onrender.com/health`
2. Check your bot token is correct
3. Run the setWebhook command again
4. Check Render logs for errors

### Error: "TELEGRAM_BOT_TOKEN not configured"

**Solution:** Check that environment variables are set in Render's settings (not in `.env`)

### Error: "No results from Giphy"

**Solution:**
1. Check your Giphy API key is correct
2. Make sure your Giphy app is active
3. Check Render logs for API errors

### Bot Doesn't Respond

**Solution:**
1. Check Render shows "Live" status
2. Verify webhook URL: `https://api.telegram.org/bot<TOKEN>/getWebhookInfo`
3. Check Render logs for errors

### Render Goes to Sleep

This is normal! Free tier apps sleep after 15 minutes of inactivity. They wake up automatically when you use the bot. Just wait a few seconds for the first request.

---

## 📊 How Webhooks Work

```
You type: @gif_bot cat
           ↓
Telegram sends HTTP POST to your webhook
           ↓
Bot processes request (very fast!)
           ↓
Bot sends results back to Telegram
           ↓
You see GIFs in chat
           ↓
Server sleeps (no resources used!)
```

---

## ✅ Deployment Checklist

- [ ] Telegram bot token obtained from BotFather
- [ ] Giphy API Key obtained
- [ ] GitHub repository forked
- [ ] Render account created
- [ ] Web Service created on Render
- [ ] Environment variables set in Render
- [ ] Webhook URL set in Telegram
- [ ] Bot tested in Telegram chat
- [ ] Inline search working

Perfect! Your bot is now live! 🎉

---

## 📝 Additional Notes

### Render Free Tier Limits

- ✅ 1 active web service
- ✅ 0.5GB RAM
- ✅ Auto-sleeps after 15 min inactivity
- ✅ Wakes up instantly when needed
- ✅ Perfect for webhook-based bots!

### About the Webhook

- Telegram sends requests to `/webhook` endpoint
- Bot validates requests and processes them
- No polling, no continuous connection
- Very cost-effective!

### Environment Variables

Never commit `.env` file! Render lets you set variables securely through the dashboard.

---

## 💬 Need Help?

1. Check [Render documentation](https://render.com/docs)
2. Check [python-telegram-bot docs](https://python-telegram-bot.readthedocs.io/)
3. Check [Giphy API docs](https://developers.giphy.com/docs)
4. Open an issue on GitHub
