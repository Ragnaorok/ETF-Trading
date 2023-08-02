import time
import datetime
import pandas as pd
import json

def retrieve_data(tickers):
    all_data = {}
    for ticker in tickers:
        period1 = int(time.mktime(datetime.datetime(2020, 1, 1, 23, 59).timetuple()))
        period2 = int(time.mktime(datetime.datetime.now().timetuple()))
        interval = '1d' # 1d, 1m
        API_endpoint = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
        df = pd.read_csv(API_endpoint)
        all_data[ticker] = json.loads(df.to_json(date_format='iso', orient='records'))
    
    # Save the JSON data to a file
    with open('FNGU.json', 'w') as file:
        file.write(json.dumps(all_data["FNGU"]))
    with open('FNGD.json', 'w') as file:
        file.write(json.dumps(all_data["FNGD"]))

    return all_data

def main():
    try:
        # Define the tickers for which to retrieve data
        tickers = ['FNGU', 'FNGD']

        # Call the retrieve_data function to get the data
        all_data = retrieve_data(tickers)

        # Optional: Print the retrieved data
        print("Retrieved data: ", all_data)

    except Exception as e:
        print("Error retrieving data:", e)

if __name__ == "__main__":
    main()
