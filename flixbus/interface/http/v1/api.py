'''
    api
    ~~~

    REST API (v1) for Flixbus.
'''
import json
import flask
from flask import request
from flask import current_app
from flask.ext import restful
from flask.ext.sqlalchemy import get_debug_queries
from config import Config
from resource.segment_resource import (SegmentList, SegmentDetail)
from resource.routes_rides_resource import (RouteList, RouteDetail,
                                            RideList, RideDetail)
from resource.ticket_resource import (TicketList, TicketDetail)

# Create a Flask blueprint
v1 = flask.Blueprint('v1', __name__)

# Register the API (flask-restful) with v1 blueprint
api = restful.Api(v1)


@api.app.after_request
def after_request(response, *args, **kwargs):
    if not request.environ.get('query_logged'):
        for query in get_debug_queries():
            if query.duration >= Config.DATABASE_QUERY_TIMEOUT:
                current_app.logger.warning(
                    Config.QUERY_LOGGING_FORMAT.format(
                        method=request.method, path=request.path,
                        func_name='',
                        statement=query.statement, params=query.parameters,
                        duration=query.duration, context=query.context
                    )
                )
    return response


class HealthCheck(restful.Resource):

    def get(self):
        return flask.make_response(
            json.dumps(
                {'message': 'The force is strong with this one.'}, 200,
                {'Content-Type': 'application/json'}
            ))


api.add_resource(SegmentList, '/segment')
api.add_resource(SegmentDetail, '/segment/<int:segment_id>')
api.add_resource(RouteList, '/route')
api.add_resource(RouteDetail, '/route/<int:route_id>')
api.add_resource(RideList, '/route/<int:route_id>/ride')
api.add_resource(RideDetail, '/route/<int:route_id>/ride/<int:ride_id>')
api.add_resource(TicketList, '/ticket')
api.add_resource(TicketDetail, '/ticket/<int:ticket_id>')
api.add_resource(HealthCheck, '/flixbus/health')
