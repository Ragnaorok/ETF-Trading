import time
import datetime
import pandas as pd
import json

class DataRetrieverAdapter:
    def retrieve_data(self):
        tickers = ['FNGU', 'FNGD']
        all_data = {}

        for ticker in tickers:
            period1 = int(time.mktime(datetime.datetime(2020, 1, 1, 23, 59).timetuple()))
            period2 = int(time.mktime(datetime.datetime.now().timetuple()))  # subtract one day to get yesterday's date
            interval = '1d' # 1d, 1m
            API_endpoint = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
            df = pd.read_csv(API_endpoint)
            all_data[ticker] = json.loads(df.to_json(date_format='iso', orient='records'))

        # Convert the dictionary to JSON format
        FNGU_json = json.dumps(all_data["FNGU"])
        FNGD_json = json.dumps(all_data["FNGD"])

        # Save the JSON data to a file
        with open('FNGU.json', 'w') as file:
            file.write(FNGU_json)
        with open('FNGD.json', 'w') as file:
            file.write(FNGD_json)


DataRetrieverAdapter().retrieve_data()