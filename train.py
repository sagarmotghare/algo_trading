# !pip install yfinance pandas scikit-learn matplotlib

def download_data(ticker):
    import yfinance as yf
    data = yf.download(ticker, period="max",interval="1m")
    # Display the first few rows of the dataset
    data = data.droplevel(level=1, axis=1)
    return data

def save_data(temp_data, ticker):
    from datetime import datetime
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"{ticker}{formatted_time}.xlsx"
    temp_data.index = temp_data.index.tz_localize(None)
    temp_data.to_excel(file_name)

def calculate_moving_avg(data):
    # Calculate moving averages
    data['MA_10'] = data['Close'].rolling(window=10).mean()
    data['MA_50'] = data['Close'].rolling(window=50).mean()
    # Volume
    if 'Volume' in data.columns:
        data['Volume'] = data['Volume']
    # Volatility (rolling std dev)
    data['Volatility_10'] = data['Close'].rolling(window=10).std()
    # RSI (Relative Strength Index)
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['RSI_14'] = 100 - (100 / (1 + rs))
    # MACD (Moving Average Convergence Divergence)
    ema12 = data['Close'].ewm(span=12, adjust=False).mean()
    ema26 = data['Close'].ewm(span=26, adjust=False).mean()
    data['MACD'] = ema12 - ema26
    # Drop NaN values
    return data.dropna()

def get_train_test_data(data):
    # Define features and target
    feature_cols = ['Close', 'MA_10', 'MA_50', 'Volume', 'Volatility_10', 'RSI_14', 'MACD']
    X = data[[col for col in feature_cols if col in data.columns]]
    y = data['Close'].shift(-1).dropna()
    X = X[:-1]
    # Split data into training and testing sets
    from sklearn.model_selection import train_test_split
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_model(X_train, X_test, y_train, y_test):
    from sklearn.linear_model import LinearRegression
    # Initialize and train the model
    model = LinearRegression()
    model.fit(X_train, y_train)
    # Make predictions
    predictions = model.predict(X_test)
    # Evaluate the model
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
    import os
    models_dir = os.path.join(os.path.dirname(__file__), 'models')
    os.makedirs(models_dir, exist_ok=True)
    filepath = os.path.join(models_dir, filename)
    joblib.dump(model, filepath)

if __name__ == "__main__":
    ticker = '^NSEI'
    data = download_data(ticker)

    save_data(data, ticker)

    data = calculate_moving_avg(data)

    X_train, X_test, y_train, y_test = get_train_test_data(data)
    model, predictions =  train_model(X_train, X_test, y_train, y_test)

    # plot_graph(y_test, predictions)    

    save_model(model, ticker+".pkl")