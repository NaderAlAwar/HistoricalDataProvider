from flask import Blueprint

bp = Blueprint('data_fetching', __name__)

from app.data_fetching import routes