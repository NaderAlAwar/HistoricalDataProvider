from app import db
from datetime import datetime

class StockDailyPrice(db.Model):
    stock_ticker = db.Column(db.String(), primary_key=True)
    date = db.Column(db.DateTime, primary_key=True)
    open_price = db.Column(db.Float, index=True)
    
    def __repr__(self):
        return '<StockDailyPrice {}>'.format(self.stock_ticker + " " + str(self.date))    
    
    def to_dict(self):
        data = {
            'stock_ticker': self.stock_ticker,
            'date': self.date,
            'open_price': self.open_price
        }
        return data

class StockTickerInfo(db.Model):
    stock_ticker = db.Column(db.String(), primary_key=True)
    last_accessed = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    data_present = db.Column(db.Boolean, index=True)
    oldest_date = db.Column(db.DateTime)
    newest_date = db.Column(db.DateTime)
    number_of_entries = db.Column(db.Integer)

    def to_dict(self):
        data = {
            'stock_ticker': self.stock_ticker,
            'last_accessed': self.last_accessed,
            'data_present': self.data_present,
            'oldest_date': self.oldest_date,
            'newest_date': self.newest_date,
            'number_of_entries': self.number_of_entries
        }
        return data