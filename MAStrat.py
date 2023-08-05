import pandas
class MovingAvg:
    def __init__(self, fngd, fngu, window_size=20, start_date=None, end_date=None):
        self.fngd, self.fngu= fngd, fngu
        self.window_size = window_size
        self.end_date = end_date
        self.start_date = start_date
        self.calculate_moving_average()
        self.calculate_ma_signals()

    def calculate_moving_average(self):
        self.fngd['FNGD Moving Average'] = self.fngd['Adj Close'].rolling(self.window_size).mean()
        self.fngu['FNGU Moving Average'] = self.fngu['Adj Close'].rolling(self.window_size).mean()

 
    def calculate_ma_signals(self, start_date=None, end_date=None):

            fngd_prev_signal = 0  
            fngu_prev_signal = 0  
            if start_date is not None and end_date is not None:
                fngd = self.fngd_graph.loc[(self.fngd_graph['Date'] >= start_date) & (self.fngd_graph['Date'] <= end_date)]
                fngu = self.fngu_graph.loc[(self.fngu_graph['Date'] >= start_date) & (self.fngu_graph['Date'] <= end_date)]
            else:
                fngd = self.fngd
                fngu = self.fngu

            for index, row in self.fngd.iterrows():
                if row['Adj Close'] > row['FNGD Moving Average'] and fngd_prev_signal != 1:
                    self.fngd.at[index, 'FNGD MA Buy'] = 1
                    fngd_prev_signal = 1
                elif row['Adj Close'] < row['FNGD Moving Average'] and fngd_prev_signal != 0:
                    self.fngd.at[index, 'FNGD MA Sell'] = 1
                    fngd_prev_signal = 0

            for index, row in self.fngu.iterrows():
                if row['Adj Close'] > row['FNGU Moving Average'] and fngu_prev_signal != 1:
                    self.fngu.at[index, 'FNGU MA Buy'] = 1
                    fngu_prev_signal = 1
                elif row['Adj Close'] < row['FNGU Moving Average'] and fngu_prev_signal != 0:
                    self.fngu.at[index, 'FNGU MA Sell'] = 1
                    fngu_prev_signal = 0
