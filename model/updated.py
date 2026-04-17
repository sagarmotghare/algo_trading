# =========================
# Getting Data
# =========================
import sqlite3
import pandas as pd

with sqlite3.connect("market.db") as conn:
    df = pd.read_sql_query('SELECT * FROM messages', conn)

print("From", df.iloc[0]['timestamp'], "Till", df.iloc[-1]['timestamp'])

# =========================
# Preparing Data
# =========================
import ast

data = pd.json_normalize(df["data"].apply(lambda x: ast.literal_eval(x)))
data.time = pd.to_datetime(data.time, unit="ms")
data.drop_duplicates(inplace=True)

X = data["price"].iloc[:-1].values.reshape(-1,1)
y = data["price"].shift(-1).iloc[:-1].values.reshape(-1, 1)

# =========================
# Dataset
# =========================
import torch
from torch.utils.data import Dataset, DataLoader

class PriceDataset(Dataset):
    def __init__(self, X, y):
        self.X = X
        self.y = y
    def __len__(self):
        return len(self.X)
    def __getitem__(self, idx):
        return torch.tensor(self.X[idx], dtype=torch.float32), torch.tensor(self.y[idx], dtype=torch.float32)

# =========================
# Models
# =========================
import torch.nn as nn

class PricePredictorFF(nn.Module):
    def __init__(self, input_size=1, output_size=1, hidden_dims=[64, 32]):
        super().__init__()
        layers = []
        prev_dim = input_size
        for h in hidden_dims:
            layers.append(nn.Linear(prev_dim, h))
            layers.append(nn.ReLU())
            prev_dim = h
        layers.append(nn.Linear(prev_dim, output_size))
        self.layer = nn.Sequential(*layers)

    def forward(self, x):
        return self.layer(x)

class PricePredictorRNN(nn.Module):
    def __init__(self, input_size=1, hidden_size=64, num_layers=2, output_size=1):
        super().__init__()
        self.rnn = nn.RNN(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True
        )
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        if x.dim() == 2:
            x = x.unsqueeze(1)
        out, hidden = self.rnn(x)
        out = out[:, -1, :]
        return self.fc(out)

class PricePredictorLSTM(nn.Module):
    def __init__(self, input_size=1, hidden_size=64, num_layers=2, output_size=1, batch_first=True):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size = input_size,
            hidden_size = hidden_size,
            num_layers = num_layers,
            batch_first = batch_first)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        if x.dim() == 2:
            x = x.unsqueeze(1)
        out, _ = self.lstm(x)
        return self.fc(out[:, -1, :])

# =========================
# Scaling & Split
# =========================
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

scaler_X = MinMaxScaler()
scaler_y = MinMaxScaler()

X_scaled = scaler_X.fit_transform(X)
y_scaled = scaler_y.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y_scaled, test_size=0.2, shuffle=False
)

train_dataset = PriceDataset(X_train, y_train)
test_dataset = PriceDataset(X_test, y_test)

batch_size = 256
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

# =========================
# Training Function
# =========================
import torch.optim as optim
from tqdm import tqdm

def train_model(model, train_loader, epochs=10):
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    with tqdm(total=epochs, desc=model.__class__.__name__) as pbar:
        for epoch in range(epochs):
            model.train()
            epoch_loss = 0.0
        
            for batch_X, batch_y in train_loader:
                outputs = model(batch_X)
                loss = criterion(outputs, batch_y)

                optimizer.zero_grad()
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
                optimizer.step()

                epoch_loss += loss.item()
        
            pbar.update(epoch+1)
            pbar.set_postfix({"Loss": epoch_loss/len(train_loader)})        
    
    return model, criterion
# =========================
# Evaluation Function
# =========================
import numpy as np

def evaluate_model(model, test_loader, criterion, scaler_y):
    model.eval()
    with torch.no_grad():
        test_losses = []
        all_preds, all_targets = [], []
        for batch_X, batch_y in test_loader:
            preds = model(batch_X)
            loss = criterion(preds, batch_y)
            test_losses.append(loss.item())

            all_preds.append(preds.detach().numpy())
            all_targets.append(batch_y.detach().numpy())

        print(f"{model.__class__.__name__} Average Test Loss: {sum(test_losses)/len(test_losses):.10f}")

    all_preds = np.vstack(all_preds)
    all_targets = np.vstack(all_targets)

    predictions_rescaled = scaler_y.inverse_transform(all_preds)
    y_test_rescaled = scaler_y.inverse_transform(all_targets)

    return predictions_rescaled, y_test_rescaled

# =========================
# Trading Simulation
# =========================
def simulate_trading(predictions_rescaled, y_test_rescaled, initial_balance=100000):
    balance = initial_balance
    stock = 0

    def trade(signal, stock_price):
        nonlocal balance, stock
        if signal == "BUY" and balance > 0:
            stock += balance / stock_price
            balance = 0
        elif signal == "SELL" and stock > 0:
            balance += stock * stock_price
            stock = 0

    for i in range(len(y_test_rescaled)):
        predicted_value = predictions_rescaled[i][0]
        current_value = y_test_rescaled[i][0]

        signal = None
        if predicted_value > current_value:
            signal = "BUY"
        elif predicted_value < current_value:
            signal = "SELL"
        trade(signal, current_value)

    # Final liquidation
    trade("SELL", current_value)

    profit = balance - initial_balance
    print("Final =>", "Balance:", balance,
          "Profit" if profit > 0 else "Loss",
          abs(profit), "%",
          (abs(profit) / initial_balance) * 100)

# =========================
# Run Both Models
# =========================
# FeedForward
ff_model = PricePredictorFF(input_size=4, output_size=1, hidden_dims=[64, 32])
ff_model, ff_criterion = train_model(ff_model, train_loader, epochs=100)
ff_preds, ff_targets = evaluate_model(ff_model, test_loader, ff_criterion, scaler_y)
simulate_trading(ff_preds, ff_targets)
torch.save(ff_model, "stock_prediction_ff.pth")

# RNN
rnn_model = PricePredictorRNN(input_size=4, hidden_size=64, num_layers=2, output_size=1)
rnn_model, rnn_criterion = train_model(rnn_model, train_loader, epochs=100)
rnn_preds, rnn_targets = evaluate_model(rnn_model, test_loader, rnn_criterion, scaler_y)
simulate_trading(rnn_preds, rnn_targets)
torch.save(rnn_model, "stock_prediction_rnn.pth")

# LSTM
lstm_model = PricePredictorLSTM(input_size=4, hidden_size=64, num_layers=2, output_size=1)
lstm_model, lstm_criterion = train_model(lstm_model, train_loader, epochs=100)
lstm_preds, lstm_targets = evaluate_model(lstm_model, test_loader, lstm_criterion, scaler_y)
simulate_trading(lstm_preds, lstm_targets)
torch.save(lstm_model, "stock_prediction_lstm.pth")

# =========================
# Combined Visualization
# =========================
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt

rows = 3
cols = 3

total_graph = rows * cols
fig, axs = plt.subplots(rows, cols, figsize=(12,10))

max_limit = 0
min_limit = 0

for row in range(rows):
  for col in range(cols):
    max_limit = min_limit + len(ff_targets)//total_graph

    axs[row][col].plot(ff_targets[min_limit:max_limit], label="Actual Prices", color="black")
    axs[row][col].plot(ff_preds[min_limit:max_limit], label="FeedForward", color="blue")
    axs[row][col].plot(rnn_preds[min_limit:max_limit], label="RNN", color="red")
    axs[row][col].plot(lstm_preds[min_limit:max_limit], label="LSTM", color="green")
    axs[row][col].legend()
    # axs[row][col].set_title("")

    min_limit = max_limit

fig.suptitle("Price Prediction Comparison: FF vs RNN vs LSTM")
plt.tight_layout()
plt.show()