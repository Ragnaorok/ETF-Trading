import json
import pandas as pd
from matplotlib import pyplot as plt

# Load the JSON data
with open('ETF.json', 'r') as f:
    data = json.load(f)

# Extract the relevant data
tickers = ["AAPL", "TSLA", "NVDA", "GOOGL", "META", "NFLX", "AMD", "SNOW", "MSFT"]  
colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'gray', 'olive', 'cyan']

# Create a DataFrame from the stock data
df = pd.concat([pd.DataFrame(data[ticker]).assign(Ticker=ticker) for ticker in tickers])

# Convert Date column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Select specific columns
df_columns = ['Adj Close', 'Date']

for ticker, color in zip(tickers, colors):
    toGraph = df.loc[df['Ticker'] == ticker, df_columns]
    plt.plot(toGraph['Date'], toGraph['Adj Close'], label=ticker, color=color)

# Add labels and title
plt.xlabel('Date')
plt.ylabel('Adj Close')
plt.title('ETF FNGU Trends')
plt.legend()

# Show the plot
plt.show()
