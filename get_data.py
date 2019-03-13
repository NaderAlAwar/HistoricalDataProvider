from datetime import datetime, timedelta
from iexfinance.stocks import get_historical_data
from app.models import StockDailyPrice
from app import db

def get_data(stock_ticker):
    # stock_record = StockDailyPrice.query.filter_by(stock_ticker=stock_ticker).all()
    result = []
    # for record in stock_record:
    #     result.append(record.to_dict())
    # if len(stock_record) == 0:
    end_date = datetime.now()
    start_date = datetime(end_date.year - 5, end_date.month, end_date.day)
    stock_record = get_historical_data(stock_ticker, start_date, end_date)
    for key, value in stock_record.items():
        datetime_object = datetime.strptime(key, '%Y-%m-%d')
        daily_price = StockDailyPrice(stock_ticker=stock_ticker, date=datetime_object, close_price=value['close'], open_price=value['open'], lowest_price=value['low'], volume=value['volume'], highest_price=value['high'])
        result.append(daily_price.to_dict())
        # db.session.add(daily_price)
    # db.session.commit()
    return result