import os
import sqlite3
import uuid
from backend.response_codes import ResponseCodes
from dotenv import load_dotenv

load_dotenv()

#Database configuration (can be configured in .env file)
DATABASE = os.getenv("DB_NAME", "urls.db")
SHORT_URL_LENGTH = int(os.getenv("SHORT_URL_LENGTH", 8))

# Persistent connection to SQLite database
_connection = sqlite3.connect(DATABASE, check_same_thread=False)
_connection.row_factory = sqlite3.Row

def init_db():
    _connection.execute('''
        CREATE TABLE IF NOT EXISTS urls (id INTEGER PRIMARY KEY, original_url TEXT NOT NULL UNIQUE, short_url TEXT NOT NULL UNIQUE, click_count INTEGER DEFAULT 0)
    ''')
    _connection.commit()

init_db()

# Function to get records from table where original_url or short_url matches
def get_records_from_table(original_url: str, short_url: str):
    query = "SELECT original_url, short_url FROM urls WHERE original_url=? OR short_url=?"
    rows = _connection.execute(query, (original_url, short_url)).fetchall()
    result = {"by_original": None, "by_short": None}
    for row in rows:
        if row["original_url"] == original_url:
            result["by_original"] = row["short_url"]
        if row["short_url"] == short_url:
            result["by_short"] = row["original_url"]
    return result

# Function to get long URL by short URL
def get_url_by_short(short_url: str):
    original_url = _connection.execute("SELECT original_url FROM urls WHERE short_url=?", (short_url,)).fetchone()
    if original_url is None:
        return ResponseCodes.NOT_FOUND, ""
    return ResponseCodes.SUCCESS, original_url

# Function to update the long URL with a short URL if provided otherwise generate a short URL
def insert_url(original_url: str, short_url: str):
    existing = get_records_from_table(original_url, short_url)
    if existing["by_short"] and existing["by_short"]!=original_url:
        return ResponseCodes.SHORT_URL_ALREADY_EXISTS, existing["by_short"]

    if existing["by_original"]:
        return ResponseCodes.ORIGINAL_URL_ALREADY_EXISTS, existing["by_original"]

    if short_url is None or short_url == "":
        max_retries = 5
        for attempt in range(max_retries):
            short_url = str(uuid.uuid4()).replace('-', '')[:SHORT_URL_LENGTH]
            try:
                _connection.execute("INSERT INTO urls (original_url, short_url) VALUES (?, ?)", (original_url, short_url))
                break
            except sqlite3.IntegrityError:
                if attempt == max_retries - 1:
                    return ResponseCodes.ERROR, ""
                continue
    else:
        _connection.execute("INSERT INTO urls (original_url, short_url) VALUES (?, ?)", (original_url, short_url))
    _connection.commit()
    return ResponseCodes.SUCCESS, short_url


def increment_clicks(short_url) -> None:
    _connection.execute("UPDATE urls SET click_count = click_count + 1 WHERE short_url=?", (short_url,))
    _connection.commit()

def get_counter(short_url: str):
    result = _connection.execute("SELECT click_count FROM urls WHERE short_url=?", (short_url,)).fetchone()
    return result["click_count"] if result else 0
    