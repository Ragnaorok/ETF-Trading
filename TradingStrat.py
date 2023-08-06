import pandas as pd
import plotly.graph_objects as go
# import display
from IPython.display import display
from BBStrategy import BollingerBands
from MAStrat import MovingAvg

#self trading strategy class
class TradingStrategy:
    def __init__(self, fngd_graph, fngu_graph, window_size=20, strategy_choice='both', start_date=None, end_date=None):
        self.fngd_graph = fngd_graph
        self.fngu_graph = fngu_graph
        self.window_size = window_size
        self.start_date = start_date
        self.end_date = end_date
        self.strategy_choice = strategy_choice
        
        ma = MovingAvg(self.fngd_graph, self.fngu_graph, self.window_size, self.start_date, self.end_date)
        ma.calculate_moving_average()
        self.fngd_graph['FNGD Moving Average'] = ma.fngd['FNGD Moving Average']
        self.fngu_graph['FNGU Moving Average'] = ma.fngu['FNGU Moving Average']
        if self.window_size is not None and (strategy_choice == 'ma' or strategy_choice == 'both'):
            self.fngd_graph['FNGD MA Buy'] = ma.fngd['FNGD MA Buy']
            self.fngd_graph['FNGD MA Sell'] = ma.fngd['FNGD MA Sell']
            self.fngu_graph['FNGU MA Buy'] = ma.fngu['FNGU MA Buy']
            self.fngu_graph['FNGU MA Sell'] = ma.fngu['FNGU MA Sell']
        
        # self.calculate_standard_deviation()
        self.round_values()
        self.format_date()
        # self.calculate_bollinger_bands()


        if strategy_choice == 'bb' or strategy_choice == 'both':
            bb = BollingerBands(self.fngd_graph, self.fngu_graph, self.start_date, self.end_date, self.window_size)
            self.fngd_graph['FNGD BB Buy'] = bb.fngd['FNGD BB Buy']
            self.fngd_graph['FNGD BB Sell'] = bb.fngd['FNGD BB Sell']
            self.fngu_graph['FNGU BB Buy'] = bb.fngu['FNGU BB Buy']
            self.fngu_graph['FNGU BB Sell'] = bb.fngu['FNGU BB Sell']

            
        self.calculate_strategy()
        self.calculate_returns()


    def round_values(self):
        self.fngd_graph = self.fngd_graph.round(2)
        self.fngu_graph = self.fngu_graph.round(2)

    def format_date(self):
        self.fngd_graph['Date'] = self.fngd_graph['Date'].astype(str).str.slice(0, 10)
        self.fngu_graph['Date'] = self.fngu_graph['Date'].astype(str).str.slice(0, 10)






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