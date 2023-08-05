import pandas as pd
import plotly.graph_objects as go
import display
from IPython.display import display

# class MovingAvg:
#     def __init__(self, fngd, fngu, window_size=20, start_date=None, end_date=None):
#         self.fngd = fngd
#         self.fngu = fngu
#         self.window_size = window_size
#         self.end_date = end_date
#         self.start_date = start_date
#         self.calculate_moving_average()
#         self.calculate_ma_signals()

#     def calculate_moving_average(self):
#         self.fngd['FNGD Moving Average'] = self.fngd['Adj Close'].rolling(self.window_size).mean()
#         self.fngu['FNGU Moving Average'] = self.fngu['Adj Close'].rolling(self.window_size).mean()

#     def calculate_ma_signals(self, start_date=None, end_date=None):

#             fngd_prev_signal = 0  
#             fngu_prev_signal = 0  
#             if start_date is not None and end_date is not None:
#                 fngd = self.fngd_graph.loc[(self.fngd_graph['Date'] >= start_date) & (self.fngd_graph['Date'] <= end_date)]
#                 fngu = self.fngu_graph.loc[(self.fngu_graph['Date'] >= start_date) & (self.fngu_graph['Date'] <= end_date)]
#             else:
#                 fngd_graph = self.fngd_graph
#                 fngu_graph = self.fngu_graph

#             for index, row in self.fngd_graph.iterrows():
#                 if row['Adj Close'] > row['FNGD Moving Average'] and fngd_prev_signal != 1:
#                     self.fngd_graph.at[index, 'FNGD MA Buy'] = 1
#                     fngd_prev_signal = 1
#                 elif row['Adj Close'] < row['FNGD Moving Average'] and fngd_prev_signal != 0:
#                     self.fngd_graph.at[index, 'FNGD MA Sell'] = 1
#                     fngd_prev_signal = 0

#             for index, row in self.fngu_graph.iterrows():
#                 if row['Adj Close'] > row['FNGU Moving Average'] and fngu_prev_signal != 1:
#                     self.fngu_graph.at[index, 'FNGU MA Buy'] = 1
#                     fngu_prev_signal = 1
#                 elif row['Adj Close'] < row['FNGU Moving Average'] and fngu_prev_signal != 0:
#                     self.fngu_graph.at[index, 'FNGU MA Sell'] = 1
#                     fngu_prev_signal = 0
# class BollingerBands:
#     def __inif__(self, start_date, end_date):
#         self.calculate_standard_deviation()
#         self.start_date = start_date
#         self.end_date = end_date
#         self.calculate_bollinger_bands()
#     def calculate_standard_deviation(self):
#         self.fngd['FNGD Moving Average'] = self.fngd['Adj Close'].rolling(self.window_size).mean()
#         self.fngu['FNGU Moving Average'] = self.fngu['Adj Close'].rolling(self.window_size).mean()

#     def calculate_bollinger_bands(self):
#         self.fngd['FNGD Upper Band'] = self.fngd['FNGD Moving Average'] + (self.fngd['FNGD Standard Deviation'] * 2)
#         self.fngd['FNGD Lower Band'] = self.fngd['FNGD Moving Average'] - (self.fngd['FNGD Standard Deviation'] * 2)
#         self.fngu['FNGU Upper Band'] = self.fngu['FNGU Moving Average'] + (self.fngu['FNGU Standard Deviation'] * 2)
#         self.fngu['FNGU Lower Band'] = self.fngu['FNGU Moving Average'] - (self.fngu['FNGU Standard Deviation'] * 2)


#self trading strategy class
class TradingStrategy:
    def __init__(self, fngd_graph, fngu_graph, window_size=20, strategy_choice='both', start_date=None, end_date=None):
        self.fngd_graph = fngd_graph
        self.fngu_graph = fngu_graph
        self.window_size = window_size
        self.start_date = start_date
        self.end_date = end_date
        self.strategy_choice = strategy_choice

        self.calculate_moving_average()
        self.calculate_standard_deviation()
        self.round_values()
        self.format_date()
        self.calculate_bollinger_bands()


        if strategy_choice == 'bb' or strategy_choice == 'both':
            self.calculate_buy_sell_signals(self.start_date, self.end_date)
        
        if self.window_size is not None and (strategy_choice == 'ma' or strategy_choice == 'both'):
            self.calculate_ma_signals(self.start_date, self.end_date)
        
        self.calculate_strategy()
        self.calculate_returns()

    def calculate_moving_average(self):
        self.fngd_graph['FNGD Moving Average'] = self.fngd_graph['Adj Close'].rolling(self.window_size).mean()
        self.fngu_graph['FNGU Moving Average'] = self.fngu_graph['Adj Close'].rolling(self.window_size).mean()

    def calculate_standard_deviation(self):
        self.fngd_graph['FNGD Standard Deviation'] = self.fngd_graph['Adj Close'].rolling(self.window_size).std()
        self.fngu_graph['FNGU Standard Deviation'] = self.fngu_graph['Adj Close'].rolling(self.window_size).std()

    def round_values(self):
        self.fngd_graph = self.fngd_graph.round(2)
        self.fngu_graph = self.fngu_graph.round(2)

    def format_date(self):
        self.fngd_graph['Date'] = self.fngd_graph['Date'].astype(str).str.slice(0, 10)
        self.fngu_graph['Date'] = self.fngu_graph['Date'].astype(str).str.slice(0, 10)

    def calculate_bollinger_bands(self):
        self.fngd_graph['FNGD Upper Band'] = self.fngd_graph['FNGD Moving Average'] + (self.fngd_graph['FNGD Standard Deviation'] * 2)
        self.fngd_graph['FNGD Lower Band'] = self.fngd_graph['FNGD Moving Average'] - (self.fngd_graph['FNGD Standard Deviation'] * 2)
        self.fngu_graph['FNGU Upper Band'] = self.fngu_graph['FNGU Moving Average'] + (self.fngu_graph['FNGU Standard Deviation'] * 2)
        self.fngu_graph['FNGU Lower Band'] = self.fngu_graph['FNGU Moving Average'] - (self.fngu_graph['FNGU Standard Deviation'] * 2)
    
    def calculate_buy_sell_signals(self, start_date=None, end_date=None):
        if start_date is not None and end_date is not None:
            fngd_graph = self.fngd_graph.loc[(self.fngd_graph['Date'] >= start_date) & (self.fngd_graph['Date'] <= end_date)]
            fngu_graph = self.fngu_graph.loc[(self.fngu_graph['Date'] >= start_date) & (self.fngu_graph['Date'] <= end_date)]
        else:
            fngd_graph = self.fngd_graph
            fngu_graph = self.fngu_graph

        self.fngd_graph['FNGD BB Buy'] = self.fngd_graph.apply(lambda row: 1 if row['Adj Close'] < row['FNGD Lower Band'] else 0, axis=1)
        self.fngd_graph['FNGD BB Sell'] = self.fngd_graph.apply(lambda row: 1 if row['Adj Close'] > row['FNGD Upper Band'] else 0, axis=1)
        self.fngu_graph['FNGU BB Buy'] = self.fngu_graph.apply(lambda row: 1 if row['Adj Close'] < row['FNGU Lower Band'] else 0, axis=1)
        self.fngu_graph['FNGU BB Sell'] = self.fngu_graph.apply(lambda row: 1 if row['Adj Close'] > row['FNGU Upper Band'] else 0, axis=1)


    def calculate_ma_signals(self, start_date=None, end_date=None):

        fngd_prev_signal = 0  
        fngu_prev_signal = 0  
        if start_date is not None and end_date is not None:
            fngd_graph = self.fngd_graph.loc[(self.fngd_graph['Date'] >= start_date) & (self.fngd_graph['Date'] <= end_date)]
            fngu_graph = self.fngu_graph.loc[(self.fngu_graph['Date'] >= start_date) & (self.fngu_graph['Date'] <= end_date)]
        else:
            fngd_graph = self.fngd_graph
            fngu_graph = self.fngu_graph

        for index, row in self.fngd_graph.iterrows():
            if row['Adj Close'] > row['FNGD Moving Average'] and fngd_prev_signal != 1:
                self.fngd_graph.at[index, 'FNGD MA Buy'] = 1
                fngd_prev_signal = 1
            elif row['Adj Close'] < row['FNGD Moving Average'] and fngd_prev_signal != 0:
                self.fngd_graph.at[index, 'FNGD MA Sell'] = 1
                fngd_prev_signal = 0

        for index, row in self.fngu_graph.iterrows():
            if row['Adj Close'] > row['FNGU Moving Average'] and fngu_prev_signal != 1:
                self.fngu_graph.at[index, 'FNGU MA Buy'] = 1
                fngu_prev_signal = 1
            elif row['Adj Close'] < row['FNGU Moving Average'] and fngu_prev_signal != 0:
                self.fngu_graph.at[index, 'FNGU MA Sell'] = 1
                fngu_prev_signal = 0




    def calculate_strategy(self):
        if 'FNGD BB Buy' in self.fngd_graph.columns and 'FNGD BB Sell' in self.fngd_graph.columns:
            self.fngd_graph['FNGD Strategy BB'] = self.fngd_graph.apply(lambda row: 1 if row['FNGD BB Buy'] == 1 else -1 if row['FNGD BB Sell'] == 1 else 0, axis=1)
        else:
            self.fngd_graph['FNGD Strategy BB'] = 0

        if 'FNGD MA Buy' in self.fngd_graph.columns and 'FNGD MA Sell' in self.fngd_graph.columns:
            self.fngd_graph['FNGD Strategy MA'] = self.fngd_graph.apply(lambda row: 1 if row['FNGD MA Buy'] == 1 else -1 if row['FNGD MA Sell'] == 1 else 0, axis=1)
        else:
            self.fngd_graph['FNGD Strategy MA'] = 0

        if 'FNGU MA Buy' in self.fngu_graph.columns and 'FNGU MA Sell' in self.fngu_graph.columns:
            self.fngu_graph['FNGU Strategy MA'] = self.fngu_graph.apply(lambda row: 1 if row['FNGU MA Buy'] == 1 else -1 if row['FNGU MA Sell'] == 1 else 0, axis=1)
        else:
            self.fngu_graph['FNGU Strategy MA'] = 0

        # Combine Bollinger Bands and Moving Average signals
        if 'FNGD Strategy BB' in self.fngd_graph.columns and 'FNGD Strategy MA' in self.fngd_graph.columns:
            self.fngd_graph['FNGD Strategy'] = self.fngd_graph['FNGD Strategy BB'] + self.fngd_graph['FNGD Strategy MA']
        else:
            self.fngd_graph['FNGD Strategy'] = 0

        if 'FNGU Strategy BB' in self.fngu_graph.columns and 'FNGU Strategy MA' in self.fngu_graph.columns:
            self.fngu_graph['FNGU Strategy'] = self.fngu_graph['FNGU Strategy BB'] + self.fngu_graph['FNGU Strategy MA']
        else:
            self.fngu_graph['FNGU Strategy'] = 0

    def get_choice(self):
        return self.strategy_choice

    # def get_signals(self):
    #     signals = pd.DataFrame({
    #         'Date': self.fngd_graph['Date'],
    #         'FNGU Price': self.fngu_graph['Adj Close'],
    #         'FNGD BB Buy': self.fngd_graph['FNGD BB Buy'],
    #         'FNGD BB Sell': self.fngd_graph['FNGD BB Sell'],
    #         'FNGU BB Buy': self.fngu_graph['FNGU BB Buy'],
    #         'FNGU BB Sell': self.fngu_graph['FNGU BB Sell'],
    #         'FNGU MA Buy': self.fngu_graph['FNGU MA Buy'],
    #         'FNGU MA Sell': self.fngu_graph['FNGU MA Sell'],
    #         'FNGD MA Buy': self.fngd_graph['FNGD MA Buy'],
    #         'FNGD MA Sell': self.fngd_graph['FNGD MA Sell'],
    #         'FNGU MA':self.fngu_graph['FNGU Moving Average'],
    #         'FNGD MA':self.fngd_graph['FNGD Moving Average'],
    #         'FNGD Price': self.fngd_graph['Adj Close']
    #     })
    #     return signals
    
    def get_signals(self):
        signals = pd.DataFrame({
            'Date': self.fngd_graph['Date'],
            'FNGU Price': self.fngu_graph['Adj Close'],
            'FNGD Price': self.fngd_graph['Adj Close'],
        })


        if 'bb' in self.strategy_choice:
            signals = signals.merge(self.fngd_graph[['Date', 'FNGD BB Buy', 'FNGD BB Sell']], on='Date', how='inner')
            signals = signals.merge(self.fngu_graph[['Date', 'FNGU BB Buy', 'FNGU BB Sell']], on='Date', how='inner')
        
        if 'ma' in self.strategy_choice:
            signals = signals.merge(self.fngd_graph[['Date', 'FNGD MA Buy', 'FNGD MA Sell']], on='Date', how='inner')
            signals = signals.merge(self.fngu_graph[['Date', 'FNGU MA Buy', 'FNGU MA Sell']], on='Date', how='inner')
        if 'both' in self.strategy_choice:
            signals = signals.merge(self.fngd_graph[['Date', 'FNGD MA Buy', 'FNGD MA Sell']], on='Date', how='inner')
            signals = signals.merge(self.fngu_graph[['Date', 'FNGU MA Buy', 'FNGU MA Sell']], on='Date', how='inner')
            signals = signals.merge(self.fngd_graph[['Date', 'FNGD BB Buy', 'FNGD BB Sell']], on='Date', how='inner')
            signals = signals.merge(self.fngu_graph[['Date', 'FNGU BB Buy', 'FNGU BB Sell']], on='Date', how='inner')
        return signals
    def calculate_returns(self):
        self.fngd_graph['FNGD Returns'] = self.fngd_graph['Adj Close'].pct_change()
        self.fngu_graph['FNGU Returns'] = self.fngu_graph['Adj Close'].pct_change()
        self.fngd_graph['FNGD Strategy Returns'] = self.fngd_graph['FNGD Returns'] * self.fngd_graph['FNGD Strategy']
        self.fngu_graph['FNGU Strategy Returns'] = self.fngu_graph['FNGU Returns'] * self.fngu_graph['FNGU Strategy']

    # def plot_graph(self):
    #     fig = go.Figure()
    #     fig.add_trace(go.Scatter(x=self.fngd_graph['Date'], y=self.fngd_graph['Adj Close'], name='FNGD'))
    #     fig.add_trace(go.Scatter(x=self.fngd_graph['Date'], y=self.fngd_graph['FNGD Moving Average'], name='FNGD Moving Average'))
    #     fig.add_trace(go.Scatter(x=self.fngd_graph['Date'], y=self.fngd_graph['FNGD Upper Band'], name='FNGD Upper Band'))
    #     fig.add_trace(go.Scatter(x=self.fngd_graph['Date'], y=self.fngd_graph['FNGD Lower Band'], name='FNGD Lower Band'))
    #     fig.add_trace(go.Scatter(x=self.fngd_graph['Date'], y=self.fngd_graph['FNGD Returns'].cumsum(), name='FNGD Cumulative Returns'))
    #     fig.add_trace(go.Scatter(x=self.fngd_graph['Date'], y=self.fngd_graph['FNGD Strategy Returns'].cumsum(), name='FNGD Strategy Cumulative Returns'))
    #     # Add buy and sell signals to the graph
    #     buy_signals = self.fngd_graph[self.fngd_graph['FNGD BB Buy'] == 1]
    #     for i, row in buy_signals.iterrows():
    #         fig.add_annotation(x=row['Date'], y=row['Adj Close'], text='Buy', font=dict(color='green'),showarrow=True, arrowhead=1, arrowcolor='green', arrowsize=2, arrowwidth=1, ax=0, ay=-30)

    #     sell_signals = self.fngd_graph[self.fngd_graph['FNGD Sell'] == 1]
    #     for i, row in sell_signals.iterrows():
    #         fig.add_annotation(x=row['Date'], y=row['Adj Close'], text='Sell',font=dict(color='red'), showarrow=True, arrowhead=1, arrowcolor='red', arrowsize=2, arrowwidth=1, ax=0, ay=30)

    #     fig.update_layout(title='FNGD Trading Strategy', xaxis_title='Date', yaxis_title='Adj Close')
    #     fig.show()

    #     fig = go.Figure()
    #     fig.add_trace(go.Scatter(x=self.fngu_graph['Date'], y=self.fngu_graph['Adj Close'], name='FNGU'))
    #     fig.add_trace(go.Scatter(x=self.fngu_graph['Date'], y=self.fngu_graph['FNGU Moving Average'], name='FNGU Moving Average'))
    #     fig.add_trace(go.Scatter(x=self.fngu_graph['Date'], y=self.fngu_graph['FNGU Upper Band'], name='FNGU Upper Band'))
    #     fig.add_trace(go.Scatter(x=self.fngu_graph['Date'], y=self.fngu_graph['FNGU Lower Band'], name='FNGU Lower Band'))
    #     fig.add_trace(go.Scatter(x=self.fngu_graph['Date'], y=self.fngu_graph['FNGU Returns'].cumsum(), name='FNGU Cumulative Returns'))
    #     fig.add_trace(go.Scatter(x=self.fngu_graph['Date'], y=self.fngu_graph['FNGU Strategy Returns'].cumsum(), name='FNGU Strategy Cumulative Returns'))
    #     # Add buy and sell signals to the graph
    #     buy_signals = self.fngu_graph[self.fngu_graph['FNGU Buy'] == 1]
    #     for i, row in buy_signals.iterrows():
    #         fig.add_annotation(x=row['Date'], y=row['Adj Close'], text='Buy', font=dict(color='green'),showarrow=True, arrowhead=1, arrowcolor='green', arrowsize=2, arrowwidth=1, ax=0, ay=-30)
        
    #     sell_signals = self.fngu_graph[self.fngu_graph['FNGU Sell'] == 1]
    #     for i, row in sell_signals.iterrows():
    #         fig.add_annotation(x=row['Date'], y=row['Adj Close'], text='Sell',font=dict(color='red'), showarrow=True, arrowhead=1, arrowcolor='red', arrowsize=2, arrowwidth=1, ax=0, ay=30)
    #     fig.update_layout(title='FNGU Trading Strategy', xaxis_title='Date', yaxis_title='Adj Close')
    #     fig.show()

def main():
    # Load data
    fngd_data = pd.read_json('FNGD.json')
    fngu_data = pd.read_json('FNGU.json')

    # Create instance of TradingStrategy class
    window_size = 20
    strategy = TradingStrategy(fngd_data, fngu_data, window_size)

    # Plot results
    strategy.plot_graph()
    #show buy and sell signals

if __name__ == '__main__':
    main()