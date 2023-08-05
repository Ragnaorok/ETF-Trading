import pandas
class BollingerBands:
    def __init__(self, fngd, fngu, start_date, end_date, window_size):
        self.fngd, self.fngu = fngd, fngu
        self.window_size = window_size
        self.start_date = start_date
        self.end_date = end_date
        self.calculate_standard_deviation()
        self.calculate_bollinger_bands()
        self.calculate_buy_sell_signals()
    def calculate_standard_deviation(self):
        self.fngd['FNGD Standard Deviation'] = self.fngd['Adj Close'].rolling(self.window_size).std()
        self.fngu['FNGU Standard Deviation'] = self.fngu['Adj Close'].rolling(self.window_size).std()

    def calculate_bollinger_bands(self):
        self.fngd['FNGD Upper Band'] = self.fngd['FNGD Moving Average'] + (self.fngd['FNGD Standard Deviation'] * 2)
        self.fngd['FNGD Lower Band'] = self.fngd['FNGD Moving Average'] - (self.fngd['FNGD Standard Deviation'] * 2)
        self.fngu['FNGU Upper Band'] = self.fngu['FNGU Moving Average'] + (self.fngu['FNGU Standard Deviation'] * 2)
        self.fngu['FNGU Lower Band'] = self.fngu['FNGU Moving Average'] - (self.fngu['FNGU Standard Deviation'] * 2)

    def calculate_buy_sell_signals(self):
        if self.start_date is not None and self.end_date is not None:
            fngd = self.fngd.loc[(self.fngd['Date'] >= self.start_date) & (self.fngd['Date'] <= self.end_date)]
            fngu = self.fngu.loc[(self.fngu['Date'] >= self.start_date) & (self.fngu['Date'] <= self.end_date)]
        else:
            fngd = self.fngd
            fngu = self.fngu

        self.fngd['FNGD BB Buy'] = self.fngd.apply(lambda row: 1 if row['Adj Close'] < row['FNGD Lower Band'] else 0, axis=1)
        self.fngd['FNGD BB Sell'] = self.fngd.apply(lambda row: 1 if row['Adj Close'] > row['FNGD Upper Band'] else 0, axis=1)
        self.fngu['FNGU BB Buy'] = self.fngu.apply(lambda row: 1 if row['Adj Close'] < row['FNGU Lower Band'] else 0, axis=1)
        self.fngu['FNGU BB Sell'] = self.fngu.apply(lambda row: 1 if row['Adj Close'] > row['FNGU Upper Band'] else 0, axis=1)
