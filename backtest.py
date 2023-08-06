import pandas as pd
from TradingStrat import TradingStrategy
from Account import Account
# import jsonLoader

def load_price_data():
    # Load data
    fngd_data = pd.read_json('FNGD.json')
    fngu_data = pd.read_json('FNGU.json')
    return {'FNGD': fngd_data, 'FNGU': fngu_data}

def get_user_input():
    strategy_choice = input("Enter the strategy to use (MA/BB/Both): ").lower()
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")
    return strategy_choice, start_date, end_date



def Ibacktest():
    # Load price data
    price_data = load_price_data()

    # Get user input for strategy and time period
    # strategy_choice, start_date, end_date = get_user_input()

    # Create instance of TradingStrategy class based on user's strategy choice
    
    strategy_choice = 'both'
    start_date = '2023-01-01'
    end_date = '2023-01-13'
    strategy = TradingStrategy(price_data['FNGD'], price_data['FNGU'], strategy_choice=strategy_choice, window_size=20)

        
    # Create instance of Account class
    account = Account()

    final_balance, returnsP, returnsD= account.backtest_strategy(strategy, price_data, start_date, end_date)    
    print(f"\nFinal Account Balance: ${final_balance:.2f}")
    print(f"Returns Gained: ${returnsD:.2f}")
    print(f"Returns Percentage: {returnsP:.2%}")

Ibacktest()