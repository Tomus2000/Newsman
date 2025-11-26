"""
Helper script to get your Telegram chat ID safely.

Usage:
1. Set your TELEGRAM_BOT_TOKEN as an environment variable.
   - macOS / Linux (bash/zsh):
       export TELEGRAM_BOT_TOKEN="123456:ABCDEF..."
   - Windows PowerShell:
       $env:TELEGRAM_BOT_TOKEN="123456:ABCDEF..."

2. Start a chat with your bot in Telegram (e.g. t.me/YourBotName) und schick eine Nachricht (/start).

3. Run this script:
       python get_chat_id.py

4. The script will print your chat ID. Use that value as TELEGRAM_CHAT_ID in your GitHub Secret.
"""

import os
import sys
import requests

API_BASE = "https://api.telegram.org/bot"


def get_bot_token() -> str:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print(
            "Error: TELEGRAM_BOT_TOKEN environment variable is not set.\n\n"
            "Set it like this and run again:\n"
            "  - macOS / Linux (bash/zsh):\n"
            '      export TELEGRAM_BOT_TOKEN="123456:ABCDEF..."\n'
            "  - Windows PowerShell:\n"
            '      $env:TELEGRAM_BOT_TOKEN="123456:ABCDEF..."\n'
        )
        sys.exit(1)
    return token


def get_bot_info(token: str) -> dict:
    url = f"{API_BASE}{token}/getMe"
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    return resp.json()


def get_updates(token: str) -> dict:
    url = f"{API_BASE}{token}/getUpdates"
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    return resp.json()


def main() -> None:
    token = get_bot_token()

    print("=" * 60)
    print("Getting bot information...")
    print("=" * 60)

    try:
        bot_info = get_bot_info(token)
    except Exception as e:
        print(f"Error: Could not get bot info. Check your bot token. ({e})")
        sys.exit(1)

    if bot_info.get("ok"):
        bot = bot_info.get("result", {})
        print(f"Bot Name: {bot.get('first_name')}")
        print(f"Bot Username: @{bot.get('username')}")
        print(f"Bot ID: {bot.get('id')}")
    else:
        print("Error: Telegram returned ok=false for getMe().")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("Getting recent messages...")
    print("=" * 60)
    print("\nMake sure you've sent a message to your bot first!")
    print("Open Telegram, go to your bot and send /start or any message.\n")

    try:
        data = get_updates(token)
    except Exception as e:
        print(f"Error while calling getUpdates: {e}")
        sys.exit(1)

    results = data.get("result", [])
    if not results:
        print("No messages found. Please:")
        print("1. Open Telegram and go to your bot")
        print("2. Click 'Start' or send any message")
        print("3. Run this script again")
        return

    chat_ids = set()
    for update in results:
        message = update.get("message") or update.get("edited_message") or {}
        chat = message.get("chat", {})
        chat_id = chat.get("id")
        if chat_id is None:
            continue
        chat_name = chat.get("first_name") or chat.get("title") or "Unknown"

        chat_ids.add((chat_id, chat_name))

    print(f"Found {len(chat_ids)} chat(s):\n")
    for cid, name in chat_ids:
        print(f"  {cid} ({name})")

    if chat_ids:
        first_chat_id = list(chat_ids)[0][0]
        print(f"\n{'=' * 60}")
        print(f"Use this Chat ID: {first_chat_id}")
        print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
