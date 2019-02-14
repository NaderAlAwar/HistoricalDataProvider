from datetime import datetime
from iexfinance.stocks import get_historical_data
from flask import jsonify

# dates should be in the format 'DDMMYYYY'

def get_data(stock_ticker, start_date, end_date):
    start_date = datetime.strptime(start_date, "%d%m%Y")
    end_date = datetime.strptime(end_date, "%d%m%Y")

    df = get_historical_data(stock_ticker, start_date, end_date)
    return jsonify(df)