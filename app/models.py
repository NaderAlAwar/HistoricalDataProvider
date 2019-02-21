from app import db

class StockDailyPrice(db.Model):
    stock_ticker = db.Column(db.String(), primary_key=True)
    date = db.Column(db.DateTime, primary_key=True)
    close_price = db.Column(db.Float, index=True)
    open_price = db.Column(db.Float, index=True)
    lowest_price = db.Column(db.Float, index=True)
    volume = db.Column(db.Float, index=True)
    highest_price = db.Column(db.Float, index=True)
    
    def __repr__(self):
        return '<StockDailyPrice {}>'.format(self.stock_ticker + " " + str(self.date))    
    
    def to_dict(self):
        data = {
            'stock_ticker': self.stock_ticker,
            'date': self.date,
            'close_price': self.close_price,
            'open_price': self.open_price,
            'lowest_price': self.lowest_price,
            'volume': self.volume,
            'highest_price': self.highest_price
        }
        return data
