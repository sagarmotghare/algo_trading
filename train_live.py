# !pip install yfinance pandas scikit-learn matplotlib
import pandas as pd
from logger2 import setup_logger
from datetime import datetime
from sklearn.linear_model import LinearRegression
import pytz

current_filename = __file__.split("\\")[-1][:-3]
logger = setup_logger(current_filename)
data = pd.read_excel("Old Data.xlsx").set_index("Datetime")
data.index = pd.to_datetime(data.index).tz_localize(pytz.UTC)
model = LinearRegression()

def download_data(ticker):
    global data
    import yfinance as yf
    download_data = yf.download(ticker, period="max",interval="1m").droplevel(level=1, axis=1)
    data = pd.concat([data, download_data])    
    return data

def save_data(temp_data, ticker):
    from datetime import datetime
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"{ticker}_{formatted_time}.xlsx"    
    temp_data.index = temp_data.index.astype(str)
    temp_data.to_excel(file_name)

def calculate_moving_avg(data):
    # Calculate moving averages
    data['MA_10'] = data['Close'].rolling(window=10).mean()
    data['MA_50'] = data['Close'].rolling(window=50).mean()    
    # Drop NaN values
    return data.dropna()

def get_train_test_data(data):
    # Define features and target
    X = data[['Close', 'MA_10', 'MA_50']]
    y = data['Close'].shift(-1).dropna()
    X = X[:-1]
    # Split data into training and testing sets
    from sklearn.model_selection import train_test_split
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_model(X_train, X_test, y_train, y_test):    
    model.fit(X_train, y_train)
    
    predictions = model.predict(X_test)
    
    from sklearn.metrics import mean_squared_error, r2_score
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    print(f'Mean Squared Error: {mse}')
    print(f'R² Score: {r2}')
    return model, predictions

def plot_graph(y_test,predictions):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(14, 7))
    plt.plot(y_test.index, y_test.values, label='Actual Price')
    plt.plot(y_test.index, predictions, label='Predicted Price')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Actual vs. Predicted Stock Prices')
    plt.legend()
    plt.show()

def save_model(model,filename):
    import joblib
    joblib.dump(model, filename)

# live_data = pd.DataFrame(columns=["Close", "MA_10", "MA_50"])
initial_balance = 100000  # Starting balance in INR
balance = initial_balance   
position = 0  # Number of shares
live_data = pd.DataFrame(columns=["Close", "MA_10", "MA_50"])

def message_handler(message):
    try:  
        global balance, position,live_data
        print("Received message:", message)

        current_price = message["price"]
        time = datetime.fromtimestamp(int(message["time"])/1000, tz=pytz.UTC)        
        
        df = pd.DataFrame({
            "Close": current_price,
            "MA_10": live_data["MA_10"][-9:].mean(),
            "MA_50": live_data["MA_50"][-49:].mean()
        }, index=[time])
        live_data = pd.concat([live_data, df])
        predict = model.predict(df)
        predicted_price = predict[0]        
        
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

    except Exception as e:
        print(f"An error occurred: {e}")
        exit(0)

def go_live(): 
    import yfinance as yf    
    
    with yf.WebSocket() as ws:
        try:
            ws.subscribe(tickers)
            ws.listen(message_handler)
        except ValueError:
            ws.close()

if __name__ == "__main__":
    tickers = ["^NSEI"]
    for ticker in tickers:
        data = download_data(ticker)
        # save_data(data, ticker)

        data = calculate_moving_avg(data)
        X_train, X_test, y_train, y_test = get_train_test_data(data)
        model, predictions =  train_model(X_train, X_test, y_train, y_test)
        # plot_graph(y_test, predictions)    

        save_model(model, ticker+".pkl")
    live_data = data
    go_live()