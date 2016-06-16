from models.common import Route, Ride, RouteSegmentMapping
from app import db
import errors
from sqlalchemy.orm.exc import NoResultFound


class RouteBaseController(object):

    def __init__(self, is_delete=False, data={}, metadata={}):
        self.user_id = metadata.get('user_id')
        self.is_delete = is_delete
        if is_delete or data:
            self.route_data = data
            self.serializable_data = self._write()
        else:
            self.serializable_data = self._fetch()
        if self.serializable_data is None:
            raise errors.NotSerializable()

    def serialize(self, serializable_data):
        route_responses = {}
        for route in serializable_data:
            segment = {
                'segment_id': route.segment_id,
                'segment_sequence': route.segment_sequence
            }
            if route.route_id in route_responses:
                route_response = route_responses.get(route.route_id)
                segment_list = route_response.get('segments')
                segment_list.append(segment)
            else:
                segment_list = [segment]
                route_response = {
                    'route_id': route.route_id,
                    'segments': segment_list
                }
                route_responses[route.route_id] = route_response

        serialized_route = [route_resp for route_id, route_resp in
                            route_responses.iteritems()]
        return serialized_route

    @property
    def serialized_repr(self):
        if isinstance(self.serializable_data, list):
            return self.serialize(self.serializable_data)
        elif isinstance(self.serializable_data, dict):
            return self.serializable_data
        raise errors.NotSerializable(
            "No serializable data found associated to the controller"
        )

    @classmethod
    def close_session(cls):
        '''Close the current db session.'''
        db.session.close()


class RideBaseController(object):

    def __init__(self, is_delete=False, data={}, metadata={}):
        self.user_id = metadata.get('user_id')
        self.is_delete = is_delete
        if is_delete or data:
            self.ride = data
            self.serializable_data = self._write()
        else:
            self.serializable_data = self._fetch()
        if self.serializable_data is None:
            raise errors.NotSerializable()

    def serialize(self, serializable_data):
        '''Return a serialized representation of the Segment object.'''
        serialized_ride = {
            'id': serializable_data.id,
            'from_stop': serializable_data.from_stop,
            'destination_stop': serializable_data.destination_stop,
            'route_id': serializable_data.route_id,
        }
        return serialized_ride

    @property
    def serialized_repr(self):
        if isinstance(self.serializable_data, list):
            return [self.serialize(data) for data in self.serializable_data]
        elif isinstance(self.serializable_data, Ride):
            return self.serialize(self.serializable_data)
        elif isinstance(self.serializable_data, dict):
            return self.serialize(self.serializable_data)
        raise errors.NotSerializable(
            "No serializable data found associated to the controller"
        )

    @classmethod
    def close_session(cls):
        '''Close the current db session.'''
        db.session.close()


class RouteListController(RouteBaseController):

    def _fetch(self, **kwargs):
        filters = dict(kwargs)
        routes = RouteSegmentMapping.query.filter_by(**filters).all()
        return [route for route in routes]

    def _write(self):
        route_segments = self.route_data.get('route_segments')
        route_segment_mappings = []
        for route_segment in route_segments:
            route_object = Route()
            db.session.add(route_object)
            db.session.flush()
            route_segment_mapping = RouteSegmentMapping(
                segment_id=route_segment.get('segment_id'),
                segment_sequence=route_segment.get('segment_sequence'),
                route_id=route_object.id
            )
            db.session.add(route_segment_mapping)
            route_segment_mappings.append(route_segment_mapping)
        db.session.commit()
        return route_segment_mappings


class RouteDetailController(RouteBaseController):
    def __init__(self, route_id, *args, **kwargs):
        self.route_id = route_id
        self.data = kwargs.get('data')
        super(RouteDetailController, self).__init__(*args, **kwargs)

    def _fetch(self):
        try:
            route_objects = RouteSegmentMapping.query.filter_by(
                route_id=self.route_id).all()
        except NoResultFound:
            raise errors.APIException(404, "Route not found")

        segments = []
        for route_object in route_objects:
            segment = {
                'segment_id': route_object.segment_id,
                'segment_sequence': route_object.segment_sequence
            }
            segments.append(segment)

        route_response = {
            'route_id': self.route_id,
            'segments': segments
        }
        return route_response

    def _write(self):
        try:
            route_objects = RouteSegmentMapping.query.filter_by(
                id=self.route_id
            ).all()
        except NoResultFound:
            raise errors.APIException(404, "Route not found")
        for route_object in route_objects:
            db.session.delete(route_object)
        db.session.commit()
        updated_route_object = {}
        route_segment_mappings = []
        if not self.is_delete:
            route_segments = self.route_data.get('route_segments')
            for route_segment in route_segments:
                route_object = Route()
                db.session.add(route_object)
                db.session.flush()
                route_segment_mapping = RouteSegmentMapping(
                    segment_id=route_segment.get('segment_id'),
                    segment_sequence=route_segment.get('segment_sequence'),
                    route_id=route_object.id
                )
                db.session.add(route_segment_mapping)
                route_segment_mappings.append(route_segment_mapping)
            db.session.commit()
            return route_segment_mappings

        return updated_route_object


class RideListController(RideBaseController):
    def __init__(self, route_id, *args, **kwargs):
        self.route_id = route_id
        super(RideListController, self).__init__(*args, **kwargs)

    def _fetch(self, **kwargs):
        rides = Ride.query.filter_by(route_id=self.route_id).all()
        return [ride for ride in rides]

    def _write(self):
        ride_object = Ride(**self.ride)
        db.session.add(ride_object)
        db.session.commit()
        return ride_object


class RideDetailController(RideBaseController):
    def __init__(self, route_id, ride_id, *args, **kwargs):
        self.route_id = route_id
        self.ride_id = ride_id
        super(RideDetailController, self).__init__(*args, **kwargs)

    def _fetch(self):
        try:
            ride_object = Ride.query.filter_by(
                id=self.ride_id, route_id=self.route_id
            ).one()
        except NoResultFound:
            raise errors.APIException(404, "Ride not found")
        return ride_object

    def _write(self):
        try:
            ride_object = Ride.query.filter_by(
                id=self.ride_id, route_id=self.route_id
            ).one()
        except NoResultFound:
            raise errors.APIException(
                404, "Ride not found"
            )
        db.session.delete(ride_object)
        if not self.is_delete:
            self.ride['id'] = self.ride_id
            updated_ride_object = Ride(**self.ride)
            db.session.add(updated_ride_object)
            db.session.commit()
            return updated_ride_object
