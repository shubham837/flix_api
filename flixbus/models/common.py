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


class Ride(db.Model):
    __tablename__ = 'flb_ride'

    id = db.Column(
        db.BigInteger, primary_key=True
    )
    from_stop = db.Column(db.Integer)
    destination_stop = db.Column(db.Integer)
    route_id = db.Column(db.ForeignKey(u'flb_route.id'), index=True)


class Ticket(db.Model):
    __tablename__ = 'flb_ticket'

    id = db.Column(
        db.BigInteger, primary_key=True
    )
    ride_id = db.Column(db.ForeignKey(u'flb_ride.id'), nullable=True,
                        index=True)
    from_stop = db.Column(db.Integer)
    destination_stop = db.Column(db.Integer)
    description = db.Column(db.Text)
    transaction_hash = db.Column(db.Text)
    price = db.Column(db.Float(53))
    # currently created_ts is considered as date of journey
    # ideally it should be different date
    created_ts = db.Column(db.DateTime(True), server_default=db.text("now()"))
    ride = db.relationship(u'Ride')