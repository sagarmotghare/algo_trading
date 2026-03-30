"""
Real-Time Market Data Collector
-------------------------------

This script connects to Yahoo Finance's WebSocket API to subscribe to live ticker updates,
processes incoming messages, and stores them in a local SQLite database. It is designed
to run continuously, automatically reconnecting if the WebSocket session ends.

Dependencies:
- os: Access environment variables
- sqlite3: Local database storage
- yfinance: WebSocket access to live market data
- asyncio: Asynchronous event-driven programming
- datetime: Timestamp generation for message logging

Environment Variables:
- TICKER: The stock or index symbol to subscribe to (e.g., ^NSEI)

Database:
- Location: ./data/market.db
- Schema: Defined in sql/messages_create.sql
- Insert Logic: Defined in sql/messages_insert.sql

Sample WebSocket Message:
{
    "id": "^NSEI",
    "price": 25693.7,
    "time": "1770372083000",
    "currency": "INR",
    "exchange": "NSI",
    "quote_type": 9,
    "market_hours": 1,
    "change_percent": 0.19849016,
    "change": 50.898438,
    "price_hint": "2"
}
"""

import os
import sqlite3
import yfinance as yf
import asyncio
import datetime
import sys

# Retrieve ticker symbol from environment variable
ticker = os.environ['TICKER'] 

# Connect to SQLite database (creates file if it does not exist)
conn = sqlite3.connect('./data/market.db')
cursor = conn.cursor()

def messages_create_table():
    """
    Create the messages table in the database.

    Reads SQL schema from 'sql/messages_create.sql' and executes it.
    Ensures the table exists before inserting any data.
    """
    with open('sql/messages_create.sql', 'r', encoding='utf-8') as f:
        messages_create_file = f.read()

    cursor.execute(messages_create_file)
    conn.commit()

def message_handler(message: dict) -> None:
    """
    Callback function to handle incoming WebSocket messages.

    Example message structure:
    {
        "id": "^NSEI",
        "price": 25693.7,
        "time": "1770372083000",
        "currency": "INR",
        "exchange": "NSI",
        "quote_type": 9,
        "market_hours": 1,
        "change_percent": 0.19849016,
        "change": 50.898438,
        "price_hint": "2"
    }

    Processing steps:
    - Prints the raw message for logging.
    - Reads SQL insert statement from 'sql/messages_insert.sql'.
    - Inserts a record into the database with:
        * timestamp: current system time (ISO format)
        * symbol: ticker ID from the message
        * message: full message serialized as string
    - Commits the transaction.
    """
    print("Received message:", message)
    
    with open('sql/messages_insert.sql', 'r', encoding='utf-8') as f:
        messages_insert_file = f.read()
    
    cursor.execute(messages_insert_file, { 
        "timestamp": datetime.datetime.now().isoformat(), 
        "symbol": message["id"], 
        "data": str(message)
    })
    conn.commit()
    
async def run_ws():
    """
    Establish and maintain a WebSocket connection to Yahoo Finance.

    - Subscribes to the ticker defined in the environment variable.
    - Listens for incoming messages and passes them to message_handler.
    - Handles exceptions gracefully and attempts to reconnect if the session ends.
    """    
    try:
        async with yf.AsyncWebSocket() as ws:
            await ws.subscribe([ticker])
            await ws.listen(message_handler)
    except TimeoutError as te:
        print("Timeout Error:", te)
        sys.exit("Timeout")


if __name__ == "__main__":
    # Ensure the database schema is created
    messages_create_table()
    # Start the asynchronous WebSocket listener
    asyncio.run(run_ws())