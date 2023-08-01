import pandas as pd
import plotly.graph_objects as go
import display
from IPython.display import display
from plotly.subplots import make_subplots


#self trading strategy class
class TradingStrategy:
    def __init__(self, fngd_graph, fngu_graph, window_size):
        self.fngd_graph = fngd_graph
        self.fngu_graph = fngu_graph
        self.window_size = window_size
        self.calculate_moving_average()
        self.calculate_standard_deviation()
        self.round_values()
        self.format_date()
        self.calculate_bollinger_bands()
        self.calculate_buy_sell_signals()
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

    def calculate_buy_sell_signals(self):
        self.fngd_graph['FNGD Buy'] = self.fngd_graph.apply(lambda row: 1 if row['Adj Close'] < row['FNGD Lower Band'] else 0, axis=1)
        self.fngd_graph['FNGD Sell'] = self.fngd_graph.apply(lambda row: 1 if row['Adj Close'] > row['FNGD Upper Band'] else 0, axis=1)
        self.fngu_graph['FNGU Buy'] = self.fngu_graph.apply(lambda row: 1 if row['Adj Close'] < row['FNGU Lower Band'] else 0, axis=1)
        self.fngu_graph['FNGU Sell'] = self.fngu_graph.apply(lambda row: 1 if row['Adj Close'] > row['FNGU Upper Band'] else 0, axis=1)

    def calculate_strategy(self):
        self.fngd_graph['FNGD Strategy'] = self.fngd_graph.apply(lambda row: 1 if row['FNGD Buy'] == 1 else -1 if row['FNGD Sell'] == 1 else 0, axis=1)
        self.fngu_graph['FNGU Strategy'] = self.fngu_graph.apply(lambda row: 1 if row['FNGU Buy'] == 1 else -1 if row['FNGU Sell'] == 1 else 0, axis=1)
        
    def get_signals(self):
        signals = pd.DataFrame({
            'Date': self.fngd_graph['Date'],
            'FNGD Buy': self.fngd_graph['FNGD Buy'],
            'FNGD Sell': self.fngd_graph['FNGD Sell'],
            'FNGU Buy': self.fngu_graph['FNGU Buy'],
            'FNGU Sell': self.fngu_graph['FNGU Sell']
        })
        return signals

    def calculate_returns(self):
        self.fngd_graph['FNGD Returns'] = self.fngd_graph['Adj Close'].pct_change()
        self.fngu_graph['FNGU Returns'] = self.fngu_graph['Adj Close'].pct_change()
        self.fngd_graph['FNGD Strategy Returns'] = self.fngd_graph['FNGD Returns'] * self.fngd_graph['FNGD Strategy']
        self.fngu_graph['FNGU Strategy Returns'] = self.fngu_graph['FNGU Returns'] * self.fngu_graph['FNGU Strategy']

    def plot_graph(self):
        fig = make_subplots(rows=2, cols=2, subplot_titles=("FNGD Bollinger Bands", "FNGD Moving Average", "FNGU Bollinger Bands", "FNGU Moving Average"))
        # Plot FNGD Bollinger Bands
        fig.add_trace(go.Scatter(x=self.fngd_graph['Date'], y=self.fngd_graph['Adj Close'], name='FNGD'), row=1, col=1)
        fig.add_trace(go.Scatter(x=self.fngd_graph['Date'], y=self.fngd_graph['FNGD Moving Average'], name='FNGD Moving Average'), row=1, col=1)
        fig.add_trace(go.Scatter(x=self.fngd_graph['Date'], y=self.fngd_graph['FNGD Upper Band'], name='FNGD Upper Band'), row=1, col=1)
        fig.add_trace(go.Scatter(x=self.fngd_graph['Date'], y=self.fngd_graph['FNGD Lower Band'], name='FNGD Lower Band'), row=1, col=1)

        # Plot FNGD Moving Average
        fig.add_trace(go.Scatter(x=self.fngd_graph['Date'], y=self.fngd_graph['Adj Close'], name='FNGD'), row=1, col=2)
        fig.add_trace(go.Scatter(x=self.fngd_graph['Date'], y=self.fngd_graph['FNGD Moving Average'], name='FNGD Moving Average'), row=1, col=2)
        # Add buy and sell signals to the graph
        buy_signals = self.fngd_graph[self.fngd_graph['FNGD Buy'] == 1]
        for i, row in buy_signals.iterrows():
            fig.add_annotation(x=row['Date'], y=row['Adj Close'], text='Buy', font=dict(color='green'),showarrow=True, arrowhead=1, arrowcolor='green', arrowsize=2, arrowwidth=1, ax=0, ay=-30)

        sell_signals = self.fngd_graph[self.fngd_graph['FNGD Sell'] == 1]
        for i, row in sell_signals.iterrows():
            fig.add_annotation(x=row['Date'], y=row['Adj Close'], text='Sell',font=dict(color='red'), showarrow=True, arrowhead=1, arrowcolor='red', arrowsize=2, arrowwidth=1, ax=0, ay=30)

        # Plot FNGU Bollinger Bands
        fig.add_trace(go.Scatter(x=self.fngu_graph['Date'], y=self.fngu_graph['Adj Close'], name='FNGU'), row=2, col=1)
        fig.add_trace(go.Scatter(x=self.fngu_graph['Date'], y=self.fngu_graph['FNGU Moving Average'], name='FNGU Moving Average'), row=2, col=1)
        fig.add_trace(go.Scatter(x=self.fngu_graph['Date'], y=self.fngu_graph['FNGU Upper Band'], name='FNGU Upper Band'), row=2, col=1)
        fig.add_trace(go.Scatter(x=self.fngu_graph['Date'], y=self.fngu_graph['FNGU Lower Band'], name='FNGU Lower Band'), row=2, col=1)

        # Plot FNGU Moving Average
        fig.add_trace(go.Scatter(x=self.fngu_graph['Date'], y=self.fngu_graph['Adj Close'], name='FNGU'), row=2, col=2)
        fig.add_trace(go.Scatter(x=self.fngu_graph['Date'], y=self.fngu_graph['FNGU Moving Average'], name='FNGU Moving Average'), row=2, col=2)
        # Add buy and sell signals to the graph
        buy_signals = self.fngu_graph[self.fngu_graph['FNGU Buy'] == 1]
        for i, row in buy_signals.iterrows():
            fig.add_annotation(x=row['Date'], y=row['Adj Close'], text='Buy', font=dict(color='green'),showarrow=True, arrowhead=1, arrowcolor='green', arrowsize=2, arrowwidth=1, ax=0, ay=-30)

        sell_signals = self.fngu_graph[self.fngu_graph['FNGU Sell'] == 1]
        for i, row in sell_signals.iterrows():
            fig.add_annotation(x=row['Date'], y=row['Adj Close'], text='Sell',font=dict(color='red'), showarrow=True, arrowhead=1, arrowcolor='red', arrowsize=2, arrowwidth=1, ax=0, ay=30)

        fig.update_layout(title_text="Trading Strategies")
        fig.show()


def main():
    # Load data
    fngd_data = pd.read_json('FNGD.json')
    fngu_data = pd.read_json('FNGU.json')

    # Create instance of TradingStrategy class
    window_size = 20
    strategy = TradingStrategy(fngd_data, fngu_data, window_size)

    # Plot results
    display(strategy.fngd_graph)
    display(strategy.fngu_graph)
    strategy.plot_graph()
    
if __name__ == '__main__':
    main()

