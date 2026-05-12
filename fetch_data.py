import sqlite3
import yfinance as yf
import asyncio
import datetime
import sys
from dotenv import dotenv_values
import csv
import os
import websocket
import ast
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

config = dotenv_values(".env")
ticker = []
db_path = config["DB_PATH"]

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--multiple", action="store_true", help="Load tickers from CSV instead of .env")
args = parser.parse_args()

if args.multiple:
    with open(f"nifty_indexes.csv", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            ticker.append(row["Symbol"])
    db_path = "MultipleNifty2.db"
else:
    ticker = ast.literal_eval(config["TICKER"])

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def messages_create_table():
    with open('sql/messages_create.sql', 'r', encoding='utf-8') as f:
        messages_create_file = f.read()

    cursor.execute(messages_create_file)
    conn.commit()

message_count = 0
def message_handler(message: dict) -> None:
    global message_count
    message_count += 1
    if message_count >= 10:
        clear_console()
        message_count = 0 
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
    while True:
        try:
            async with yf.AsyncWebSocket() as ws:
                await ws.subscribe(ticker)
                await ws.listen(message_handler)        
        except TimeoutError:
            print("Timeout, retrying...")
            continue
        except websocket.exceptions.ConnectionClosedError:
            print("Connection lost, reconnecting...")
            continue
        except ConnectionError:
            print("Connection lost, reconnecting...")
            continue
        except KeyboardInterrupt:
            print("Shutting down...")
            break
        except Exception as e:
            print("Unexpected errorcontinue:", e)
            continue

if __name__ == "__main__":
    messages_create_table()
    asyncio.run(run_ws())