import time
from statsd import StatsClient

from flask import current_app
from flask import request
from flask.ext.sqlalchemy import get_debug_queries

import config


def log_queries(min_time=config.Config.DATABASE_QUERY_TIMEOUT):
    def wrap(func):
        def wrapped(*args, **kwargs):
            number_of_queries_before = len(get_debug_queries())
            result = func(*args, **kwargs)
            query_list = (get_debug_queries())[number_of_queries_before:]
            request.environ['query_logged'] = True
            for query in query_list:
                if query.duration * 100 >= min_time:
                    current_app.logger.warning(
                        config.Config.QUERY_LOGGING_FORMAT.format(
                            method=request.method, path=request.path,
                            func_name=func.func_name,
                            statement=query.statement, params=query.parameters,
                            duration=query.duration, context=query.context
                        )
                    )
            return result
        return wrapped
    return wrap


def statsd_enabled_only(method):
    def wrapper(self, *args, **kwargs):
        if self.disabled:
            return
        return method(self, *args, **kwargs)
    return wrapper


class StatsdLogger(object):
    def __init__(self, client):
        self.statsd = client
        self.disabled = False
        self.namespace = 'Flixbus'

    def bucket_key(self, name):
        return '%s%s' % (('%s.' % self.namespace) if self.namespace else '',
                         name)

    @statsd_enabled_only
    def _counter(self, path, delta):
        self.statsd.incr(path, delta)

    def _counter_wrapper(self, func, name, delta):
        def inner(*args, **kwargs):
            self._counter(self.bucket_key(name), delta=delta)
            return func(*args, **kwargs)
        return inner

    def increment(self, name, delta=1):
        def decorator(func):
            return self._counter_wrapper(func, name, delta)
        return decorator

    def decrement(self, name, delta=-1):
        def decorator(func):
            return self._counter_wrapper(func, name, delta)
        return decorator

    def counter(self, name, delta):
        return self.increment(name, delta)

    def timer(self, name):
        def decorator(func):
            def wrapper(*args, **kwargs):
                if not self.disabled:
                    start_time = time.time()
                result = func(*args, **kwargs)
                if not self.disabled:
                    end_time = time.time()
                    self.statsd.timing(
                        self.namespace, (end_time-start_time) * 1000
                    )
                return result
            return wrapper
        return decorator

    def gauge(self, name):
        def decorator(func):
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                if not self.disabled:
                    self.statsd.gauge(self.namespace, result)
                return result
            return wrapper
        return decorator


statsd_logger = StatsdLogger(StatsClient())
