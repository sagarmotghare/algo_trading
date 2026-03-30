# 📈 Real-Time Market Data Collector

This project provides a Python-based service that connects to Yahoo Finance’s WebSocket API, subscribes to live ticker updates, and stores incoming messages in a local SQLite database. It is designed to run continuously, automatically reconnecting if the WebSocket session ends.

## 🚀 Features
- Connects to Yahoo Finance WebSocket for real-time market data.
- Persists ticker data in SQLite databases (`./data/{ticker}.db`).
- Schema and insert logic defined via external SQL files.
- Automatic reconnection on WebSocket errors.
- Dockerized for easy deployment.

## 📂 Project Structure

```
```
## 🛠️ Requirements
- Python 3.12+
- Dependencies listed in `requirements.txt`:
  - `yfinance`
  - `asyncio`
  - `sqlite3` (standard library)

---

## ⚙️ Environment Variables
- **`TICKER`**: The stock or index symbol to subscribe to (e.g., `^NSEI` for Nifty 50).

---

## 🗄️ Database
- Location: `./data/{ticker}.db`
- Schema: Defined in `sql/messages_create.sql`
- Insert Logic: Defined in `sql/messages_insert.sql`

### Sample WebSocket Message
```json
{
  "id": "^NSEI",
  "price": 25693.7,
  "time": "1770372083000",
  "currency": "INR",
  "exchange": "NSI",
  "quote_type": 9,
  "market_hours": 1,
  "change_percent": 0.19849016,
  "change": 50.898438,
  "price_hint": "2"
}
```

## ▶️ Running the Service
### Locally
```bash
export TICKER=^NSEI
python main.py
```


### With Docker Compose
```yaml
version: "3.9"

services:
  fetch_data:
    build:
      context: .
      dockerfile: Dockerfile.fetch_data
    command: python main.py
    environment:
      - TICKER=^NSEI
    volumes:
      - ./data:/fetch_data/data
```
Run:
```bash
docker-compose up --build
```

## 📊 Usage Notes
- Persistence: Use Docker volumes to persist market.db across container restarts.
- Scalability: Multiple tickers can be supported by running separate containers or extending the subscription list.
- Error Handling: The script automatically reconnects on WebSocket failure, ensuring continuous data collection.

## 📝 License
This project is licensed under the MIT License. See [Looks like the result wasn't safe to show. Let's switch things up and try something else!] for details.