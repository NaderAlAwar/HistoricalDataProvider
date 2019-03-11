from app.backtesting import bp
import pandas as pd
from flask import request
from get_data import get_data
from flask import jsonify
from get_statistics import prepare_dataframe
from get_statistics import compute_statistics
from get_statistics import compute_daily_returns
from get_statistics import compute_moving_average
from get_statistics import compute_moving_standard_deviation

@bp.route("/api/backtest", methods=['POST'])
def get_portfolio_statistics():
    portfolio = request.get_json(force=True)
    prices_df = prepare_dataframe(portfolio)
    performance = compute_statistics(prices_df)
    return performance.to_json(orient='index')

@bp.route("/api/backtest/daily_returns", methods=['POST'])
def get_daily_returns():
    portfolio = request.get_json(force=True)
    prices_df = prepare_dataframe(portfolio)
    performance = compute_daily_returns(prices_df)
    return performance.to_json(orient='index')

@bp.route("/api/backtest/moving_average", methods=['POST'])
def get_moving_average():
    portfolio = request.get_json(force=True)
    window = int(request.args.get('window'))
    prices_df = prepare_dataframe(portfolio)
    performance = compute_moving_average(prices_df, window)
    return performance.to_json(orient='index')

@bp.route("/api/backtest/moving_standard_deviation", methods=['POST'])
def get_moving_standard_deviation():
    portfolio = request.get_json(force=True)
    window = int(request.args.get('window'))
    prices_df = prepare_dataframe(portfolio)
    performance = compute_moving_standard_deviation(prices_df, window)
    return performance.to_json(orient='index')