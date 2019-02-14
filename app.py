from flask import Flask
from flask import request
from get_data import get_data
myapp = Flask(__name__)

@myapp.route("/")
def hello():
    return "Hello Flask, on Azure App Service for Linux"

@myapp.route("/api/data", methods=['GET'])
def get_stock_ticker_data():
    stock_ticker = request.args.get('ticker')
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    return get_data(stock_ticker, start_date, end_date)