from models.ticket import Ticket
from models.common import Ride


def get_tickets_for_rides(route_ids):
    rides_in_routes = Ride.route_id.in_(route_ids)
    tickets_for_rides = Ticket.query.filter(rides_in_routes).join(
        Ride, Ticket.ride_id == Ride.id).all()
    return tickets_for_rides


def check_ticket_added_for_segment(segment_id, e_tag):
    '''This function will be used in future to check if tickets added for
    segments after the date e_tag was created'''
    pass
