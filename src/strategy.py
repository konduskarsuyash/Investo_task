import matplotlib.pyplot as plt
import pandas as pd
import mysql.connector

# Load Data
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="suyash@123",
    database="investo_internship"
)
query = "SELECT * FROM stock_data WHERE instrument='HINDALCO'"
data = pd.read_sql(query, conn)
conn.close()

# Calculate Moving Averages
data['SMA_10'] = data['close'].rolling(window=10).mean()
data['SMA_30'] = data['close'].rolling(window=30).mean()

# Generate Buy/Sell Signals
data['Signal'] = 0
data.loc[data['SMA_10'] > data['SMA_30'], 'Signal'] = 1  # Buy
data.loc[data['SMA_10'] < data['SMA_30'], 'Signal'] = -1  # Sell

# Plot the strategy
plt.figure(figsize=(14, 7))
plt.plot(data['datetime'], data['close'], label='Close Price', color='blue')
plt.plot(data['datetime'], data['SMA_10'], label='10-Day SMA', color='green')
plt.plot(data['datetime'], data['SMA_30'], label='30-Day SMA', color='red')
plt.legend()
plt.show()

# Backtest Performance
data['Daily_Return'] = data['close'].pct_change()
data['Strategy_Return'] = data['Signal'].shift(1) * data['Daily_Return']
cumulative_strategy_return = (1 + data['Strategy_Return']).cumprod()
cumulative_baseline_return = (1 + data['Daily_Return']).cumprod()

# Plot performance
plt.figure(figsize=(14, 7))
plt.plot(data['datetime'], cumulative_strategy_return, label='Strategy Return', color='green')
plt.plot(data['datetime'], cumulative_baseline_return, label='Baseline (Buy-and-Hold)', color='blue')
plt.legend()
plt.show()
