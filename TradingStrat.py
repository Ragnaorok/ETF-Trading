import pandas as pd
import plotly.graph_objects as go
import display
from IPython.display import display


#self trading strategy class
class TradingStrategy:
    def __init__(self, fngd_graph, fngu_graph, window_size):
        self.fngd_graph = fngd_graph
        self.fngu_graph = fngu_graph
        self.window_size = window_size
        self.calculate_moving_average()
        self.calculate_standard_deviation()
        # self.round_values()
        # self.format_date()
        self.calculate_bollinger_bands()
        self.calculate_buy_sell_signals()
        self.calculate_ma_signals()
        self.calculate_strategy()
        self.calculate_returns()
        

    # function to calculate moving average of FNGD and FNGU
    def calculate_moving_average(self):
        self.fngd_graph['FNGD Moving Average'] = self.fngd_graph['Adj Close'].rolling(self.window_size).mean()
        self.fngu_graph['FNGU Moving Average'] = self.fngu_graph['Adj Close'].rolling(self.window_size).mean()
    
    # function to calculate standard deviation of FNGD and FNGU
    def calculate_standard_deviation(self):
        self.fngd_graph['FNGD Standard Deviation'] = self.fngd_graph['Adj Close'].rolling(self.window_size).std()
        self.fngu_graph['FNGU Standard Deviation'] = self.fngu_graph['Adj Close'].rolling(self.window_size).std()
   
   # function to round values
    def round_values(self):
        self.fngd_graph = self.fngd_graph.round(2)
        self.fngu_graph = self.fngu_graph.round(2)

   # function to format date
    def format_date(self):
        self.fngd_graph['Date'] = self.fngd_graph['Date'].astype(str).str.slice(0, 10)
        self.fngu_graph['Date'] = self.fngu_graph['Date'].astype(str).str.slice(0, 10)


   # function to calculate bollinger bands
    def calculate_bollinger_bands(self):
        self.fngd_graph['FNGD Upper Band'] = self.fngd_graph['FNGD Moving Average'] + (self.fngd_graph['FNGD Standard Deviation'] * 2)
        self.fngd_graph['FNGD Lower Band'] = self.fngd_graph['FNGD Moving Average'] - (self.fngd_graph['FNGD Standard Deviation'] * 2)
        self.fngu_graph['FNGU Upper Band'] = self.fngu_graph['FNGU Moving Average'] + (self.fngu_graph['FNGU Standard Deviation'] * 2)
        self.fngu_graph['FNGU Lower Band'] = self.fngu_graph['FNGU Moving Average'] - (self.fngu_graph['FNGU Standard Deviation'] * 2)

   # function to calculate buy and sell signals
    def calculate_buy_sell_signals(self):
        self.fngd_graph['FNGD BB Buy'] = self.fngd_graph.apply(lambda row: 1 if row['Adj Close'] < row['FNGD Lower Band'] else 0, axis=1)
        self.fngd_graph['FNGD BB Sell'] = self.fngd_graph.apply(lambda row: 1 if row['Adj Close'] > row['FNGD Upper Band'] else 0, axis=1)
        self.fngu_graph['FNGU BB Buy'] = self.fngu_graph.apply(lambda row: 1 if row['Adj Close'] < row['FNGU Lower Band'] else 0, axis=1)
        self.fngu_graph['FNGU BB Sell'] = self.fngu_graph.apply(lambda row: 1 if row['Adj Close'] > row['FNGU Upper Band'] else 0, axis=1)
   
   
   # function to calculate moving average signals
    def calculate_ma_signals(self):
        # Calculate Moving Average signals for FNGD
        self.fngd_graph['FNGD MA Buy'] = self.fngd_graph.apply(
            lambda row: 1 if row['Adj Close'] > row['FNGD Moving Average'] else 0, axis=1)
        self.fngd_graph['FNGD MA Sell'] = self.fngd_graph.apply(
            lambda row: 1 if row['Adj Close'] < row['FNGD Moving Average'] else 0, axis=1)

        # Calculate Moving Average signals for FNGU
        self.fngu_graph['FNGU MA Buy'] = self.fngu_graph.apply(
            lambda row: 1 if row['Adj Close'] > row['FNGU Moving Average'] else 0, axis=1)
        self.fngu_graph['FNGU MA Sell'] = self.fngu_graph.apply(
            lambda row: 1 if row['Adj Close'] < row['FNGU Moving Average'] else 0, axis=1)

        # Apply the signals on specific dates
        self.fngd_graph['FNGD MA Buy'] = self.fngd_graph['FNGD MA Buy'] * self.fngd_graph['FNGD MA Buy'].shift(-1)
        self.fngd_graph['FNGD MA Sell'] = self.fngd_graph['FNGD MA Sell'] * self.fngd_graph['FNGD MA Sell'].shift(-1)
        # Apply the signals on specific dates
        self.fngu_graph['FNGU MA Buy'] = self.fngu_graph['FNGU MA Buy'] * self.fngu_graph['FNGU MA Buy'].shift(-1)
        self.fngu_graph['FNGU MA Sell'] = self.fngu_graph['FNGU MA Sell'] * self.fngu_graph['FNGU MA Sell'].shift(-1)
   # function to calculate strategy
    def calculate_strategy(self):
        self.fngd_graph['FNGD Strategy BB'] = self.fngd_graph.apply(lambda row:  1 if row['FNGD BB Buy'] == 1 else -1 if row['FNGD BB Sell'] == 1 else 0, axis=1)
        self.fngu_graph['FNGU Strategy BB'] = self.fngu_graph.apply(lambda row: 1 if row['FNGU BB Buy'] == 1 else -1 if row['FNGU BB Sell'] == 1 else 0, axis=1)
        self.fngd_graph['FNGD Strategy MA'] = self.fngd_graph.apply(lambda row: 1 if row['FNGD MA Buy'] == 1 else -1 if row['FNGD MA Sell'] == 1 else 0, axis=1)
        self.fngu_graph['FNGU Strategy MA'] = self.fngu_graph.apply(lambda row: 1 if row['FNGU MA Buy'] == 1 else -1 if row['FNGU MA Sell'] == 1 else 0, axis=1)

        # Combine Bollinger Bands and Moving Average signals
        self.fngd_graph['FNGD Strategy'] = self.fngd_graph['FNGD Strategy BB'] + self.fngd_graph['FNGD Strategy MA']
        self.fngu_graph['FNGU Strategy'] = self.fngu_graph['FNGU Strategy BB'] + self.fngu_graph['FNGU Strategy MA']
    
    # getting the signals for the strategy BB and MA , buy and sell
    def get_signals(self):
        signals = pd.DataFrame({
            'Date': self.fngd_graph['Date'],
            'FNGU Price': self.fngu_graph['Adj Close'],
            'FNGD BB Buy': self.fngd_graph['FNGD BB Buy'],
            'FNGD BB Sell': self.fngd_graph['FNGD BB Sell'],
            'FNGU BB Buy': self.fngu_graph['FNGU BB Buy'],
            'FNGU BB Sell': self.fngu_graph['FNGU BB Sell'],
            'FNGU MA Buy': self.fngu_graph['FNGU MA Buy'],
            'FNGU MA Sell': self.fngu_graph['FNGU MA Sell'],
            'FNGD MA Buy': self.fngd_graph['FNGD MA Buy'],
            'FNGD MA Sell': self.fngd_graph['FNGD MA Sell'],
            'FNGU MA':self.fngu_graph['FNGU Moving Average']

        })
        return signals
   
   # function to calculate returns, used in backtest.py
    def calculate_returns(self):
        self.fngd_graph['FNGD Returns'] = self.fngd_graph['Adj Close'].pct_change()
        self.fngu_graph['FNGU Returns'] = self.fngu_graph['Adj Close'].pct_change()
        self.fngd_graph['FNGD Strategy Returns'] = self.fngd_graph['FNGD Returns'] * self.fngd_graph['FNGD Strategy']
        self.fngu_graph['FNGU Strategy Returns'] = self.fngu_graph['FNGU Returns'] * self.fngu_graph['FNGU Strategy']
   

   # function to plot graph of FNGD and FNGU
    def plot_graph(self):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self.fngd_graph['Date'], y=self.fngd_graph['Adj Close'], name='FNGD'))
        fig.add_trace(go.Scatter(x=self.fngd_graph['Date'], y=self.fngd_graph['FNGD Moving Average'], name='FNGD Moving Average'))
        fig.add_trace(go.Scatter(x=self.fngd_graph['Date'], y=self.fngd_graph['FNGD Upper Band'], name='FNGD Upper Band'))
        fig.add_trace(go.Scatter(x=self.fngd_graph['Date'], y=self.fngd_graph['FNGD Lower Band'], name='FNGD Lower Band'))
        fig.add_trace(go.Scatter(x=self.fngd_graph['Date'], y=self.fngd_graph['FNGD Returns'].cumsum(), name='FNGD Cumulative Returns'))
        fig.add_trace(go.Scatter(x=self.fngd_graph['Date'], y=self.fngd_graph['FNGD Strategy Returns'].cumsum(), name='FNGD Strategy Cumulative Returns'))
        # Add buy and sell signals to the graph
        # buy_signals = self.fngd_graph[self.fngd_graph['FNGD MA Buy'] == 1]
        # for i, row in buy_signals.iterrows():
        #     fig.add_annotation(x=row['Date'], y=row['Adj Close'], text='Buy', font=dict(color='green'),showarrow=True, arrowhead=1, arrowcolor='green', arrowsize=2, arrowwidth=1, ax=0, ay=-30)

        # sell_signals = self.fngd_graph[self.fngd_graph['FNGD MA Sell'] == 1]
        # for i, row in sell_signals.iterrows():
        #     fig.add_annotation(x=row['Date'], y=row['Adj Close'], text='Sell',font=dict(color='red'), showarrow=True, arrowhead=1, arrowcolor='red', arrowsize=2, arrowwidth=1, ax=0, ay=30)

        fig.update_layout(title='FNGD Trading Strategy', xaxis_title='Date', yaxis_title='Adj Close')
        fig.show()

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self.fngu_graph['Date'], y=self.fngu_graph['Adj Close'], name='FNGU'))
        fig.add_trace(go.Scatter(x=self.fngu_graph['Date'], y=self.fngu_graph['FNGU Moving Average'], name='FNGU Moving Average'))
        fig.add_trace(go.Scatter(x=self.fngu_graph['Date'], y=self.fngu_graph['FNGU Upper Band'], name='FNGU Upper Band'))
        fig.add_trace(go.Scatter(x=self.fngu_graph['Date'], y=self.fngu_graph['FNGU Lower Band'], name='FNGU Lower Band'))
        fig.add_trace(go.Scatter(x=self.fngu_graph['Date'], y=self.fngu_graph['FNGU Returns'].cumsum(), name='FNGU Cumulative Returns'))
        fig.add_trace(go.Scatter(x=self.fngu_graph['Date'], y=self.fngu_graph['FNGU Strategy Returns'].cumsum(), name='FNGU Strategy Cumulative Returns'))
        # Add buy and sell signals to the graph
        # buy_signals = self.fngu_graph[self.fngu_graph['FNGU MA Buy'] == 1]
        # for i, row in buy_signals.iterrows():
        #     fig.add_annotation(x=row['Date'], y=row['Adj Close'], text='Buy', font=dict(color='green'),showarrow=True, arrowhead=1, arrowcolor='green', arrowsize=2, arrowwidth=1, ax=0, ay=-30)
        
        # sell_signals = self.fngu_graph[self.fngu_graph['FNGU MA Sell'] == 1]
        # for i, row in sell_signals.iterrows():
        #     fig.add_annotation(x=row['Date'], y=row['Adj Close'], text='Sell',font=dict(color='red'), showarrow=True, arrowhead=1, arrowcolor='red', arrowsize=2, arrowwidth=1, ax=0, ay=30)
        # fig.update_layout(title='FNGU Trading Strategy', xaxis_title='Date', yaxis_title='Adj Close')
        fig.show()

#main function to be called
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
    
  
    

#main function call

if __name__ == '__main__':
    main()