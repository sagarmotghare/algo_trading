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
This will generate a serialized model file named `^NSEI.pkl`.
## 📡 Live Trading
Once the model is trained, start live data processing:
```bash
python live.py
```
This script uses the trained model to make predictions based on real-time market data.
## 📁 Project Structure
```bash
algo_trading/
├── ^NSEI.pkl        # Generated model file after training
├── train.py         # Model training script
├── live.py          # Live data processing and prediction
├── requirements.txt # Python dependencies
├── start.bat        # Launch script with PID tracking
└── stop.bat         # Terminates the running Python process
└── schedule.bat     # Registers daily start/stop tasks via Task Scheduler
```
🖥️ Batch Scripts
- main.bat: Central controller script supporting multiple flags:
    - `--start`: Activates the virtual environment (if present), launches `live.py`, and saves the Python process ID to `pid.txt`.
    - `--stop`: Reads the PID from `pid.txt` and terminates the corresponding Python process.
    - `--schedule`: Self-elevates to Administrator and registers two scheduled tasks using Windows Task Scheduler:
        - Runs `main.bat --start` daily at 9:10 AM
        - Runs `main.bat --stop` daily at 3:35 PM
    - --shortcut: Creates three desktop shortcuts:
        - StartAlgoTrading.lnk → runs `main.bat --start`
        - StopAlgoTrading.lnk → runs `main.bat --stop`
        - ScheduleAlgoTrading.lnk → runs `main.bat --schedule`

💡 To apply the schedule, run `main.bat --schedule`. It will request elevation automatically if needed.


## 🛠️ Notes
- Ensure internet connectivity for live data access.
- Use `start.bat` to launch the system and `stop.bat` to terminate it cleanly.
- Logs are saved to `log.txt` if redirected in `live.py`.
