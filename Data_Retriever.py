import yfinance as yf
import json
import datetime

# Get the current date
current = datetime.date.today()

# Define the tickers based on the ETFs you want to track
tickers = ["AAPL", "TSLA", "NVDA","GOOGL","META","NFLX","TSLA","AMD","SNOW","MSFT"] # Substitute with your specific ETFs

# Define an empty dictionary to hold all data
all_data = {}

# Download the data for each ticker and store it in the dictionary
for ticker in tickers:
    data = yf.download(ticker, start='2020-01-01', end=current.isoformat())
    all_data[ticker] = json.loads(data.reset_index().to_json(date_format='iso', orient='records'))

# Convert the dictionary to JSON format
data_json = json.dumps(all_data)

# Save the JSON data to a file
with open('ETF.json', 'w') as file:
    file.write(data_json)
