import unittest
import os
import datetime
import pandas as pd
import json

class TestYahooFinanceAPI(unittest.TestCase):

    def test_data_retrieval_FNGU(self):
        # Arrange
        ticker = 'FNGU'
        period1 = int(datetime.datetime(2020, 1, 1, 23, 59).timestamp())
        period2 = int(datetime.datetime.now().timestamp())
        interval = '1d'
        API_endpoint = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
        
        # Act
        df = pd.read_csv(API_endpoint)

        # Assert
        self.assertIsNotNone(df)
        self.assertIsInstance(df, pd.DataFrame)

    def test_data_retrieval_FNGD(self):
        # Arrange
        ticker = 'FNGD'
        period1 = int(datetime.datetime(2020, 1, 1, 23, 59).timestamp())
        period2 = int(datetime.datetime.now().timestamp())
        interval = '1d'
        API_endpoint = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
        
        # Act
        df = pd.read_csv(API_endpoint)

        # Assert
        self.assertIsNotNone(df)
        self.assertIsInstance(df, pd.DataFrame)

    def test_file_creation_FNGU(self):
        # Assert
        self.assertTrue(os.path.exists('FNGU.json'))

    def test_file_creation_FNGD(self):
        # Assert
        self.assertTrue(os.path.exists('FNGD.json'))
    
if __name__ == '__main__':
    unittest.main()