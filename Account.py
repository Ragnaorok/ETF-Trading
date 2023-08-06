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
            print(f"{date}: Insufficient balance to execute the buying transaction.")

    def sell(self, symbol, price, shares, date):
        amount = price * shares

        if self.balance >= amount and self._has_sufficient_shares(symbol, shares):
            self.balance += amount
            self._record_transaction('Sell', symbol, price, shares, amount, date)

            print(f"{date}: Sold {shares} shares of {symbol} at ${price:.2f} per share.")
        else:
            print(f"{date}: Insufficient shares to execute the selling transaction.")

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
    def get_remaining_shares(self):
        shares_bought = self.transactions.loc[self.transactions['Action'] == 'Buy'].groupby('Symbol')['Shares'].sum()
        shares_sold = self.transactions.loc[self.transactions['Action'] == 'Sell'].groupby('Symbol')['Shares'].sum()
        remaining_shares = shares_bought.sub(shares_sold, fill_value=0)

        remaining_shares_dict = remaining_shares.to_dict()

        return remaining_shares_dict

    # def get_portfolio_value(self, price_data, start_date, end_date):
    #     portfolio_value = self.balance
    #     for _, transaction in self.transactions.iterrows():
    #         date = transaction['Date']

    #         if start_date <= pd.Timestamp(date) <= end_date:
    #             symbol = transaction['Symbol']
    #             try:
    #                 price = price_data[symbol].loc[date]['Adj Close']
    #             except KeyError:
    #                 print(f"Price data not available for symbol: {symbol} on date: {date}")
    #                 continue  # Skip to the next transaction

    #             shares = transaction['Shares']
    #             portfolio_value += shares * price
        
    #     return portfolio_value

    def calculate_returns(self, price_data):
        final_balance = self.get_balance()
        cash_balance = self.initialBalance
        returns = ((final_balance - cash_balance) / (cash_balance))
        return returns
    

    def backtest_strategy(self, strategy, price_data, start_date, end_date):
        self.start_date, self.end_date = start_date, end_date
        choice = strategy.get_choice()
        signals = strategy.get_signals()
        if not isinstance(start_date, pd.Timestamp):
            start_date = pd.Timestamp(start_date)
        if not isinstance(end_date, pd.Timestamp):
            end_date = pd.Timestamp(end_date)
        shares = 1000
        for _, signal in signals.iterrows():
            date = signal['Date']

            # Check if the signal date is after the start date and before the end date
            if start_date <= pd.Timestamp(date) <= end_date:

                if choice =='bb' or choice =='both':
                    
                    if signal['FNGD BB Buy'] == 1:
                        self.buy('FNGD', price_data['FNGD'][price_data['FNGD']['Date'] == date]['Adj Close'].values[0], shares, date)

                    elif signal['FNGD BB Sell'] == 1:
                        self.sell('FNGD', price_data['FNGD'][price_data['FNGD']['Date'] == date]['Adj Close'].values[0], shares, date)
                    if signal['FNGU BB Sell'] == 1:
                        self.sell('FNGU', price_data['FNGU'][price_data['FNGU']['Date'] == date]['Adj Close'].values[0], shares, date)
                    elif signal['FNGU BB Buy'] == 1:
                        self.buy('FNGU', price_data['FNGU'][price_data['FNGU']['Date'] == date]['Adj Close'].values[0], shares, date)
                
                if choice =='ma' or choice =='both':
                    if signal['FNGD MA Buy'] == 1:
                        self.buy('FNGD', price_data['FNGD'][price_data['FNGD']['Date'] == date]['Adj Close'].values[0], shares, date)

                    elif signal['FNGD MA Sell'] == 1:
                        self.sell('FNGD', price_data['FNGD'][price_data['FNGD']['Date'] == date]['Adj Close'].values[0], shares, date)

                    if signal['FNGU MA Buy'] == 1:
                        self.buy('FNGU', price_data['FNGU'][price_data['FNGU']['Date'] == date]['Adj Close'].values[0], shares, date)

                    elif signal['FNGU MA Sell'] == 1:
                        self.sell('FNGU', price_data['FNGU'][price_data['FNGU']['Date'] == date]['Adj Close'].values[0],shares, date)

        for symbol, shares in self.get_remaining_shares().items(): 
            if shares > 0:
                
                closing_price = price_data[symbol][price_data[symbol]['Date'] == end_date]['Adj Close'].values[0]
                self.sell(symbol, closing_price, shares, end_date)
        
        final_balance = self.get_balance()
        returnsP = self.calculate_returns(price_data)
      
        returnsD = final_balance - self.initialBalance
        return final_balance, returnsP, returnsD
