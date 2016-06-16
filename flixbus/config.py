import logging

import secrets


class Config(object):
    DEBUG = True
    PATH = '.'.join([__name__, 'Config'])
    SQLALCHEMY_DATABASE_URI = "postgresql://%s:%s@%s:%s/%s" % (
        secrets.db['user'],
        secrets.db['password'],
        secrets.db['host'],
        secrets.db['port'],
        'test_local_db'
    )

    LOGGING_FORMAT = (
        '[%(asctime)s] [%(levelname)-8s] [%(name)s:%(lineno)s] -- %(message)s'
    )
    QUERY_LOGGING_FORMAT = (
        "{method} {path} {func_name} SLOW QUERY: {statement}\t"
        "Parameters: {params}\tDuration: {duration}s\tContext: {context}"
    )
    LOGGING_LOCATION = '/var/log/flixbus_api/logfile.log'
    LOGGING_LEVEL = logging.DEBUG

    REDIS_HOST = secrets.redis['host']
    REDIS_PORT = secrets.redis['port']

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_RECORD_QUERIES = True
    DATABASE_QUERY_TIMEOUT = 0.50


class TestingConfig(Config):
    DEBUG = True
    PATH = '.'.join([__name__, 'TestingConfig'])
    SQLALCHEMY_DATABASE_URI = "postgresql://%s:%s@%s:%s/%s" % (
        secrets.db['user'],
        secrets.db['password'],
        secrets.db['host'],
        secrets.db['port'],
        'test_case_local_db'
    )
    REDIS_HOST = secrets.redis['host']
    REDIS_PORT = secrets.redis['port']
    LOGGING_LOCATION = '/var/log/flixbus_api/logfile.log'
    QUERY_LOGGING_FORMAT = (
        "{method} {path} {func_name} SLOW QUERY: {statement}\t"
        "Parameters: {params}\tDuration: {duration}s\tContext: {context}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
