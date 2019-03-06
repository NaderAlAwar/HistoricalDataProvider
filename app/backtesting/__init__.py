from flask import Blueprint

bp = Blueprint('backtesting', __name__)

from app.backtesting import routes