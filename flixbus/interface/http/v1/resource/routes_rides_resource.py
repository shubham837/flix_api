'''
    Routes and Rides API Resources
'''

import json
import flask
from flask import request
from flask.ext import restful

from interface.http.v1.decorators import authenticate_user

from schema import (RouteHeadersSchema, RouteBodySchema,
                    RideHeadersSchema, RideBodySchema)
from utils import SchemaValidatorMixin
from controllers.route_ride_controller import (RouteListController,
                                               RouteDetailController,
                                               RideListController,
                                               RideDetailController)


class RouteList(SchemaValidatorMixin, restful.Resource):
    decorators = [authenticate_user()]
    controller_class = RouteListController
    schema_validator_class = RouteHeadersSchema
    __schema_args_source__ = ['request_headers', 'request_args']

    def get(self):
        controller = self.controller_class(metadata=self.metadata)
        return flask.make_response(
            json.dumps(controller.serialized_repr), 200,
            {'Content-Type': 'application/json'}
        )

    def post(self):
        post_body_schema = RouteBodySchema(strict=True)
        data = post_body_schema.load(request.json).data
        controller = self.controller_class(data=data, metadata=self.metadata)
        return flask.make_response(
            json.dumps(controller.serialized_repr), 201,
            {'Content-Type': 'application/json'}
        )


class RouteDetail(SchemaValidatorMixin, restful.Resource):
    decorators = [authenticate_user()]
    controller_class = RouteDetailController
    schema_validator_class = RouteHeadersSchema
    __schema_args_source__ = ['request_headers', 'request_args']


    def get(self, route_id):
        controller = self.controller_class(route_id, metadata=self.metadata)
        return flask.make_response(
            json.dumps(controller.serialized_repr), 200,
            {'Content-Type': 'application/json'}
        )

    def put(self, route_id):
        put_body_schema = RouteBodySchema(strict=True)
        data = put_body_schema.load(request.json).data
        controller = self.controller_class(
            route_id, is_delete=False, data=data, metadata=self.metadata
        )
        return flask.make_response(
            json.dumps(controller.serialized_repr), 200,
            {'Content-Type': 'application/json'}
        )

    def delete(self, segment_id):
        self.controller_class(segment_id, is_delete=True)
        return flask.make_response('', 204)


class RideList(SchemaValidatorMixin, restful.Resource):
    decorators = [authenticate_user()]
    controller_class = RideListController
    schema_validator_class = RideHeadersSchema
    __schema_args_source__ = ['request_headers', 'request_args']

    def get(self, route_id):
        controller = self.controller_class(route_id=route_id,
                                           metadata=self.metadata)
        return flask.make_response(
            json.dumps(controller.serialized_repr), 200,
            {'Content-Type': 'application/json'}
        )

    def post(self, route_id):
        post_body_schema = RideBodySchema(strict=True)
        data = post_body_schema.load(request.json).data
        controller = self.controller_class(route_id=route_id, data=data,
                                           metadata=self.metadata)
        return flask.make_response(
            json.dumps(controller.serialized_repr), 201,
            {'Content-Type': 'application/json'}
        )


class RideDetail(SchemaValidatorMixin, restful.Resource):
    decorators = [authenticate_user()]
    controller_class = RideDetailController
    schema_validator_class = RideHeadersSchema
    __schema_args_source__ = ['request_headers', 'request_args']

    def get(self, route_id, ride_id):
        controller = self.controller_class(route_id, ride_id,
                                           metadata=self.metadata)
        return flask.make_response(
            json.dumps(controller.serialized_repr), 200,
            {'Content-Type': 'application/json'}
        )

    def put(self, route_id, ride_id):
        put_body_schema = RideBodySchema(strict=True)
        data = put_body_schema.load(request.json).data
        controller = self.controller_class(
            route_id, ride_id, data=data, metadata=self.metadata
        )
        return flask.make_response(
            json.dumps(controller.serialized_repr), 200,
            {'Content-Type': 'application/json'}
        )

    def delete(self, route_id, ride_id):
        self.controller_class(route_id, ride_id, is_delete=True)
        return flask.make_response('', 204)
