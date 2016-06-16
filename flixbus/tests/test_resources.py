import app
from flask.ext.testing import TestCase
from interface.http.v1.api import v1
from interface.http.v1.resource.segment_resource import (SegmentList,
                                                         SegmentDetail)
from interface.http.v1.resource.routes_rides_resource import (RouteList,
                                                              RouteDetail,
                                                              RideList)
from interface.http.v1.resource.ticket_resource import (TicketList,
                                                        TicketDetail)
from werkzeug.datastructures import EnvironHeaders

from flask import request


class SchemaValidationFailureMixin(object):
    def _test_schema_validation_success(self, method, endpoint,
                                        headers_extra={}):
        headers = {'user': 1,
                   'app_client': 'flixbus_data_app'}
        resp = getattr(self.client, method)(
            endpoint, headers=dict(headers.items() +
                                   headers_extra.items()))
        self.assertEquals(resp.status_code, 200)

    def _test_schema_validation_failure(self, method, endpoint,
                                        headers_extra={}):
        headers = {'user': 1,
                   'app_client': 'flixbus_data_app'}
        resp = getattr(self.client, method)(
            endpoint, headers=dict(headers.items() +
                                   headers_extra.items()))
        self.assertEquals(resp.status_code, 400)


class SegmentResourceTestCase(SchemaValidationFailureMixin, TestCase):
    def create_app(self):
        _app = app.create_app()
        _app.register_blueprint(v1)
        return _app

    def setUp(self):
        self.headers = EnvironHeaders({
            'HTTP_USER': 1,
            'HTTP_APP_CLIENT': 'flixbus_data_app',
        })

    def test_segment_list_schema_validators_valid(self):
        request.headers = EnvironHeaders({
            'HTTP_USER': 1,
            'HTTP_APP_CLIENT': 'flixbus_data_app'
        })
        expected = {
            'user_id': 1,
            'source': 'flixbus_data_app',
            'limit': 20,
            'start': 0
        }
        clst = SegmentList()
        self.assertEquals(clst.metadata, expected)

    def test_segment_detail_schema_validators(self):
        request.headers = EnvironHeaders({
            'HTTP_USER': 1,
            'HTTP_APP_CLIENT': 'flixbus_data_app'
        })
        expected = {
            'user_id': 1,
            'source': 'flixbus_data_app',
            'limit': 20,
            'start': 0
        }
        cdl = SegmentDetail()
        self.assertEquals(cdl.metadata, expected)

    def test_schema_validation_failure(self):
        self._test_schema_validation_success('get', '/segment')
        self._test_schema_validation_success('get', '/segment/1')
        self._test_schema_validation_success('put', '/segment/1')


class TestAppWrapper(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        environ['HTTP_USER'] = 1
        environ['app_client'] = 'flixbus_data_app'
        return self.app(environ, start_response)


class RouteResourceTestCase(SchemaValidationFailureMixin, TestCase):
    def create_app(self):
        _app = app.create_app()
        _app.register_blueprint(v1)
        return _app

    def test_route_list_schema_validators(self):
        request.headers = EnvironHeaders({
            'HTTP_USER': 1,
            'HTTP_APP_CLIENT': 'flixbus_data_app',
        })
        expected = {
            'user_id': 1,
            'source': 'flixbus_data_app',
            'limit': 20,
            'start': 0
        }
        clst = RouteList()
        self.assertEquals(clst.metadata, expected)

    def test_route_detail_schema_validators(self):
        request.headers = EnvironHeaders({
            'HTTP_USER': 1,
            'HTTP_APP_CLIENT': 'flixbus_data_app',
        })
        expected = {
            'user_id': 1,
            'source': 'flixbus_data_app',
            'limit': 20,
            'start': 0
        }
        clst = RouteDetail()
        self.assertEquals(clst.metadata, expected)

    def test_schema_validation_failure(self):
        self._test_schema_validation_success('get', '/route')
        self._test_schema_validation_success('get', '/route/1')


class RideResourceTestCase(SchemaValidationFailureMixin, TestCase):
    def create_app(self):
        _app = app.create_app()
        _app.register_blueprint(v1)
        return _app

    def test_ride_schema_validators(self):
        request.headers = EnvironHeaders({
            'HTTP_USER': 1,
            'HTTP_APP_CLIENT': 'flixbus_data_app'
        })
        expected = {
            'user_id': 1,
            'source': 'flixbus_data_app',
            'limit': 20,
            'start': 0
        }
        clst = RideList()
        self.assertEquals(clst.metadata, expected)

    def test_schema_validation_failure(self):
        self._test_schema_validation_success('get', '/route/1/ride')


class TicketResourceTestCase(SchemaValidationFailureMixin, TestCase):
    def create_app(self):
        _app = app.create_app()
        _app.register_blueprint(v1)
        return _app

    def test_ticket_schema_validators(self):
        request.headers = EnvironHeaders({
            'HTTP_USER': 1,
            'HTTP_APP_CLIENT': 'flixbus_data_app'
        })
        expected = {
            'user_id': 1,
            'source': 'flixbus_data_app',
            'limit': 20,
            'start': 0
        }
        clst = TicketList()
        self.assertEquals(clst.metadata, expected)

    def test_ticket_detail_schema_validators(self):
        request.headers = EnvironHeaders({
                'HTTP_USER': 1,
                'HTTP_APP_CLIENT': 'flixbus_data_app'
        })
        expected = {
            'user_id': 1,
            'source': 'flixbus_data_app',
            'limit': 20,
            'start': 0
        }
        cdl = TicketDetail()
        self.assertEquals(cdl.metadata, expected)

    def test_schema_validation_failure(self):
        self._test_schema_validation_success('get', '/ticket')
        self._test_schema_validation_success('get', '/ticket/1')
