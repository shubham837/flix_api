from flask.ext.testing import TestCase
from interface.http.v1.api import v1
from app import create_app, db
from models.common import Segment, Route, RouteSegmentMapping, Ride, Ticket
import json


class TicketListTest(TestCase):
    def create_app(self):
        _app = create_app()
        _app.register_blueprint(v1)
        return _app

    def setUp(self):
        db.drop_all()
        db.create_all()
        self.headers = {'user': 1, 'app_client': 'flixbus_data_app'}

        self.segment1 = Segment(from_stop=1, destination_stop=2,
                                distance=4.5)
        self.segment2 = Segment(from_stop=2, destination_stop=5,
                                distance=3.5)
        self.segment3 = Segment(from_stop=5, destination_stop=7,
                                distance=2.5)
        self.segment4 = Segment(from_stop=2, destination_stop=4,
                                distance=4.5)
        self.segment5 = Segment(from_stop=2, destination_stop=7,
                                distance=4.5)
        self.segment6 = Segment(from_stop=4, destination_stop=2,
                                distance=4.5)

        self.route1 = Route()
        self.route2 = Route()
        self.route3 = Route()
        self.route4 = Route()

        self.route_segment_mapping1 = RouteSegmentMapping(
            route_id=1,
            segment_id=1,
            segment_sequence=1
        )
        self.route_segment_mapping2 = RouteSegmentMapping(
            route_id=1,
            segment_id=2,
            segment_sequence=2
        )
        self.route_segment_mapping3 = RouteSegmentMapping(
            route_id=1,
            segment_id=3,
            segment_sequence=3
        )
        self.route_segment_mapping4 = RouteSegmentMapping(
            route_id=2,
            segment_id=1,
            segment_sequence=1
        )
        self.route_segment_mapping5 = RouteSegmentMapping(
            route_id=2,
            segment_id=5,
            segment_sequence=2
        )
        self.route_segment_mapping6 = RouteSegmentMapping(
            route_id=3,
            segment_id=1,
            segment_sequence=1
        )
        self.route_segment_mapping7 = RouteSegmentMapping(
            route_id=3,
            segment_id=4,
            segment_sequence=2
        )
        self.route_segment_mapping8 = RouteSegmentMapping(
            route_id=3,
            segment_id=6,
            segment_sequence=3
        )
        self.route_segment_mapping9 = RouteSegmentMapping(
            route_id=3,
            segment_id=5,
            segment_sequence=4
        )
        self.route_segment_mapping10 = RouteSegmentMapping(
            route_id=4,
            segment_id=4,
            segment_sequence=1
        )
        self.route_segment_mapping9 = RouteSegmentMapping(
            route_id=4,
            segment_id=6,
            segment_sequence=2
        )
        self.route_segment_mapping9 = RouteSegmentMapping(
            route_id=4,
            segment_id=2,
            segment_sequence=3
        )

        self.ride1 = Ride(route_id=1, from_stop=1, destination_stop=7)
        self.ride2 = Ride(route_id=2, from_stop=1, destination_stop=7)
        self.ride3 = Ride(route_id=3, from_stop=1, destination_stop=7)
        self.ride4 = Ride(route_id=4, from_stop=2, destination_stop=5)
        self.ride4 = Ride(route_id=1, from_stop=1, destination_stop=7)

        self.ticket1 = Ticket(ride_id=1, from_stop=1,
                              destination_stop=7, created_ts='2013-01-01',
                              transaction_hash='test1', price=8.5)
        self.ticket2 = Ticket(ride_id=1, from_stop=5,
                              destination_stop=7, created_ts='2013-01-01',
                              transaction_hash='test2', price=8)
        self.ticket3 = Ticket(ride_id=1, from_stop=1,
                              destination_stop=5, created_ts='2013-01-01',
                              transaction_hash='test3', price=6.5)
        self.ticket4 = Ticket(ride_id=1, from_stop=2,
                              destination_stop=5, created_ts='2013-01-01',
                              transaction_hash='test4', price=3)
        self.ticket5 = Ticket(ride_id=2, from_stop=1,
                              destination_stop=7, created_ts='2013-01-01',
                              transaction_hash='test5', price=1.5)
        self.ticket6 = Ticket(ride_id=3, from_stop=1,
                              destination_stop=2, created_ts='2013-01-01',
                              transaction_hash='test6', price=2)
        self.ticket7 = Ticket(ride_id=3, from_stop=1,
                              destination_stop=4, created_ts='2013-01-01',
                              transaction_hash='test7', price=3)
        self.ticket8 = Ticket(ride_id=1, from_stop=1,
                              destination_stop=7, created_ts='2013-01-01',
                              transaction_hash='test8', price=8.5)

        for obj in [self.segment1, self.segment2, self.segment3,
                    self.segment4, self.segment5, self.segment6]:
            db.session.add(obj)

        for obj in [self.route1, self.route2, self.route3, self.route4]:
            db.session.add(obj)

        for obj in [self.route_segment_mapping1, self.route_segment_mapping2,
                    self.route_segment_mapping3, self.route_segment_mapping4,
                    self.route_segment_mapping5, self.route_segment_mapping6,
                    self.route_segment_mapping7, self.route_segment_mapping8,
                    self.route_segment_mapping9, self.route_segment_mapping10]:
            db.session.add(obj)

        db.session.flush()

        for obj in [self.ride1, self.ride2, self.ride3, self.ride4]:
            db.session.add(obj)

        for obj in [self.ticket1, self.ticket2, self.ticket3, self.ticket4,
                    self.ticket5, self.ticket6, self.ticket7, self.ticket8]:
            db.session.add(obj)

        db.session.commit()

    def test_get_ticket_list(self):
        resp = self.client.get('/ticket', headers=self.headers,
                               content_type='application/json')
        get_ride_response_data = json.loads(resp.data)
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(len(get_ride_response_data), 8)

    def test_post_ticket_list(self):
        ticket_body = {
            "ride_id": 1,
            "from_stop": 1,
            "destination_stop": 2,
            "transaction_hash": 'testhash'
        }
        resp = self.client.post('/ticket', headers=self.headers,
                                data=json.dumps(ticket_body),
                                content_type='application/json')
        self.assertEquals(resp.status_code, 201)
