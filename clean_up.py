from flask_script import Manager

from HistoricalDataProvider import app
from app import db
from app.models import StockDailyPrice
from app.models import StockTickerInfo
from operator import itemgetter

manager = Manager(app)

@manager.command
def clean_up():
    stock_data_status = StockTickerInfo.query.filter_by(data_present=True).all()
    stock_data_status_dict = [data.to_dict() for data in stock_data_status]
    stock_data_status_dict = sorted(stock_data_status_dict, key = itemgetter('last_accessed'))
    while (get_number_of_rows() > 9000):
        oldest_data_status = stock_data_status.pop()
        oldest_data_status_dict = stock_data_status_dict.pop()    
        stock_data = StockDailyPrice.query.filter_by(stock_ticker=oldest_data_status_dict['stock_ticker']).delete()
        oldest_data_status.data_present = False
        oldest_data_status.number_of_entries = 0
        db.session.commit()

@manager.command
def clear_db():
    stock_data_status = StockTickerInfo.query.all().delete()
    stock_data = StockDailyPrice.query.all().delete()

@manager.command
def get_all_statuses():
    stock_data_status = StockTickerInfo.query.all()
    stock_data_status = [data.to_dict() for data in stock_data_status]
    for status in stock_data_status:
        print(status)

@manager.command
def get_number_of_rows():
    answer = len(StockDailyPrice.query.all())
    print(answer)
    return answer

if __name__ == "__main__":
    manager.run()