import pandas as pd
from TradingStrat import TradingStrategy
from Account import Account

def load_price_data():
    # Load data
    fngd_data = pd.read_json('FNGD.json')
    fngu_data = pd.read_json('FNGU.json')
    return {'FNGD': fngd_data, 'FNGU': fngu_data}


def get_user_input():
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")
    return start_date, end_date

if __name__ == '__main__':
    # Load price data
    price_data = load_price_data()

    # Create instance of TradingStrategy class
    strategy = TradingStrategy(price_data['FNGD'], price_data['FNGU'], window_size=20)

    # Get user input for time period
    start_date, end_date = get_user_input()

    # Filter price data based on user's preferred time period
    price_data['FNGD'] = price_data['FNGD'][(price_data['FNGD']['Date'] >= start_date) & (price_data['FNGD']['Date'] <= end_date)]
    price_data['FNGU'] = price_data['FNGU'][(price_data['FNGU']['Date'] >= start_date) & (price_data['FNGU']['Date'] <= end_date)]

    # Create instance of Account class
    account = Account(initial_balance=100000)

    # Backtest the strategy
    final_balance, returns = account.backtest_strategy(strategy, price_data)
    print(f"Final Account Balance: ${final_balance:.2f}")
    print(f"Returns: {returns:.2%}")