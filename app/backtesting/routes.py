from app.backtesting import bp
from flask import request
from get_data import get_data
from flask import jsonify
from get_statistics import get_statistics

@bp.route("/api/backtest", methods=['POST'])
def get_stock_ticker_data():
    portfolio = request.get_json(force=True)
    get_statistics(portfolio)
    return jsonify(portfolio)