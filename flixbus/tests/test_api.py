import app
from config import Config
from flask import current_app
from flask.ext.testing import TestCase
from interface.http.v1.api import v1
from mock import patch


class TestAfterRequest(TestCase):
    def create_app(self):
        _app = app.create_app()
        _app.register_blueprint(v1)
        return _app

    def setUp(self):
        self.DATABASE_QUERY_TIMEOUT = Config.DATABASE_QUERY_TIMEOUT
        Config.DATABASE_QUERY_TIMEOUT = 0
        self.headers = {'user': 1, 'app_version': '1',
                        'app_client': 'flixbus_data_app', 'device_id': '1'}

    def test_after_request(self):
        with patch.object(
            current_app.logger, 'warning', return_value=None
        ) as mock_method:
            self.client.get('/segment', headers=dict(self.headers.items()))
            self.assertGreaterEqual(mock_method.call_count, 1)

    def tearDown(self):
        Config.DATABASE_QUERY_TIMEOUT = self.DATABASE_QUERY_TIMEOUT
