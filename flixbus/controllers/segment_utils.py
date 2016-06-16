from models.common import Segment
from app import db
from sqlalchemy.sql import text
from services.route_ride_service import (get_routes_for_segment,
                                         get_segments_in_routes)
from services.ticket_service import get_tickets_for_rides


class SegmentUtils(object):

    @staticmethod
    def check_ticket_overlap(stop_list, from_stop, to_stop,
                             segment_from_stop, segment_to_stop):
        is_from_checked = False
        is_segment_detected = False
        is_ticket_overlap = False
        travel_distance = 0
        for stop in stop_list:
            if is_from_checked:
                travel_distance += stop[2]
            if stop[0] == from_stop:
                is_from_checked = True
                travel_distance = 0  # Take the shortest route
                travel_distance += stop[2]
            if stop[0] == segment_from_stop and stop[1] == segment_to_stop:
                is_segment_detected = True
                if not is_from_checked:
                    break
            if is_from_checked and stop[1] == to_stop:
                if is_segment_detected:
                    is_ticket_overlap = True
                    break
        return is_ticket_overlap, travel_distance

    @staticmethod
    def calculate_segment_cost(travel_distance, segment_distance,
                               ticket_price):
        return ticket_price/travel_distance * segment_distance

    @staticmethod
    def get_passengers_count_and_revenue(segment_id):
        segment = Segment.query.get(segment_id)

        route_ids = get_routes_for_segment(segment_id)
        segment_in_routes = get_segments_in_routes(route_ids)

        route_detail = {}
        for mapping in segment_in_routes:
            if mapping.route_id in route_detail:
                route_detail_list = route_detail.get(mapping.route_id)
                route_detail_list.append(
                    (
                        mapping.segment.from_stop,
                        mapping.segment.destination_stop,
                        mapping.segment.distance
                    )
                )
            else:
                route_detail[mapping.route_id] = [
                    (
                        mapping.segment.from_stop,
                        mapping.segment.destination_stop,
                        mapping.segment.distance

                    )
                ]
        tickets_for_rides = get_tickets_for_rides(route_ids)
        passenger_count = 0
        segment_revenue = 0
        for ticket in tickets_for_rides:
            stop_list = route_detail.get(ticket.ride.route_id)
            is_travel_segment, travel_dist = SegmentUtils.check_ticket_overlap(
                stop_list,
                ticket.from_stop,
                ticket.destination_stop,
                segment.from_stop,
                segment.destination_stop
            )
            if is_travel_segment:
                passenger_count += 1
                segment_revenue += SegmentUtils.calculate_segment_cost(
                    travel_dist,
                    segment.distance,
                    ticket.price)

        return passenger_count, segment_revenue

    @staticmethod
    def pre_process_data(segment_id):
        '''Here data could be processed beforehand to improve the response
        time of api'''
        query = "SELECT *  \
                   FROM flb_segment \
                   JOIN flb_route_segment_mapping \
                     ON flb_route_segment_mapping.segment_id = flb_segment.id \
                   JOIN flb_route \
                     ON flb_route_segment_mapping.route_id=flb_route.id \
                   JOIN flb_ride \
                     ON flb_ride.route_id = flb_route.id \
                  WHERE flb_segment.id = :segment_id"
        result = db.session.execute(text(query).params(segment_id=segment_id))
        for v in result:
            for column, value in v.items():
                print('{0}: {1}'.format(column, value))