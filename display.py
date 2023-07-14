import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot

# Read the CSV file into a pandas DataFrame
fngd = pd.read_csv('FNGD.csv')

# Select specific columns
fngd_columns = ['Adj Close', 'Date']
toGraph = fngd[fngd_columns]
toGraph.head()
# Plot the selected columns




# Save the plot as HTML
# Create the plot using Plotly
fig = go.Figure(data=go.Scatter(x=toGraph['Date'], y=toGraph['Adj Close']))

# Save the plot as HTML
fig.write_html('plot.html')
import json
import pandas as pd
import matplotlib.pyplot as plt

# Load the JSON data
with open('ETF.json', 'r') as f:
    data = json.load(f)

# Extract the relevant data
tickers = ["FNGU", "FNGD"]
colors = ['red', 'blue']

# Create a DataFrame from the stock data
df = pd.DataFrame()
for ticker in tickers:
    stock_df = pd.DataFrame(data[ticker])
    stock_df['Ticker'] = ticker
    df = pd.concat([df, stock_df])

# Convert Date column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Select specific columns
df_columns = ['Adj Close', 'Date']

for ticker, color in zip(tickers, colors):
    toGraph = df[df['Ticker'] == ticker][df_columns]
    plt.plot(toGraph['Date'], toGraph['Adj Close'], label=ticker, color=color)

# Add labels and title
plt.xlabel('Date')
plt.ylabel('Adj Close')
plt.title('ETF FNGD Trends')
plt.legend()

# Show the plot
plt.show()