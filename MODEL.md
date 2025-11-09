## 📊 Moving Average?
A moving average (MA) is a statistical tool that calculates the average price of an asset over a specific number of days. It updates daily, dropping the oldest data point and adding the newest one, which helps smooth out short-term fluctuations and highlight the underlying trend.
### 🔟 10-Day Moving Average (Short-Term)
- **Purpose**: Tracks short-term price momentum.
- **Sensitivity**: Highly responsive to recent price changes.
- **Use Case**:
	- Traders use it to spot quick entry and exit points.
	- Often used in fast-paced strategies like swing trading or scalping.
- **Signal**: If the price crosses above the 10-day MA, it may indicate short-term bullish momentum; below it could signal bearishness.
### 5️⃣0️⃣ 50-Day Moving Average (Mid-Term)
- **Purpose**: Captures medium-term trends.
- **Sensitivity**: Less reactive than the 10-day MA, but more stable.
- **Use Case**:
	- Widely used by both traders and investors.
	- Helps identify support/resistance levels and overall market direction.
- **Signal**:
	- Price above the 50-day MA suggests a bullish trend.
	- Price below it may indicate a bearish trend.
	- Crossovers (e.g., 10-day crossing above the 50-day) are often used as buy/sell signals.
### 📈 Common Strategy: Moving Average Crossover
One popular method is the crossover strategy:
- **Bullish crossover**: When the 10-day MA crosses above the 50-day MA → potential buy signal.
- **Bearish crossover**: When the 10-day MA crosses below the 50-day MA → potential sell signal.

This helps traders spot trend reversals or confirmations.
### 🧠 Why Use Both?
Using both averages together gives a layered view:
- The 10-day MA shows short-term momentum.
- The 50-day MA reveals the broader trend.
- Together, they help filter out noise and improve timing for trades.

## Volatility (rolling standard deviation)
**Volatility (rolling standard deviation)** is a key metric in time series analysis and trading that measures how much a value (like a stock price) fluctuates over a specific rolling window. It helps quantify **risk** or **uncertainty** in price movements.
### 📐 Formula
For a rolling window of size n, the rolling standard deviation at time t is:
```Latex
```
$$
 \sigma_t = \sqrt{\frac{1}{n-1} \sum_{i=0}^{n-1} (x_{t-i} - \bar{x})^2} 
 $$
```
```
Where:
-   $x_{t-i}$ are the values in the window
-   $\bar{x}$ is the mean of those values
-   $\sigma_t$ is the standard deviation at time t
### 📊 Why It Matters
-   **High volatility** → More risk, more potential reward.
-   **Low volatility** → Stable prices, less trading opportunity.
-   **Used in**:
	-   Risk management
	-   Position sizing
	-   Volatility breakout strategies
	-   Bollinger Bands (which use rolling std dev)

## RSI (Relative Strength Index)
**RSI (Relative Strength Index)** is a momentum oscillator that measures the speed and magnitude of recent price changes to identify overbought or oversold conditions. It ranges from 0 to 100 and is widely used in technical analysis.

### 📈 What RSI Tells You
-   **Overbought**: RSI > 70 → Asset may be overvalued and due for a pullback.
-   **Oversold**: RSI < 30 → Asset may be undervalued and due for a rebound.
-   **Neutral zone**: RSI between 30 and 70 → No strong momentum signal.

RSI helps traders spot potential reversals or confirm trends based on momentum shifts.

### 🧮 RSI Formula

The RSI is calculated using the following steps:

1.  **Average Gain and Loss** over a period (typically 14 days):
```Latex
```
$$
\text{RS} = \frac{\text{Average Gain}}{\text{Average Loss}}
$$
```
```
3.  **RSI Calculation**:
```Latex
```
$$
\text{RSI} = 100 - \left( \frac{100}{1 + \text{RS}} \right)
$$
```
```
This formula smooths price changes and converts them into a bounded oscillator.

### 🔍 How Traders Use RSI

-   **Trend confirmation**: RSI staying above 50 in an uptrend or below 50 in a downtrend.
-   **Divergence**: Price makes a new high/low but RSI doesn’t → possible reversal.
-   **Swing trading**: Buy when RSI crosses above 30, sell when it drops below 70.

### 🧠 Pro Tip

RSI works best when combined with other indicators like moving averages or Bollinger Bands. You can also customize the window (e.g., RSI-10 or RSI-20) depending on your strategy’s time horizon.

Want help integrating RSI into your trading logic or visualizing it alongside volatility and moving averages? I can help you build that out.