from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import create_engine
import urllib.parse as urlparse
import logging
import os
from logging.handlers import RotatingFileHandler
import redis

db = SQLAlchemy()
migrate = Migrate()
redis_url = urlparse.urlparse(Config.REDISCLOUD_URL)
r = redis.Redis(host=redis_url.hostname, port=redis_url.port, password=redis_url.password)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.backtesting import bp as backtesting_bp
    app.register_blueprint(backtesting_bp)

    if not app.debug and not app.testing:
        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/HistoricalDataProvider.log', maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('HistoricalDataProvider Startup')
    
    return app


from app import models
