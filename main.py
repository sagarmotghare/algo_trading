import asyncio
import yfinance as yf

import sqlite3
import datetime

conn = sqlite3.connect("nifty50.db")
cursor = conn.cursor()

# CREATE TABLE IF NOT EXISTS messages (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     price REAL,    
#     time TEXT,
#     symbol TEXT,
#     exchange TEXT,
#     quote_type INTEGER,
#     market_hours INTEGER,
#     change_percent REAL,
#     change REAL,
#     open_price REAL,
#     price_hint INTEGER
# )
# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    symbol TEXT,
    data TEXT
)
""")
conn.commit()

# Define a callback function to handle messages
def message_handler(message):
    symbol = message["id"]    
    ts = datetime.datetime.now().isoformat()
    cursor.execute("INSERT INTO messages (timestamp, symbol, data) VALUES (?, ?, ?)",
                   (ts, symbol, str(message)))
    conn.commit()
    print("Received message:", message)

async def run_ws():
    while True:
        try:
            async with yf.AsyncWebSocket() as ws:
                await ws.subscribe(["^NSEI"])  # NIFTY 50 index
                await ws.listen( message_handler)
        except Exception as e:
            print("WebSocket error:", e)

        # Reconnect immediately
        print("Session ended. Reconnecting now...")

asyncio.run(run_ws())

# {'id': '^NSEI', 'price': 25693.7, 'time': '1770372083000', 'currency': 'INR', 'exchange': 'NSI', 'quote_type': 9, 'market_hours': 1, 'change_percent': 0.19849016, 'change': 50.898438, 'price_hint': '2'}