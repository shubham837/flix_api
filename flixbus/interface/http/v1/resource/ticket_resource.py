'''
    Ticket API Resources
'''
import json
import flask
from flask import request
from flask.ext import restful

from interface.http.v1.decorators import authenticate_user

from schema import (TicketHeadersSchema,
                    TicketBodySchema)
from utils import SchemaValidatorMixin
from controllers.ticket_controller import (TicketListController,
                                           TicketDetailController)


class TicketList(SchemaValidatorMixin, restful.Resource):
    decorators = [authenticate_user()]
    controller_class = TicketListController
    schema_validator_class = TicketHeadersSchema
    __schema_args_source__ = ['request_headers', 'request_args']

    def get(self):
        controller = self.controller_class(metadata=self.metadata)
        return flask.make_response(
            json.dumps(controller.serialized_repr), 200,
            {'Content-Type': 'application/json'}
        )

    def post(self):
        post_body_schema = TicketBodySchema(strict=True)
        data = post_body_schema.load(request.json).data
        controller = self.controller_class(data=data, metadata=self.metadata)
        return flask.make_response(
            json.dumps(controller.serialized_repr), 201,
            {'Content-Type': 'application/json'}
        )


class TicketDetail(SchemaValidatorMixin, restful.Resource):
    decorators = [authenticate_user()]
    controller_class = TicketDetailController
    schema_validator_class = TicketHeadersSchema

    def get(self, ticket_id):
        controller = self.controller_class(ticket_id, metadata=self.metadata)
        return flask.make_response(
            json.dumps(controller.serialized_repr), 200,
            {'Content-Type': 'application/json'}
        )

    def put(self, ticket_id):
        put_body_schema = TicketBodySchema(strict=True)
        data = put_body_schema.load(request.json).data
        controller = self.controller_class(
            ticket_id, data=data, metadata=self.metadata
        )
        return flask.make_response(
            json.dumps(controller.serialized_repr), 200,
            {'Content-Type': 'application/json'}
        )

    def delete(self, ticket_id):
        self.controller_class(ticket_id, is_delete=True)
        return flask.make_response('', 204)
