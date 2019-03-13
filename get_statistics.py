import pandas as pd
from get_data import get_data

def prepare_dataframe(portfolio):
    # portfolio is a dict mapping stocks to weights
    stock_prices = {}

    for key, value in portfolio.items():
        stock_prices[key] = get_data(key)
    df = dict_to_dataframe(stock_prices)
    df.dropna(inplace=True)
    df = compute_total_value(df, portfolio)
    return df

def compute_total_value(prices_over_time, portfolio):
    df = prices_over_time
    for column in df:
        df[column] = df[column].apply(lambda x: x * portfolio[column]) # multiply each column by the number of stocks bought to get total price
    stocks_list = list(df)
    df['total_value'] = df.sum(axis=1)
    df.drop(stocks_list, axis=1, inplace=True)
    return df

def compute_daily_returns(prices_over_time):
    df = prices_over_time
    df['daily_returns'] = df.diff()
    return df

def compute_moving_average(prices_over_time, window):
    df = prices_over_time
    df['moving_average'] = float('nan')
    df['moving_average'] = df.rolling(window=window).mean()
    return df

def compute_moving_standard_deviation(prices_over_time, window):
    df = prices_over_time
    df['moving_standard_deviation'] = float('nan')
    df['moving_standard_deviation'] = df.rolling(window=window).std()
    return df

def compute_statistics(prices_over_time):
    df = prices_over_time
    df = compute_daily_returns(df)
    df = compute_moving_average(df, 50)
    df = compute_moving_standard_deviation(df, 50)
    return df

def dict_to_dataframe(stock_prices_dict): # takes in a dictionary of stock prices and returns a dataframe
    list_of_earliest_dates = []
    list_of_oldest_dates = []

    for key, value in stock_prices_dict.items():
        list_of_earliest_dates.append(value[0]['date'])
        list_of_oldest_dates.append(value[-1]['date'])

    earliest_date = max(list_of_earliest_dates) # to get a common starting point for all stocks
    oldest_date = min(list_of_oldest_dates) # to get a common ending point for all stocks
    df = pd.DataFrame() # this will contain a column for each stock and be indexed by date
    df['date'] = pd.date_range(earliest_date, oldest_date)
    df = df.set_index(['date'])

    for key, value in stock_prices_dict.items():
        df[key] = float('nan')
        for stock_quote in value:
            current_date = stock_quote['date']
            if current_date < earliest_date or current_date > oldest_date:
                continue
            df.at[current_date, key] = stock_quote['close_price']
    
    return df            