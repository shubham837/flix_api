import logging
import redis

from logging.handlers import RotatingFileHandler
from flask import Flask

import config
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def logging_setup(app):
    # add log file handler to app
    file_handler = RotatingFileHandler(
        app.config['LOGGING_LOCATION'],
        maxBytes=4 * 1024 * 1024,  # 4 MB
        backupCount=10
    )
    file_handler.setLevel(app.config['LOGGING_LEVEL'])
    formatter = logging.Formatter(app.config['LOGGING_FORMAT'])
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)


def redis_setup(app):
    # attach redis pool to app
    redis_pool = redis.ConnectionPool(
        host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'], db=0
    )
    app.redis_client = redis.Redis(connection_pool=redis_pool)


def create_app(testing=False):
    app = Flask(__name__)
    configuration = config.TestingConfig if testing else config.Config
    app.config.from_object(configuration)
    # attach db to app
    db.init_app(app)

    redis_setup(app)

    logging_setup(app)

    return app
