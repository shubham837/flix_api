from models.common import Ride, RouteSegmentMapping
from sqlalchemy.orm import joinedload


def get_routes_for_segment(segment_id):
    route_segment_mappings = RouteSegmentMapping.query.filter_by(
        segment_id=segment_id
    ).all()

    route_ids = []
    for mapping in route_segment_mappings:
        route_ids.append(mapping.route_id)

    return route_ids


def get_segments_in_routes(route_ids):

    routes_in_query = RouteSegmentMapping.route_id.in_(route_ids)

    segment_in_routes = RouteSegmentMapping.query.filter(
        routes_in_query).options(
        joinedload(RouteSegmentMapping.segment)).order_by(
        RouteSegmentMapping.segment_sequence.asc()).all()

    return segment_in_routes


def check_segment_added_in_route(segment_id):
    '''This function will be used in future to check if segment is added
    in new route'''
    pass