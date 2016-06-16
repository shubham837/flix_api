from models.common import Ticket
from app import db
import errors
from sqlalchemy.orm.exc import NoResultFound


class TicketBaseController(object):

    def __init__(self, is_delete=False, data={}, metadata={}):
        self.user_id = metadata.get('user_id')
        self.is_delete = is_delete
        if is_delete or data:
            self.ticket = data
            self.serializable_data = self._write()
        else:
            self.serializable_data = self._fetch()
        if self.serializable_data is None:
            raise errors.NotSerializable()

    def serialize(self, serializable_data):
        serialized_ticket = {
            'id': serializable_data.id,
            'from_stop': serializable_data.from_stop,
            'destination_stop': serializable_data.destination_stop,
            'ride_id': serializable_data.ride_id,
            'description': serializable_data.description,
            'transaction_hash': serializable_data.transaction_hash,
            'price': serializable_data.price
        }
        return serialized_ticket

    @property
    def serialized_repr(self):
        if isinstance(self.serializable_data, list):
            return [self.serialize(data) for data in self.serializable_data]
        elif isinstance(self.serializable_data, Ticket):
            return self.serialize(self.serializable_data)
        elif isinstance(self.serializable_data, dict):
            return self.serialize(self.serializable_data)
        raise errors.NotSerializable(
            "No serializable data found associated to the controller"
        )

    @property
    def get_total_passengers(self):
        return int(sum(
            ticket['price'] * ticket['quantity'] for ticket in
            self.serializable_data['ticket']
        ))

    @classmethod
    def close_session(cls):
        db.session.close()


class TicketListController(TicketBaseController):

    def _fetch(self, **kwargs):
        filters = dict(kwargs)
        tickets = Ticket.query.filter_by(**filters).all()
        return [ticket for ticket in tickets]

    def _write(self):
        ticket_object = Ticket(**self.ticket)
        db.session.add(ticket_object)
        db.session.commit()
        return ticket_object


class TicketDetailController(TicketBaseController):
    def __init__(self, ticket_id, *args, **kwargs):
        self.ticket_id = ticket_id
        self.data = kwargs.get('data')
        super(TicketDetailController, self).__init__(*args, **kwargs)

    def _fetch(self):
        try:
            ticket_object = Ticket.query.filter_by(
                id=self.ticket_id
            ).one()
        except NoResultFound:
            raise errors.APIException(404, "Ticket not found")
        return ticket_object

    def _write(self):
        try:
            ticket_object = Ticket.query.filter_by(
                id=self.ticket_id
            ).one()
        except NoResultFound:
            raise errors.APIException(
                404, "Ticket not found"
            )
        db.session.delete(ticket_object)
        if not self.is_delete:
            self.ticket['id'] = self.ticket_id
            updated_ticket_object = Ticket(**self.ticket)
            db.session.add(updated_ticket_object)
            db.session.commit()
            return updated_ticket_object
