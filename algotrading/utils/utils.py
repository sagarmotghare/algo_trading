# utils.py
# Utility functions for algo_trading

def calculate_moving_avg(data):
    data['MA_10'] = data['Close'].rolling(window=10).mean()
    data['MA_50'] = data['Close'].rolling(window=50).mean()
    return data.dropna()

# Add more utility functions as needed
