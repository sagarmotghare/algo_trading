import joblib
import yfinance as yf
import pandas as pd
from logger import logger

loaded_model = joblib.load('^NSEI.pkl')
initial_balance = 100000  # Starting balance in INR
balance = initial_balance
position = 0  # Number of shares

data = pd.read_excel("Old Data.xlsx")
old_data = data[["Close"]]

def message_handler(message):
    global balance, position    
    print("Received message:", message)    

    current_price = message["price"]
    df = pd.DataFrame({"Close": current_price }, index=[0])
    new_data = pd.concat([old_data, df], ignore_index=True)
    new_data['MA_10'] = new_data['Close'].rolling(window=10).mean()
    new_data['MA_50'] = new_data['Close'].rolling(window=50).mean()
    new_data = new_data.dropna()
    
    predict = loaded_model.predict(new_data)
    predicted_price = predict[-1]        

    if predicted_price > current_price and balance >= current_price:
        # Buy stock
        shares_to_buy = int(balance // current_price)  # Buy whole shares only
        if shares_to_buy > 0:  # Ensure we are buying at least one share
            position += shares_to_buy
            balance -= shares_to_buy * current_price
            logger.info(f"Buying {shares_to_buy} shares at {current_price:.2f}")            

    elif predicted_price < current_price and position > 0:
        # Sell stock
        balance += position * current_price
        logger.info(f"Selling {position} shares at {current_price:.2f}")
        position = 0

with yf.WebSocket() as ws:
    ws.subscribe(["^NSEI"])
    ws.listen(message_handler)    

final_balance = balance + (position * old_data.iloc[-1]['Close'])
profit = final_balance - initial_balance
print(f"Final balance: {final_balance:.2f}")
print(f"Profit: {profit:.2f}")