import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    REDISCLOUD_URL = 'redis://rediscloud:JHvZmJmZTiMCbAg5Q0Gbm9MlS1Pv1KGC@redis-13359.c52.us-east-1-4.ec2.cloud.redislabs.com:13359'