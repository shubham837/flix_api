# Source: https://github.com/steinnes/statsdmiddleware
# http://steinn.org/post/flask-statsd/
import resource
import time


def get_cpu_time():
    '''add up user time (ru_utime) and system time (ru_stime).'''
    resources = resource.getrusage(resource.RUSAGE_SELF)
    return resources[0] + resources[1]


class TimingStats(object):
    def __init__(self, statsd, name=''):
        self.statsd = statsd
        self.name = name

    def __enter__(self):
        self.start_time = time.time()
        self.start_cpu_time = get_cpu_time()
        return self

    @property
    def time(self):
        return self.end_time - self.start_time

    @property
    def cpu_time(self):
        return self.end_cpu_time - self.start_cpu_time

    def __exit__(self, exc_type, exc_value, traceback):
        self.end_time = time.time()
        self.end_cpu_time = get_cpu_time()

        self.statsd.incr('{}.count'.format(self.name))
        self.statsd.timing('{}.time'.format(self.name), self.time)
        self.statsd.timing('{}.cpuTime'.format(self.name), self.cpu_time)


class StatsdMiddleware(object):
    def __init__(self, app, statsd, prefix=None):
        self.app = app
        self.wsgi_app = app.wsgi_app
        self.statsd = statsd
        self.map = app.url_map.bind('')
        self.prefix = prefix

    def _metric_name(self, path, method):
        path = self.map.match(path.split('?')[0], method)
        return '{}.path.{}.method.{}'.format(
            self.prefix and 'app.{}'.format(self.prefix) or '',
            path[0].replace('.', '-'), method
        )

    def __call__(self, environ, start_response):
        def start_response_wrapper(*args, **kwargs):
            if len(args) > 0 and isinstance(args[0], str):
                status = args[0].split(' ')[0]
            else:
                status = ''
            self.status = status
            return start_response(*args, **kwargs)

        try:
            metric_name = self._metric_name(
                environ['PATH_INFO'], environ['REQUEST_METHOD']
            )
            with TimingStats(self.statsd, metric_name) as metric:
                response = self.wsgi_app(environ, start_response_wrapper)
                metric.name = '{}.status.{}'.format(metric_name, self.status)
        except Exception:
            # this should only happen if the URL is not supported by our app,
            # in which case we'll just let the app handle the 404 normally
            return self.wsgi_app(environ, start_response_wrapper)

        return response
