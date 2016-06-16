import unittest

from marshmallow import ValidationError

from schema import (BaseHeadersSchema, SegmentBodySchema,
                    RouteBodySchema)


class HeadersSchemaTestCase(unittest.TestCase):

    def test_if_it_fails_on_missing_data(self):
        missing_headers_list = [
            {
                'app_client': 'flixbus_data_app',
            },
            {
                'user': '123',
            }]

        schema = BaseHeadersSchema(strict=True)
        for headers in missing_headers_list:
            with self.assertRaises(ValidationError):
                schema.validate(headers)

    def test_if_it_fails_on_invalid_data(self):
        invalid_headers_list = [
            {
                'user': 'abc',  # user id not integer
                'app_client': 'flixbus_data_app',
            }]

        schema = BaseHeadersSchema(strict=True)
        for headers in invalid_headers_list:
            with self.assertRaises(ValidationError):
                schema.validate(headers)

    def test_if_nothing_is_ignored(self):
        headers = {
            'user': '123',
            'app_client': 'flixbus_data_app',
        }
        schema = BaseHeadersSchema(strict=True)
        self.assertEqual(schema.validate(headers), {})


class SegmentBodySchemaTestCase(unittest.TestCase):

    def test_if_it_throws_error_on_empty_items(self):
        body = {
            'from_stop': 1
        }
        body_schema = SegmentBodySchema(strict=True)
        with self.assertRaises(ValidationError):
            body_schema.load(body)

    def test_if_it_throws_error_on_invalid_items(self):
        body = {
            'from_stop': 'abc',
            'destination_stop': '132'
        }
        schema = SegmentBodySchema(strict=True)
        with self.assertRaises(ValidationError):
            schema.load(body)

    def test_if_loading_is_correct(self):
        body = {
            'from_stop': 13,
            'destination_stop': 132
        }
        schema = SegmentBodySchema(strict=True)
        self.assertEqual(body, schema.load(body).data)


class RouteBodySchemaTestCase(unittest.TestCase):

    def test_if_segments_not_present(self):
        body = {
        }
        schema = RouteBodySchema(strict=True)
        with self.assertRaises(ValidationError):
            schema.load(body)

    def test_if_it_throws_error_on_incorrect_segments(self):
        body = {
            'route_segments': []
        }
        schema = RouteBodySchema(strict=True)
        with self.assertRaises(ValidationError):
            schema.load(body)

    def test_if_segments_are_present(self):
        body = {
            'route_segments': [
                {
                    'segment_id': 1,
                    'segment_sequence': 1
                }
            ]
        }

        schema = RouteBodySchema(strict=True)
        expected_output = {
            'route_segments': [
                {
                    'segment_id': 1,
                    'segment_sequence': 1
                }
            ]
        }
        actual_output = schema.load(body).data
        self.assertEqual(expected_output, actual_output)
