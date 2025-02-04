import pandas as pd
import logging
import re
import os
import emoji
import sqlite3

# Ensure required directories exist
os.makedirs("logs", exist_ok=True)
os.makedirs("data/cleaned", exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/data_cleaning.log"),  # Log to file
        logging.StreamHandler()  # Log to console
    ]
)

# ✅ Load CSV
def load_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        logging.info(f"✅ CSV file '{file_path}' loaded successfully.")
        return df
    except Exception as e:
        logging.error(f"❌ Error loading CSV file: {e}")
        raise

# ✅ Extract & Remove Emojis
def extract_emojis(text):
    emojis = ''.join(c for c in text if c in emoji.EMOJI_DATA)
    return emojis if emojis else "No emoji"

def remove_emojis(text):
    return ''.join(c for c in text if c not in emoji.EMOJI_DATA)

# ✅ Extract & Remove YouTube Links
def extract_youtube_links(text):
    youtube_pattern = r"(https?://(?:www\.)?(?:youtube\.com|youtu\.be)/[^\s]+)"
    links = re.findall(youtube_pattern, text)
    return ', '.join(links) if links else "No YouTube link"

def remove_youtube_links(text):
    youtube_pattern = r"https?://(?:www\.)?(?:youtube\.com|youtu\.be)/[^\s]+"
    return re.sub(youtube_pattern, '', text).strip()

# ✅ Standardize Text
def clean_text(text):
    if pd.isna(text):
        return "No Message"
    return re.sub(r'\n+', ' ', text).strip()

# ✅ Clean DataFrame
def clean_dataframe(df):
    try:
        df = df.drop_duplicates(subset=["ID"]).copy()
        logging.info("✅ Duplicates removed.")

        # ✅ Convert Date to datetime format
        df.loc[:, 'Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df.loc[:, 'Date'] = df['Date'].where(df['Date'].notna(), None)
        logging.info("✅ Date formatted.")

        # ✅ Convert 'ID' to integer
        df.loc[:, 'ID'] = pd.to_numeric(df['ID'], errors="coerce").fillna(0).astype(int)

        # ✅ Fill missing values
        df.loc[:, 'Message'] = df['Message'].fillna("No Message")
        df.loc[:, 'Media Path'] = df['Media Path'].fillna("No Media")

        # ✅ Standardize text columns
        df.loc[:, 'Channel Title'] = df['Channel Title'].str.strip()
        df.loc[:, 'Channel Username'] = df['Channel Username'].str.strip()
        df.loc[:, 'Message'] = df['Message'].apply(clean_text)
        df.loc[:, 'Media Path'] = df['Media Path'].str.strip()

        # ✅ Extract & Remove Emojis
        df.loc[:, 'emoji_used'] = df['Message'].apply(extract_emojis)
        df.loc[:, 'Message'] = df['Message'].apply(remove_emojis)

        # ✅ Extract & Remove YouTube Links
        df.loc[:, 'youtube_links'] = df['Message'].apply(extract_youtube_links)
        df.loc[:, 'Message'] = df['Message'].apply(remove_youtube_links)

        # ✅ Rename columns for consistency
        df = df.rename(columns={
            "Channel Title": "channel_title",
            "Channel Username": "channel_username",
            "ID": "message_id",
            "Message": "message",
            "Date": "message_date",
            "Media Path": "media_path",
            "emoji_used": "emoji_used",
            "youtube_links": "youtube_links"
        })

        logging.info("✅ Data cleaning completed successfully.")
        return df
    except Exception as e:
        logging.error(f"❌ Data cleaning error: {e}")
        raise

# ✅ Save Cleaned Data
def save_cleaned_data(df, output_path):
    try:
        df.to_csv(output_path, index=False)
        logging.info(f"✅ Cleaned data saved to '{output_path}'.")
    except Exception as e:
        logging.error(f"❌ Error saving cleaned data: {e}")
        raise

# ✅ Store Data in Database
def save_to_database(df, db_path="data/medical_data.db"):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # ✅ Create table if it doesn’t exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                message_id INTEGER PRIMARY KEY,
                channel_title TEXT,
                channel_username TEXT,
                message TEXT,
                message_date TEXT,
                media_path TEXT,
                emoji_used TEXT,
                youtube_links TEXT
            )
        ''')

        # ✅ Insert data
        df.to_sql("messages", conn, if_exists="append", index=False)
        conn.commit()
        conn.close()

        logging.info(f"✅ Data saved to database '{db_path}'.")
    except Exception as e:
        logging.error(f"❌ Database error: {e}")
        raise

# ✅ Main Execution
if __name__ == "__main__":
    file_path = "data/raw/messages.csv"
    output_path = "data/cleaned/cleaned_data.csv"

    df = load_csv(file_path)
    df = clean_dataframe(df)
    save_cleaned_data(df, output_path)
    save_to_database(df)