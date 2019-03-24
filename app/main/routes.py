"""
.. module:: main
   :synopsis: All endpoints getting the historical data are defined here
.. moduleauthor:: Nader Al Awar <github.com/naderalawar>
"""

from app.main import bp
from flask import request
from get_data import get_data
from flask import jsonify

@bp.route("/")
def hello():
    return "Hello Flask, on Azure App Service for Linux"

@bp.route("/api/data", methods=['GET'])
def get_stock_ticker_data():
    """
        **Get the historical data**

        This function allows the user to get the historical data of a stock from five years ago

        :param ticker: ticker of the stock
        :type ticker: int
        :return: json of historical data 

        - Example ::
            
            GET http://127.0.0.1:5000/api/data?ticker=GOOG
        
         - Expected Success Response::

            [
                {
                    "close_price":558.46,
                    "date":"Thu, 27 Mar 2014 00:00:00 GMT",
                    "highest_price":568.0,
                    "lowest_price":552.92,
                    "open_price":568.0,
                    "stock_ticker":"GOOG",
                    "volume":13052.0
                },
                {

                },
            ]
    """
    stock_ticker = request.args.get('ticker')
    return jsonify(get_data(stock_ticker))