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
from collections import deque

def get_data(stock_ticker, start_date, end_date):
    data_status = check_data_status(stock_ticker)
    stock_record = []
    missing_data = []
    if is_data_present(data_status, start_date, end_date):
        stock_record = StockDailyPrice.query.filter_by(stock_ticker=stock_ticker).filter(StockDailyPrice.date.between(start_date, end_date)).order_by(asc(StockDailyPrice.date)).all()
        newest_date = stock_record[-1].date
        oldest_date = stock_record[0].date
        stock_record = [stock_price.to_dict() for stock_price in stock_record]
        current_date = datetime.now()
        data_status.last_accessed = current_date
        if end_date.date() != newest_date.date():
            missing_data = fetch_missing_data(stock_ticker, newest_date + timedelta(days=1), end_date)
            stock_record = stock_record + missing_data
        if start_date.date() != oldest_date.date():
            missing_data = fetch_missing_data(stock_ticker, start_date, oldest_date - timedelta(days=1))
            stock_record = missing_data + stock_record
    else:
        current_date = datetime.now()
        data_status.data_present = True
        missing_data = fetch_missing_data(stock_ticker, start_date, end_date)
        stock_record = missing_data
    data_status.newest_date = end_date
    data_status.oldest_date = start_date
    data_status.number_of_entries = data_status.number_of_entries + len(missing_data)
    db.session.commit()
    return stock_record

def check_data_status(stock_ticker):
    try:
        stock_ticker_data_status = StockTickerInfo.query.filter_by(stock_ticker=stock_ticker).one()
        return stock_ticker_data_status
    except NoResultFound:
        stock_ticker_data_status = StockTickerInfo(stock_ticker=stock_ticker, last_accessed=datetime.now(), data_present=False, number_of_entries=0)
        db.session.add(stock_ticker_data_status)
        db.session.commit()
        return stock_ticker_data_status

def is_data_present(data_status, start_date, end_date):
    if data_status.data_present == False:
        return False
    if end_date.date() < data_status.oldest_date.date():
        return False
    if start_date.date() > data_status.newest_date.date():
        return False
    return True

def fetch_missing_data(stock_ticker, start_date, end_date):
    stock_data = get_historical_data(stock_ticker, start_date, end_date)
    stock_data_list = []
    for key, value in sorted(stock_data.items()):
        datetime_object = datetime.strptime(key, '%Y-%m-%d')
        daily_price = StockDailyPrice(stock_ticker=stock_ticker, date=datetime_object, open_price=value['open'])
        stock_data_list.append(daily_price.to_dict())
        db.session.add(daily_price)
    return stock_data_list