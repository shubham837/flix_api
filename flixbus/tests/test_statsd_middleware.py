import statsd

import app
from flask.ext.testing import TestCase
from interface.http.v1.api import v1
from mock import patch
from statsd import StatsClient
from middleware.statsd import StatsdMiddleware


class TestStatsdMiddleware(TestCase):
    def create_app(self):
        _app = app.create_app()
        _app.wsgi_app = StatsdMiddleware(_app, statsd.StatsClient(),
                                         'Flixbus')
        _app.register_blueprint(v1)
        return _app

    def setUp(self):
        self.headers = {'user': 1, 'app_client': 'flixbus_data_app'}

    def test_middlewaret(self):
        with patch.object(
                    StatsClient, 'incr', return_value=None
                ) as incr_mock_method, patch.object(
                    StatsClient, 'timing', return_value=None
                ) as timing_mock_method:
            self.client.get('/segment', headers=dict(self.headers.items()))
            self.assertEqual(incr_mock_method.call_count, 1)
            self.assertEqual(timing_mock_method.call_count, 2)
