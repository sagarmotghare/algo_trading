import joblib
import yfinance as yf



import pandas as pd


import joblib
import yfinance as yf
import pandas as pd
import os
from logger import logger

# Model and trading state
model_path = os.path.join(os.path.dirname(__file__), 'models', '^NSEI.pkl')
loaded_model = joblib.load(model_path)
initial_balance = 100000  # Starting balance in INR
balance = initial_balance
position = 0  # Number of shares

# Load initial data
data = pd.read_excel("Old Data.xlsx")
old_data = data[["Close"]]

def message_handler(message):
    global balance, position
    print("Received message:", message)

    current_price = message["price"]
    df = pd.DataFrame({"Close": current_price}, index=[0])
    new_data = pd.concat([old_data, df], ignore_index=True)
    new_data['MA_10'] = new_data['Close'].rolling(window=10).mean()
    new_data['MA_50'] = new_data['Close'].rolling(window=50).mean()
    # Volume (if available, else fill with 0)
    if 'Volume' in old_data.columns:
        new_data['Volume'] = old_data['Volume'].tolist() + [message.get('volume', 0)]
    else:
        new_data['Volume'] = 0
    # Volatility (rolling std dev)
    new_data['Volatility_10'] = new_data['Close'].rolling(window=10).std()
    # RSI (Relative Strength Index)
    delta = new_data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    new_data['RSI_14'] = 100 - (100 / (1 + rs))
    # MACD (Moving Average Convergence Divergence)
    ema12 = new_data['Close'].ewm(span=12, adjust=False).mean()
    ema26 = new_data['Close'].ewm(span=26, adjust=False).mean()
    new_data['MACD'] = ema12 - ema26
    new_data = new_data.dropna()
    # Select only the last row for prediction, matching training features
    feature_cols = ['Close', 'MA_10', 'MA_50', 'Volume', 'Volatility_10', 'RSI_14', 'MACD']
    predict_input = new_data[feature_cols].tail(1)
    predict = loaded_model.predict(predict_input)
    predicted_price = predict[-1]

    # Debug: Print decision variables
    print(f"Predicted: {predicted_price}, Current: {current_price}, Balance: {balance}, Position: {position}")
    logger.info(f"Decision: Predicted={predicted_price}, Current={current_price}, Balance={balance}, Position={position}")

    # Calculate and log current profit after each request
    current_market_value = position * current_price
    unrealized_profit = current_market_value - (position * (message_handler.last_buy_price if message_handler.last_buy_price else 0))
    total_profit = balance + current_market_value - initial_balance
    print(f"Unrealized Profit: {unrealized_profit:.2f}, Total Profit: {total_profit:.2f}")
    logger.info(f"Unrealized Profit: {unrealized_profit:.2f}, Total Profit: {total_profit:.2f}")

    # Risk management parameters
    STOP_LOSS_PCT = 0.02  # 2% stop-loss
    TAKE_PROFIT_PCT = 0.04  # 4% take-profit

    # Improved buy logic:
    min_change_pct = 0.2 / 100  # 0.2%
    threshold = current_price * min_change_pct
    ma_10_rising = new_data['MA_10'].iloc[-1] > new_data['MA_10'].iloc[-2] if len(new_data['MA_10']) > 1 else True
    rsi_ok = new_data['RSI_14'].iloc[-1] < 70
    significant_prediction = predicted_price > current_price + threshold

    if significant_prediction and balance >= current_price and ma_10_rising and rsi_ok:
        max_shares = int(balance // current_price)
        shares_to_buy = max(int(max_shares * 0.5), 1)  # Buy 50% of possible shares, at least 1
        if shares_to_buy > 0:
            position += shares_to_buy
            balance -= shares_to_buy * current_price
            message_handler.last_buy_price = current_price
            logger.info(f"Scaling Buy: {shares_to_buy} shares at {current_price:.2f} (Threshold: {threshold:.2f}, MA10 rising: {ma_10_rising}, RSI: {new_data['RSI_14'].iloc[-1]:.2f})")
            print(f"Scaling Buy: {shares_to_buy} shares at {current_price:.2f} (Threshold: {threshold:.2f}, MA10 rising: {ma_10_rising}, RSI: {new_data['RSI_14'].iloc[-1]:.2f})")

    # Sell logic (scaling: sell 50% of position)
    elif position > 0:
        # Stop-loss and take-profit checks
        last_buy = message_handler.last_buy_price
        stop_loss_triggered = last_buy and current_price <= last_buy * (1 - STOP_LOSS_PCT)
        take_profit_triggered = last_buy and current_price >= last_buy * (1 + TAKE_PROFIT_PCT)
        model_sell_signal = predicted_price < current_price

        if stop_loss_triggered:
            logger.info(f"Stop-loss triggered: Bought at {last_buy:.2f}, Current {current_price:.2f}")
            print(f"Stop-loss triggered: Bought at {last_buy:.2f}, Current {current_price:.2f}")
        if take_profit_triggered:
            logger.info(f"Take-profit triggered: Bought at {last_buy:.2f}, Current {current_price:.2f}")
            print(f"Take-profit triggered: Bought at {last_buy:.2f}, Current {current_price:.2f}")
        if stop_loss_triggered or take_profit_triggered or model_sell_signal:
            shares_to_sell = max(int(position * 0.5), 1)  # Sell 50% of position, at least 1
            balance += shares_to_sell * current_price
            logger.info(f"Scaling Sell: {shares_to_sell} shares at {current_price:.2f}")
            print(f"Scaling Sell: {shares_to_sell} shares at {current_price:.2f}")
            position -= shares_to_sell
            if position == 0:
                message_handler.last_buy_price = None

# Initialize persistent attribute for buy price tracking
message_handler.last_buy_price = None

import time
def run_websocket():
    while True:
        try:
            with yf.WebSocket() as ws:
                ws.subscribe(["^NSEI"])
                ws.listen(message_handler)
        except Exception as e:
            print(f"WebSocket error: {e}. Reconnecting in 5 seconds...")
            logger.error(f"WebSocket error: {e}. Reconnecting in 5 seconds...")
            time.sleep(5)

run_websocket()

final_balance = balance + (position * old_data.iloc[-1]['Close'])
print(f"Final balance: {final_balance:.2f}")
print(f"Profit: {final_balance - initial_balance:.2f}")
def run_websocket():
    while True:
        try:
            with yf.WebSocket() as ws:
                ws.subscribe(["^NSEI"])
                ws.listen(message_handler)
        except Exception as e:
            print(f"WebSocket error: {e}. Reconnecting in 5 seconds...")
            logger.error(f"WebSocket error: {e}. Reconnecting in 5 seconds...")
            time.sleep(5)

run_websocket()

final_balance = balance + (position * old_data.iloc[-1]['Close'])
print(f"Final balance: {final_balance:.2f}")
print(f"Profit: {final_balance - initial_balance:.2f}")