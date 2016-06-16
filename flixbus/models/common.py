from app import db


class Segment(db.Model):
    __tablename__ = 'flb_segment'
    __table_args__ = (
        db.Index(
            'idx_flb_from_stop_destination_stop', 'from_stop',
            'destination_stop'
        ),
    )

    id = db.Column(
        db.BigInteger, primary_key=True, autoincrement=True
    )
    from_stop = db.Column(db.Integer)
    destination_stop = db.Column(db.Integer)
    distance = db.Column(db.Float(53))
    created_ts = db.Column(db.DateTime(True), server_default=db.text("now()"))
    update_ts = db.Column(db.DateTime(True), server_default=db.text("now()"))
    is_active = db.Column(db.Boolean, server_default=db.text("true"))
    pax_count = db.Column(db.Integer, nullable=True)
    revenue = db.Column(db.Float, nullable=True)
#   route_segment_mappings = db.relationship('RouteSegmentMapping',
#                                            back_populates='segment',
#                                            lazy='joined')

    def __repr__(self):
        return ('Segment(id={segment_id}, from_stop={from_stop}, '
                'destination_stop={destination_stop}, distance={distance})'
                .format(segment_id=self.id,
                        from_stop=self.from_stop,
                        destination_stop=self.destination_stop,
                        distance=self.distance))


class Route(db.Model):
    __tablename__ = 'flb_route'
    id = db.Column(
        db.BigInteger, primary_key=True
    )
    created_ts = db.Column(db.DateTime(True), server_default=db.text("now()"))
#   rides = db.relationship('Ride', back_populates='route', lazy='joined')


class RouteSegmentMapping(db.Model):
    __tablename__ = 'flb_route_segment_mapping'
    id = db.Column(
        db.BigInteger, primary_key=True
    )
    route_id = db.Column(db.ForeignKey(u'flb_route.id'), nullable=False,
                         index=True)
    segment_id = db.Column(db.ForeignKey(u'flb_segment.id'), nullable=False,
                           index=True)
    segment_sequence = db.Column(db.Integer)
    segment = db.relationship(u'Segment')
#   route = db.relationship(u'Route')


class Ride(db.Model):
    __tablename__ = 'flb_ride'

    id = db.Column(
        db.BigInteger, primary_key=True
    )
    from_stop = db.Column(db.Integer)
    destination_stop = db.Column(db.Integer)
    route_id = db.Column(db.ForeignKey(u'flb_route.id'), index=True)
#   route = db.relationship(u'Route')
#   tickets = db.relationship('Ticket', back_populates='ride',
#                             lazy='joined')
