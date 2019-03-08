import pandas as pd
from get_data import get_data

def get_statistics(portfolio):
    # portfolio is a dict mapping stocks to weights
    stock_prices = {}

    for key, value in portfolio.items():
        stock_prices[key] = get_data(key)

    list_of_earliest_dates = []
    list_of_oldest_dates = []

    for key, value in stock_prices.items():
        list_of_earliest_dates.append(value[0]['date'])
        list_of_oldest_dates.append(value[-1]['date'])

    earliest_date = max(list_of_earliest_dates) # to get a common starting point for all stocks
    oldest_date = min(list_of_oldest_dates) # to get a common ending point for all stocks
    df = pd.DataFrame() # this will contain a column for each stock and be indexed by date
    df['date'] = pd.date_range(earliest_date, oldest_date)
    df = df.set_index(['date'])

    for key, value in stock_prices.items():
        df[key] = float('nan')
        for stock_quote in value:
            current_date = stock_quote['date']
            if current_date < earliest_date or current_date > oldest_date:
                continue
            df.at[current_date, key] = stock_quote['close_price']
    
    print(df)            
    return stock_prices

# def get_earliest_date(stock_prices): # gets the earliest available date of the historical prices
#     for key,value in stock_prices.items():
