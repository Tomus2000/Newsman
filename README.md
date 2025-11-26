# Daily Europe News Telegram Bot

An automated Python bot that fetches the latest European news headlines and sends them via Telegram every morning at 09:00 Lisbon time using GitHub Actions.

## Features

- Fetches top European news from World News API
- **Fallback system**: Uses Chat API (OpenAI) to generate news overview if news API fails
- Formats news into clean, readable Telegram messages
- Sends messages automatically via GitHub Actions cron schedule
- No server required - runs entirely on GitHub Actions

## Project Structure

```
.
├── main.py                    # Entry point
├── news_client.py             # Fetches news from World News API
├── chat_api_client.py         # Fallback: Generates news overview using Chat API
├── telegram_formatter.py      # Formats Telegram messages
├── telegram_sender.py         # Sends messages via Telegram Bot API
├── config.py                  # Environment variable management
├── requirements.txt           # Python dependencies
├── .github/
│   └── workflows/
│       └── daily-news.yml    # GitHub Actions workflow
└── README.md                  # This file
```

## Setup

### 1. Local Development

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory with your credentials:
   ```env
   NEWS_API_KEY=your_world_news_api_key
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   TELEGRAM_CHAT_ID=your_telegram_chat_id
   CHAT_API_KEY=your_chat_api_key  # Optional: for fallback news overview
   ```
4. Get your Telegram Chat ID:
   - Send a message to your bot on Telegram
   - Run: `python get_chat_id.py` to get your chat ID
5. Run locally:
   ```bash
   python main.py
   ```

### 2. GitHub Actions Deployment

1. Push this repository to GitHub

2. Add the following secrets in your GitHub repository settings:
   - Go to Settings → Secrets and variables → Actions
   - Add the following secrets:
     - `NEWS_API_KEY`: Your World News API key
     - `TELEGRAM_BOT_TOKEN`: Your Telegram bot token (from BotFather)
     - `TELEGRAM_CHAT_ID`: Your Telegram chat ID (run `get_chat_id.py` to find it)
     - `CHAT_API_KEY`: (Optional) Your Chat API key (OpenAI) for fallback news overview

3. Enable GitHub Actions in your repository settings

4. The workflow will run automatically every day at 09:00 UTC (09:00 Lisbon time in winter, 10:00 in summer)

### Getting API Keys

#### World News API
1. Visit [worldnewsapi.com](https://worldnewsapi.com/)
2. Sign up for a free account
3. Get your API key from the dashboard

#### Telegram Bot
1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Use `/newbot` command to create a new bot
3. Get your bot token from BotFather
4. Send a message to your bot
5. Run `python get_chat_id.py` to get your chat ID

## How It Works

1. **News Fetching**: The bot calls the World News API with filters for European news (`source-country=eu`, `language=en`)
2. **Fallback System**: If the news API fails or returns no articles, the bot uses the Chat API (OpenAI) to generate an AI-powered overview of European news
3. **Message Formatting**: Articles (or AI overview) are formatted into a clean Telegram message with HTML formatting
4. **Telegram Sending**: The message is sent via Telegram Bot API
5. **Scheduling**: GitHub Actions runs the script daily at the scheduled time

## Manual Testing

You can manually trigger the workflow:
1. Go to the "Actions" tab in your GitHub repository
2. Select "Daily Europe News Telegram"
3. Click "Run workflow"

## Troubleshooting

- **Telegram message not sending**: Check that your `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` are correct
- **No news articles**: Verify your `NEWS_API_KEY` is valid and has remaining API calls. You may hit rate limits during testing. The bot will automatically use the Chat API fallback if configured.
- **Fallback not working**: Make sure `CHAT_API_KEY` is set if you want the AI fallback feature. The bot will still send a message even without it, just without the AI overview.
- **Workflow not running**: Ensure GitHub Actions is enabled and the cron schedule is correct
- **Chat ID not found**: Make sure you've sent at least one message to your bot before running `get_chat_id.py`

## License

MIT

