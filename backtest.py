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
    start_date = '2020-01-01'
    end_date = '2023-07-21'
    # Filter price data based on user's preferred time period

    # Create instance of Account class
    account = Account()

    # Backtest the strategy
    final_balance, returns = account.backtest_strategy(strategy, price_data, start_date, end_date)    
    print(f"Final Account Balance: ${final_balance:.2f}")
    print(f"Returns: {returns:.2%}")
# Assuming you have defined 'strategy' and 'price_data'
# price_data = load_price_data()
# strategy = TradingStrategy(price_data['FNGD'], price_data['FNGU'], window_size=20)
# # Define the date range for backtesting
# start_date = pd.Timestamp('2023-01-01')
# end_date = pd.Timestamp('2023-06-30')

# # Create an instance of the Account class
# account = Account()

# # Backtest the strategy for the specified date range
# final_balance, returns = account.backtest_strategy(strategy, price_data, start_date, end_date)

# # Print the results
# print("Final Balance:", final_balance)
# print("Returns:", returns)
