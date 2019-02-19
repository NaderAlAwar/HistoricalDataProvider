from app import app
from flask import request
from get_data import get_data

@app.route("/")
def hello():
    return "Hello Flask, on Azure App Service for Linux"

@app.route("/api/data", methods=['GET'])
def get_stock_ticker_data():
    stock_ticker = request.args.get('ticker')
    return get_data(stock_ticker)