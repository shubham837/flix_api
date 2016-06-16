from models.common import Segment
from app import db
import errors
from sqlalchemy.orm.exc import NoResultFound
from segment_utils import SegmentUtils


class SegmentBaseController(object):

    def __init__(self, is_delete=False, data={}, metadata={}):
        self.user_id = metadata.get('user_id')

        self.start = metadata.get('start')
        self.limit = metadata.get('limit')
        self.get_pax = metadata.get('get_pax')
        self.get_revenue = metadata.get('get_revenue')

        filters = {}
        if 'from_stop' in metadata:
            self.filters['from_stop'] = metadata.get('from_stop')
        if 'destination_stop' in metadata:
            self.filters['destination_stop'] = metadata.get('destination_stop')
        if 'distance' in metadata:
            self.filters['distance'] = metadata.get('distance')

        self.is_delete = is_delete
        if is_delete or data:
            self.segment = data
            self.serializable_data = self._write()
        else:
            self.serializable_data = self._fetch(filters)

        if self.serializable_data is None:
            raise errors.NotSerializable()

    def serialize(self, serializable_data):
        serialized_segment = {
            'id': serializable_data.id,
            'from_stop': serializable_data.from_stop,
            'destination_stop': serializable_data.destination_stop,
            'distance': serializable_data.distance,
            'is_active': serializable_data.is_active
        }
        return serialized_segment

    @property
    def serialized_repr(self):
        if isinstance(self.serializable_data, list):
            return [self.serialize(data) for data in self.serializable_data]
        elif isinstance(self.serializable_data, Segment):
            return self.serialize(self.serializable_data)
        elif isinstance(self.serializable_data, dict):
            return self.serialize(self.serializable_data)
        raise errors.NotSerializable(
            "No serializable data found associated to the controller"
        )

    @classmethod
    def close_session(cls):
        db.session.close()


class SegmentListController(SegmentBaseController):

    def _fetch(self, filters):
        segments = Segment.query.filter_by(**filters).all()
        return [segment for segment in segments]

    def _write(self):
        segment_object = Segment(**self.segment)
        db.session.add(segment_object)
        db.session.commit()
        return segment_object


class SegmentDetailController(SegmentBaseController):
    def __init__(self, segment_id, *args, **kwargs):
        self.segment_id = segment_id
        self.data = kwargs.get('data')
        super(SegmentDetailController, self).__init__(*args, **kwargs)

    def _fetch(self, filters):
        try:
            segment_object = Segment.query.filter_by(
                id=self.segment_id, **filters
            ).one()
        except NoResultFound:
            raise errors.APIException(404, "Segment not found")
        if self.get_pax or segment_object.revenue:
            # TODO: Currently only current segment object is checked,
            # later going route service and ticket service will be
            # called to check if new routes or tickets added for segment
            if not (segment_object.pax_count and segment_object.revenue):
                pax_count, segment_revenue = \
                    SegmentUtils.get_passengers_count_and_revenue(
                        self.segment_id)
                segment_object.pax_count = pax_count
                segment_object.segment_revenue = segment_revenue
                db.session.add(segment_object)
                db.session.commit()
        return segment_object

    def _write(self):
        try:
            segment_object = Segment.query.filter_by(
                id=self.segment_id
            ).one()
        except NoResultFound:
            raise errors.APIException(
                404, "Segment not found"
            )
        db.session.delete(segment_object)
        if not self.is_delete:
            self.segment['id'] = self.segment_id
            updated_segment_object = Segment(**self.segment)
            db.session.add(updated_segment_object)

        db.session.commit()
        return updated_segment_object
