from marshmallow import (Schema, fields, validates_schema, ValidationError)
from marshmallow.utils import get_value


# Adds Werkzeug MultiDict in fields.List
class MultiDictFieldMixin(object):
    def get_attribute(self, attr, obj, default):
        field = self.fields.get(attr)
        if field:
            metadata = field.metadata
            if (metadata and metadata.get('is_multidict', False) and
                    isinstance(obj, dict) and hasattr(obj, 'getlist')):
                return obj.getlist(attr)
        return get_value(attr, obj, default)


class BaseHeadersSchema(MultiDictFieldMixin, Schema):
    user = fields.Int(required=True, dump_to='user_id')
    app_client = fields.Str(required=True, dump_to='source')


class SegmentExtraFieldsSchema(Schema):
    get_pax = fields.Bool()
    get_revenue = fields.Bool()
    start = fields.Int(default=0, dump_to='start')
    limit = fields.Int(default=20, dump_to='limit')
    from_stop = fields.Int()
    destination_stop = fields.Int()
    distance = fields.Float()


class RouteExtraFieldsSchema(Schema):
    start = fields.Int(default=0, dump_to='start')
    limit = fields.Int(default=20, dump_to='limit')
    segment_id = fields.List(fields.Int)


class RideExtraFieldsSchema(Schema):
    start = fields.Int(default=0, dump_to='start')
    limit = fields.Int(default=20, dump_to='limit')
    from_stop = fields.Int()
    destination_stop = fields.Int()


class TicketExtraFieldsSchema(Schema):
    start = fields.Int(default=0, dump_to='start')
    limit = fields.Int(default=20, dump_to='limit')
    transaction_hash = fields.Str()
    from_stop = fields.Int()
    destination_stop = fields.Int()


class SegmentHeadersSchema(BaseHeadersSchema, SegmentExtraFieldsSchema):
    pass


class RouteHeadersSchema(BaseHeadersSchema, RouteExtraFieldsSchema):
    pass


class RideHeadersSchema(BaseHeadersSchema,RideExtraFieldsSchema):
    pass


class TicketHeadersSchema(BaseHeadersSchema, TicketExtraFieldsSchema):
    pass


class SegmentBodySchema(Schema):
    from_stop = fields.Int(required=True, dump_to='from_stop')
    destination_stop = fields.Int(required=True, dump_to='destination_stop')
    distance = fields.Float(dump_to='distance')
    is_active = fields.Bool(dump_to='is_active')


class RouteSegmentSchema(Schema):
    segment_id = fields.Int(required=True)
    segment_sequence = fields.Int(required=True)


class RouteBodySchema(Schema):
    route_segments = fields.List(fields.Dict, required=True,
                                 dump_to='route_segments')

    @validates_schema
    def validate_route_segments(self, data):
        route_segment_schema = RouteSegmentSchema(strict=True)
        try:
            data_segments = data.get('route_segments')
            if not isinstance(data_segments, list) or not data_segments:
                raise ValidationError('segments should be of non empty list '
                                      'type')
            for data_segment in data_segments:
                if data_segment == {}:
                    raise ValidationError('empty segment passed')
                route_segment_schema.validate(data_segment)
        except KeyError as error:
            message = ' '.join([
                '\'{key}\' key required when'.format(key=error.message),
                'creating routes'
            ])
            raise ValidationError(message)


class RideBodySchema(Schema):
    route_id = fields.Int(required=True, dump_to='route_id')
    from_stop = fields.Int(required=True, dump_to='to_stop')
    destination_stop = fields.Int(required=True, dump_to='destination_stop')


class TicketBodySchema(Schema):
    ride_id = fields.Int(required=False, dump_to='ride_id')
    from_stop = fields.Int(dump_to='to_stop')
    destination_stop = fields.Int(dump_to='destination_stop')
    date = fields.Date(dump_to='date')
    description = fields.Str(dump_to='description')
    transaction_hash = fields.Str(dump_to='transaction_hash')
    price = fields.Float(dump_to='price')
