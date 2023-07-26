import pandas as pd
from TradingStrat import TradingStrategy



def load_data(file_path):
    data = pd.read_json(file_path)
    return data

import pandas as pd

class Account:
    def __init__(self, initial_balance=100000):
        self.balance = initial_balance
        self.transactions = pd.DataFrame(columns=['Date', 'Symbol', 'Action', 'Price', 'Shares', 'Amount'])

    def buy(self, symbol, price, shares):
        amount = price * shares
        if self.balance >= amount:
            self.balance -= amount
            self._record_transaction('Buy', symbol, price, shares, amount)
            print(f"Bought {shares} shares of {symbol} at ${price:.2f} per share.")
        else:
            print("Insufficient balance to execute the transaction.")

    def sell(self, symbol, price, shares):
        amount = price * shares
        if self._has_sufficient_shares(symbol, shares):
            self.balance += amount
            self._record_transaction('Sell', symbol, price, shares, amount)
            print(f"Sold {shares} shares of {symbol} at ${price:.2f} per share.")
        else:
            print("Insufficient shares to execute the transaction.")

    def _has_sufficient_shares(self, symbol, shares):
        current_shares = self.transactions[(self.transactions['Symbol'] == symbol) & (self.transactions['Action'] == 'Buy')]['Shares'].sum()
        return current_shares >= shares

    def _record_transaction(self, action, symbol, price, shares, amount):
        date = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
        self.transactions = self.transactions.append({
            'Date': date,
            'Symbol': symbol,
            'Action': action,
            'Price': price,
            'Shares': shares,
            'Amount': amount
        }, ignore_index=True)

    def get_balance(self):
        return self.balance

    def get_transactions(self):
        return self.transactions

    def get_portfolio_value(self, price_data):
        portfolio_value = self.balance
        for _, transaction in self.transactions.iterrows():
            symbol = transaction['Symbol']
            price = price_data[symbol].iloc[-1]['Adj Close']
            shares = transaction['Shares']
            portfolio_value += shares * price
        return portfolio_value

    def calculate_returns(self, price_data):
        portfolio_value = self.get_portfolio_value(price_data)
        initial_portfolio_value = 100000
        returns = (portfolio_value - initial_portfolio_value) / initial_portfolio_value
        return returns
        
    def backtest_strategy(self, strategy, price_data):
        signals = strategy.get_signals()

        for _, signal in signals.iterrows():
            date = signal['Date']

            if signal['FNGD Buy'] == 1:
                self.buy('FNGD', price_data['FNGD'][price_data['FNGD']['Date'] == date]['Adj Close'].values[0], 100)
            elif signal['FNGD Sell'] == 1:
                self.sell('FNGD', price_data['FNGD'][price_data['FNGD']['Date'] == date]['Adj Close'].values[0], 100)

            if signal['FNGU Buy'] == 1:
                self.buy('FNGU', price_data['FNGU'][price_data['FNGU']['Date'] == date]['Adj Close'].values[0], 100)
            elif signal['FNGU Sell'] == 1:
                self.sell('FNGU', price_data['FNGU'][price_data['FNGU']['Date'] == date]['Adj Close'].values[0], 100)

        final_balance = self.get_balance()
        returns = self.calculate_returns(price_data)
        return final_balance, returns

        
