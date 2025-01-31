import logging
import requests
import pandas as pd
from config import BOT_TOKEN, CHANNELS

# Set up logging
logging.basicConfig(filename="logs/scraper.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Telegram API URL
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def get_channel_messages(channel):
    """
    Fetches messages from a public Telegram channel using the bot.
    """
    try:
        url = f"{BASE_URL}/getUpdates"
        response = requests.get(url)
        data = response.json()

        if data.get("ok"):
            messages = []
            for result in data.get("result", []):
                message_data = result.get("message", {})
                if "text" in message_data:
                    messages.append({
                        "channel": channel,
                        "message_id": message_data.get("message_id"),
                        "date": message_data.get("date"),
                        "text": message_data.get("text")
                    })
            return messages
        else:
            logging.error(f"Failed to fetch messages from {channel}: {data}")
            return None
    except Exception as e:
        logging.error(f"Error fetching messages from {channel}: {e}")
        return None

def save_messages_to_csv(messages, filename="data/raw/messages.csv"):
    """
    Saves scraped messages to a CSV file.
    """
    df = pd.DataFrame(messages)
    df.to_csv(filename, index=False, mode='a', header=not bool(pd.read_csv(filename).shape[0]))
    logging.info(f"Saved {len(messages)} messages to {filename}")

def main():
    all_messages = []
    
    for channel in CHANNELS:
        messages = get_channel_messages(channel)
        if messages:
            all_messages.extend(messages)
    
    if all_messages:
        save_messages_to_csv(all_messages)
        print(f"✅ Scraped {len(all_messages)} messages successfully!")

if __name__ == "__main__":
    main()
