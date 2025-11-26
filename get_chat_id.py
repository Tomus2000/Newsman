"""Helper script to get your Telegram chat ID.
1. Start a chat with your bot: t.me/Newsman2000_bot
2. Send any message to the bot (e.g., /start)
3. Run this script to get your chat_id
"""

import os
import sys

# Set your bot token
os.environ["TELEGRAM_BOT_TOKEN"] = "8361912731:AAHkHX7zRnpgLLbzCo1y1e9Ii0yEpFe6SWQ"

# Import after setting env var to avoid config errors
import sys
sys.path.insert(0, '.')

# Set chat_id to empty string to avoid config error
os.environ["TELEGRAM_CHAT_ID"] = ""

from telegram_sender import get_updates, get_bot_info

if __name__ == "__main__":
    print("=" * 60)
    print("Getting bot information...")
    print("=" * 60)
    
    bot_info = get_bot_info()
    if bot_info.get("ok"):
        bot = bot_info.get("result", {})
        print(f"Bot Name: {bot.get('first_name')}")
        print(f"Bot Username: @{bot.get('username')}")
        print(f"Bot ID: {bot.get('id')}")
    else:
        print("Error: Could not get bot info. Check your bot token.")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("Getting recent messages...")
    print("=" * 60)
    print("\nMake sure you've sent a message to your bot first!")
    print("Go to: t.me/Newsman2000_bot and send /start\n")
    
    updates = get_updates()
    
    if not updates:
        print("No messages found. Please:")
        print("1. Open Telegram and go to: t.me/Newsman2000_bot")
        print("2. Click 'Start' or send any message")
        print("3. Run this script again")
    else:
        print(f"Found {len(updates)} recent message(s):\n")
        chat_ids = set()
        for update in updates:
            message = update.get("message", {})
            chat = message.get("chat", {})
            chat_id = chat.get("id")
            chat_name = chat.get("first_name") or chat.get("title") or "Unknown"
            chat_ids.add((chat_id, chat_name))
        
        print("Your Chat ID(s):")
        for chat_id, chat_name in chat_ids:
            print(f"  {chat_id} ({chat_name})")
        
        if chat_ids:
            first_chat_id = list(chat_ids)[0][0]
            print(f"\n{'='*60}")
            print(f"Use this Chat ID: {first_chat_id}")
            print(f"{'='*60}")

