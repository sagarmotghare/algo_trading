# 📈 AlgoTrading
An algorithmic trading system designed to train predictive models and operate on live market data.
## 🚀 Getting Started
### 1. Clone the Repository
```bash
git clone https://github.com/sagarmotghare/algo_trading.git
cd algo_trading
```
## 2. Install Dependencies
Make sure you have Python 3.8+ installed. Then install required packages:
```bash
pip install -r requirements.txt
```

## 🧠 Model Training
Before running live predictions, train the model using historical data:
```bash
python train.py
```
This will generate a serialized model file named ```^NSEI.pkl```.
## 📡 Live Trading
Once the model is trained, start live data processing:
```bash
python live.py
```
This script uses the trained model to make predictions based on real-time market data.
## 📁 Project Structure
```bash
algo_trading/
├── train.py         # Model training script
├── live.py          # Live data processing and prediction
├── requirements.txt # Python dependencies
└── ^NSEI.pkl        # Generated model file after training
```

## 🛠️ Notes
- Ensure internet connectivity for live data access.