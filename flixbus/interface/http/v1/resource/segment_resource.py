'''
    Segment API Resources
'''
import json
import flask
from flask import request
from flask.ext import restful

from interface.http.v1.decorators import authenticate_user

from schema import (SegmentHeadersSchema, SegmentBodySchema)
from utils import SchemaValidatorMixin
from controllers.segment_controller import (SegmentListController,
                                            SegmentDetailController)


class SegmentList(SchemaValidatorMixin, restful.Resource):
    decorators = [authenticate_user()]
    controller_class = SegmentListController
    schema_validator_class = SegmentHeadersSchema
    __schema_args_source__ = ['request_headers', 'request_args']

    def get(self):
        controller = self.controller_class(metadata=self.metadata)
        return flask.make_response(
            json.dumps(controller.serialized_repr), 200,
            {'Content-Type': 'application/json'}
        )

    def post(self):
        post_body_schema = SegmentBodySchema(strict=True)
        data = post_body_schema.load(request.json).data
        controller = self.controller_class(data=data, metadata=self.metadata)
        return flask.make_response(
            json.dumps(controller.serialized_repr), 201,
            {'Content-Type': 'application/json'}
        )


class SegmentDetail(SchemaValidatorMixin, restful.Resource):
    decorators = [authenticate_user()]
    controller_class = SegmentDetailController
    schema_validator_class = SegmentHeadersSchema
    __schema_args_source__ = ['request_headers', 'request_args']

    def get(self, segment_id):
        controller = self.controller_class(segment_id, metadata=self.metadata)
        return flask.make_response(
            json.dumps(controller.serialized_repr), 200,
            {'Content-Type': 'application/json'}
        )

    def put(self, segment_id):
        put_body_schema = SegmentBodySchema(strict=True)
        data = put_body_schema.load(request.json).data
        controller = self.controller_class(
            segment_id, data=data, metadata=self.metadata
        )
        return flask.make_response(
            json.dumps(controller.serialized_repr), 200,
            {'Content-Type': 'application/json'}
        )

    def delete(self, segment_id):
        self.controller_class(segment_id, is_delete=True)
        return flask.make_response('', 204)
