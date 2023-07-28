import yfinance as yf
import json
import datetime

# Get the current date
current = datetime.date.today()

# Define the tickers based on the ETFs you want to track
tickers = ["FNGU", "FNGD"]
# Define an empty dictionary to hold all data
all_data = {}

# Download the data for each ticker and store it in the dictionary
for ticker in tickers:
    data = yf.download(ticker, start='2020-01-01', end=current.isoformat())
    all_data[ticker] = json.loads(data.reset_index().to_json(date_format='iso', orient='records'))

# Convert the dictionary to JSON format

FNGU_json = json.dumps(all_data["FNGU"])
FNGD_json = json.dumps(all_data["FNGD"])
# Save the JSON data to a file
with open('FNGU.json', 'w') as file:
    file.write(FNGU_json)
with open('FNGD.json', 'w') as file:
    file.write(FNGD_json)