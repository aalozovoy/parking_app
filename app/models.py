from datetime import datetime
from sqlalchemy import UniqueConstraint
from . import db

class Client(db.Model):
    """
    Модель клиента.
    """
    __tablename__ = 'client'

    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(50), nullable=False)
    surname: str = db.Column(db.String(50), nullable=False)
    credit_card: str | None = db.Column(db.String(50), nullable=True)
    car_number: str | None = db.Column(db.String(10), nullable=True)

    def __repr__(self) -> str:
        return f'<Client {self.name} {self.surname}>'

class Parking(db.Model):
    """
    Модель парковки.
    """
    __tablename__ = 'parking'

    id: int = db.Column(db.Integer, primary_key=True)
    address: str = db.Column(db.String(100), nullable=False)
    opened: bool = db.Column(db.Boolean, default=True)
    count_places: int = db.Column(db.Integer, nullable=False)
    count_available_places: int = db.Column(db.Integer, nullable=False)

    def __repr__(self) -> str:
        return f'<Parking {self.address}>'

class ClientParking(db.Model):
    """
    Модель лога въезда-выезда на парковку.
    """
    __tablename__ = 'client_parking'

    id: int = db.Column(db.Integer, primary_key=True)
    client_id: int = db.Column(db.Integer, db.ForeignKey('client.id'))
    parking_id: int = db.Column(db.Integer, db.ForeignKey('parking.id'))
    time_in: datetime | None = db.Column(db.DateTime, nullable=True)
    time_out: datetime | None = db.Column(db.DateTime, nullable=True)

    # Уникальность пары (client_id, parking_id)
    __table_args__ = (
        UniqueConstraint('client_id', 'parking_id', name='unique_client_parking'),
    )

    # Связи
    client = db.relationship('Client', backref='parkings')
    parking = db.relationship('Parking', backref='clients')

    def __repr__(self) -> str:
        return f'<ClientParking {self.client_id} -> {self.parking_id}>'