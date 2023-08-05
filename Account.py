import pandas as pd
from TradingStrat import TradingStrategy

def load_data(file_path):
    data = pd.read_json(file_path)
    return data

import pandas as pd

class Account:
    def __init__(self, initial_balance=100000):
        self.initialBalance = initial_balance
        self.balance = initial_balance
        self.transactions = pd.DataFrame(columns=['Date', 'Symbol', 'Action', 'Price', 'Shares', 'Amount'])

    def buy(self, symbol, price, shares, date):
        amount = price * shares
        if self.balance >= amount:
            self.balance -= amount
            self._record_transaction('Buy', symbol, price, shares, amount, date)

            print(f"{date}: Bought {shares} shares of {symbol} at ${price:.2f} per share.")
        else:
            print("Insufficient balance to execute the transaction.")

    def sell(self, symbol, price, shares, date):
        amount = price * shares
        if self.balance >= amount and self._has_sufficient_shares(symbol, shares):
            self.balance += amount
            self._record_transaction('Sell', symbol, price, shares, amount, date)

            print(f"{date}: Sold {shares} shares of {symbol} at ${price:.2f} per share.")
        else:
            print("Insufficient shares to execute the transaction.", self.balance)

    def _has_sufficient_shares(self, symbol, shares):
        current_shares = self.transactions[(self.transactions['Symbol'] == symbol) & (self.transactions['Action'] == 'Buy')]['Shares'].sum()
        return current_shares >= shares

    def _record_transaction(self, action, symbol, price, shares, amount, date):
        
        self.transactions = self.transactions._append({
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
        final_balance = self.get_balance()
        cash_balance = self.initialBalance
        print("cash_balance:", cash_balance)
        returns = ((final_balance - cash_balance) / (cash_balance))
        return returns
    

    def backtest_strategy(self, strategy, price_data, start_date, end_date):
        choice = strategy.get_choice()
        print('choice:', choice)
        signals = strategy.get_signals()
        if not isinstance(start_date, pd.Timestamp):
            start_date = pd.Timestamp(start_date)
        if not isinstance(end_date, pd.Timestamp):
            end_date = pd.Timestamp(end_date)
        if choice =='bb':
            signals.to_csv('BBsignals.csv', index=False)
        elif choice =='MA':
            signals.to_csv('MAsignals.csv', index=False)
        for _, signal in signals.iterrows():
            date = signal['Date']

            # Check if the signal date is after the start date and before the end date
            if start_date <= pd.Timestamp(date) <= end_date:

                if choice =='bb' or choice =='both':
                    
                    if signal['FNGD BB Buy'] == 1:
                        print("\nFNGD BB Buy")
                        self.buy('FNGD', price_data['FNGD'][price_data['FNGD']['Date'] == date]['Adj Close'].values[0], 100, date)

                    elif signal['FNGD BB Sell'] == 1:
                        print("\nFNGD BB Sell")
                        self.sell('FNGD', price_data['FNGD'][price_data['FNGD']['Date'] == date]['Adj Close'].values[0], 100, date)
                    if signal['FNGU BB Sell'] == 1:
                        print("\nFNGU BB Sell")
                        self.sell('FNGU', price_data['FNGU'][price_data['FNGU']['Date'] == date]['Adj Close'].values[0], 100, date)
                    elif signal['FNGU BB Buy'] == 1:
                        print("\nFNGU BB Buy")
                        self.buy('FNGU', price_data['FNGU'][price_data['FNGU']['Date'] == date]['Adj Close'].values[0], 100, date)
                
                if choice =='ma' or choice =='both':
                    if signal['FNGD MA Buy'] == 1:
                        print("\nFNGD MA Buy")
                        print(f"FNGD Price {signal['FNGD Price']}")
                        self.buy('FNGD', price_data['FNGD'][price_data['FNGD']['Date'] == date]['Adj Close'].values[0], 100, date)

                    elif signal['FNGD MA Sell'] == 1:
                        print("\nFNGD MA Sell")
                        print(f"FNGD Price {signal['FNGD Price']}")
                        self.sell('FNGD', price_data['FNGD'][price_data['FNGD']['Date'] == date]['Adj Close'].values[0], 100, date)

                    if signal['FNGU MA Buy'] == 1:
                        print("\nFNGU MA Buy")
                        print(f"FNGU Price {signal['FNGU Price']}")
                        self.buy('FNGU', price_data['FNGU'][price_data['FNGU']['Date'] == date]['Adj Close'].values[0], 100, date)

                    elif signal['FNGU MA Sell'] == 1:
                        print("\nFNGU MA Sell")
                        print(f"FNGU Price {signal['FNGU Price']}")
                        self.sell('FNGU', price_data['FNGU'][price_data['FNGU']['Date'] == date]['Adj Close'].values[0], 100, date)

                
        
        
        print(self.get_portfolio_value(price_data))
        final_balance = self.get_balance()
        returns = self.calculate_returns(price_data)
        return final_balance, returns