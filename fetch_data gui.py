import os
import sqlite3
import yfinance as yf
import asyncio
import datetime
import sys
import threading
import tkinter as tk
from tkinter import ttk
from dotenv import dotenv_values
import queue

msg_queue = queue.Queue()

# Load config
config = {
    "TICKER": "^NSEI",
    "DB_PATH": "test.db"
    }
ticker = config["TICKER"]

conn = sqlite3.connect(config["DB_PATH"])
cursor = conn.cursor()

# --- Database setup ---
def messages_create_table():
    with open('sql/messages_create.sql', 'r', encoding='utf-8') as f:
        messages_create_file = f.read()
    cursor.execute(messages_create_file)
    conn.commit()

def message_handler(message: dict) -> None:
    # Insert into DB
    msg_queue.put(message)    

# --- Async WebSocket ---
async def run_ws():
    try:
        async with yf.AsyncWebSocket() as ws:
            await ws.subscribe([ticker])
            await ws.listen(message_handler)
    except TimeoutError as te:
        print("Timeout Error:", te)
        sys.exit("Timeout")

def start_ws_loop():
    asyncio.run(run_ws())

# --- GUI Setup ---
root = tk.Tk()
root.title("AlgoTrading: Live Data")

frm = ttk.Frame(root, padding=10)
frm.grid(sticky="nsew")

# Table
columns = ("Timestamp", "Symbol", "Price", "Change")
tree = ttk.Treeview(frm, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

tree.grid(row=0, column=0, sticky="nsew")

# Scrollbar
scrollbar = ttk.Scrollbar(frm, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.grid(row=0, column=1, sticky="ns")

# Expand to fill window
frm.rowconfigure(0, weight=1)
frm.columnconfigure(0, weight=1)

def process_queue():
    while not msg_queue.empty():
        message = msg_queue.get()
        # insert into DB
        with open('sql/messages_insert.sql', 'r', encoding='utf-8') as f:
            messages_insert_file = f.read()
        cursor.execute(messages_insert_file, {
            "timestamp": datetime.datetime.now().isoformat(),
            "symbol": message["id"],
            "data": str(message)
        })
        conn.commit()
        # update GUI
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tree.insert("", 0, values=(ts, message["id"], message.get("price", ""), message.get("change", "")))
    root.after(100, process_queue)  # keep polling

# start polling loop
process_queue()

# --- Run ---
if __name__ == "__main__":
    messages_create_table()
    # Run WebSocket in background thread so GUI stays responsive
    threading.Thread(target=start_ws_loop, daemon=True).start()
    root.mainloop()
