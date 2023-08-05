import pandas as pd
from TradingStrat import TradingStrategy
from Account import Account

def load_price_data():
    # Load data
    fngd_file = 'FNGD.json'
    fngu_file = 'FNGU.json'
    
    fngd_data = pd.read_json(fngd_file)
    fngu_data = pd.read_json(fngu_file)
    return {'FNGD': fngd_data, 'FNGU': fngu_data}

def get_user_input():
    strategy_choice = input("Enter the strategy to use (MA/BB/Both): ").lower()
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")
    return strategy_choice, start_date, end_date

if __name__ == '__main__':
    # Load price data interactively
    price_data = load_price_data()

    # Get user input for strategy and time period
    strategy_choice, start_date, end_date = get_user_input()

    # Create instance of TradingStrategy class based on user's strategy choice
    strategy = TradingStrategy(price_data['FNGD'], price_data['FNGU'], strategy_choice=strategy_choice, window_size=20)

    # Create instance of Account class
    account = Account()

    # Backtest the strategy
    final_balance, returns = account.backtest_strategy(strategy, price_data, start_date, end_date)    
    print(f"\nFinal Account Balance: ${final_balance:.2f}")
    print(f"Returns: {returns:.2%}")
