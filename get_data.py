from datetime import datetime, timedelta
import pandas as pd
from iexfinance.stocks import get_historical_data
from app.models import StockDailyPrice
from app.models import StockTickerInfo
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import asc
from app import db
from data_manipulation import dict_to_dataframe
from dateutil.relativedelta import relativedelta

def get_data(stock_ticker):
    data_status = check_data_status(stock_ticker)
    if data_status.data_present == True:
        stock_record = StockDailyPrice.query.filter_by(stock_ticker=stock_ticker).order_by(asc(StockDailyPrice.date)).all()
        newest_date = stock_record[-1].date
        oldest_date = stock_record[0].date
        stock_record = [stock_price.to_dict() for stock_price in stock_record]
        current_date = datetime.now()
        data_status.last_accessed = current_date
        if current_date.date() != newest_date.date():
            latest_data = fetch_new_data(stock_ticker, newest_date + timedelta(days=1), current_date)
            for key, value in sorted(latest_data.items()):
                datetime_object = datetime.strptime(key, '%Y-%m-%d')
                daily_price = StockDailyPrice(stock_ticker=stock_ticker, date=datetime_object, close_price=value['close'], open_price=value['open'], lowest_price=value['low'], volume=value['volume'], highest_price=value['high'])
                stock_record.append(daily_price.to_dict())
                db.session.add(daily_price)
            data_status.newest_date = current_date
            data_status.number_of_entries = data_status.number_of_entries + len(latest_data)
            db.session.commit()
        return stock_record
    else:
        current_date = datetime.now()
        data_status.data_present = True
        stock_data = fetch_new_data(stock_ticker, current_date - relativedelta(years=5), current_date)
        stock_record = []
        stock_record_dict = []
        for key, value in sorted(stock_data.items()):
            datetime_object = datetime.strptime(key, '%Y-%m-%d')
            daily_price = StockDailyPrice(stock_ticker=stock_ticker, date=datetime_object, close_price=value['close'], open_price=value['open'], lowest_price=value['low'], volume=value['volume'], highest_price=value['high'])
            stock_record.append(daily_price)
            stock_record_dict.append(daily_price.to_dict())
            db.session.add(daily_price)
        data_status.oldest_date = stock_record[-1].date  
        data_status.newest_date = stock_record[0].date      
        data_status.number_of_entries = len(stock_data)
        db.session.commit()
        return stock_record_dict

def check_data_status(stock_ticker):
    try:
        stock_ticker_data_status = StockTickerInfo.query.filter_by(stock_ticker=stock_ticker).one()
        return stock_ticker_data_status
    except NoResultFound:
        stock_ticker_data_status = StockTickerInfo(stock_ticker=stock_ticker, last_accessed=datetime.now(), data_present=False)
        db.session.add(stock_ticker_data_status)
        db.session.commit()
        return stock_ticker_data_status

def fetch_new_data(stock_ticker, start_date, end_date):
    stock_data = get_historical_data(stock_ticker, start_date, end_date)
    return stock_data