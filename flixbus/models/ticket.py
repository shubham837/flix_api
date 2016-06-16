from app import db


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
