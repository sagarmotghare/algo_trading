import joblib
import yfinance as yf
import pandas as pd
from logger import logger
from train import calculate_parameters

loaded_model = joblib.load('^NSEI.pkl')
initial_balance = 100000  # Starting balance in INR
balance = initial_balance
position = 0  # Number of shares

data = pd.read_excel("Old Data.xlsx")
old_data = data[["Close"]]
live_data = pd.DataFrame()

BUY = "BUY"
SELL = "SELL"
def get_signal(current_row, previous_row, predicted_price):
    current_price = current_row["Close"]
    min_change_pct = 0.2 / 100  # 0.2%
    threshold = current_price * min_change_pct
    significant_prediction = predicted_price > current_price + threshold
    ma_10_rising = current_row['MA_10'] > previous_row['MA_10'] if 'MA_10' in previous_row else True
    rsi_ok = current_row['RSI_14'] < 70
    print(f"predicted_price: {predicted_price} significant_prediction: {significant_prediction} balance: {balance} current_price: {current_price} ma_10_rising: {ma_10_rising} rsi: {current_row['RSI_14']} rsi_ok: {rsi_ok}")    
    if significant_prediction and balance >= current_price and ma_10_rising and rsi_ok:
        return BUY
    elif predicted_price < current_price and position>0:
        return SELL
    else:
        return None

stocks = pd.DataFrame()
def message_handler(message):
    global balance, position, live_data, stocks
    # print(message)
    
    current_price = message["price"]
    current_time = pd.to_datetime(float(message["time"]), unit='ms')
    df = pd.DataFrame({
        "Close": current_price
    }, index=[current_time])    
    df.index = pd.to_datetime(df.index)
    live_data = pd.concat([live_data, df]).resample('1min').agg(
        Open=("Close", "first"),
        High=("Close", "max"),
        Low=("Close", "min"),
        Close=("Close", "last"),
        )
    live_data["Volume"] = 0
    new_data = calculate_parameters(live_data.dropna())    
    print(new_data.shape, live_data.shape)
    
    if new_data.shape[0] <= 0 :
        return
    
    predict = loaded_model.predict(new_data)
    predicted_price = predict[-1]

    signal = get_signal(new_data.iloc[-1], new_data.iloc[-2] if new_data.shape[0] > 1 else {}, predicted_price)
    if  signal == BUY:    
        # Buy stock
        shares_to_buy = int(balance // current_price)  # Buy whole shares only
        if shares_to_buy > 0:  # Ensure we are buying at least one share
            position += shares_to_buy
            balance -= shares_to_buy * current_price
            logger.info(f"Buying {shares_to_buy} shares at {current_price:.2f}")            
            stocks = pd.concat([stocks, pd.DataFrame({"Stock": shares_to_buy, "Price": current_price}, index=[current_time])])
    elif signal == SELL:
        # Sell stock
        balance += position * current_price
        logger.info(f"Selling {position} shares at {current_price:.2f}")
        position = 0

# # live
# with yf.WebSocket() as ws:
#     ws.subscribe(["^NSEI"])
#     ws.listen(message_handler)

# backtest
import yfinance as yf
yf_data = yf.download("^NSEI", period="2d",interval="1m")
yf_data.index = yf_data.index.tz_convert("Asia/Kolkata")    
yf_data = yf_data.droplevel(level=1, axis=1)
d = calculate_parameters(yf_data)

for index ,row in d.iterrows():
    message_handler({"price": row["Close"], "time": pd.Timestamp(index, unit='s').value // 10**6})

final_balance = balance + (position * old_data.iloc[-1]['Close'])
profit = final_balance - initial_balance
print(f"Final balance: {final_balance:.2f}")
print(f"Profit: {profit:.2f}")
live_data.to_csv("Test.csv")