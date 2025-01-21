import factory
import factory.fuzzy
from faker import Faker
from app.models import Client, Parking
from app import db

fake = Faker()


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    """
    Фабрика для создания клиентов.
    """
    class Meta:
        model = Client
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    name = factory.Faker("first_name")
    surname = factory.Faker("last_name")
    credit_card = factory.Faker("credit_card_number")
    car_number = factory.Faker("license_plate")


class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    """
    Фабрика для создания парковок.
    """
    class Meta:
        model = Parking
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    address = factory.Faker("street_address")
    count_places = factory.fuzzy.FuzzyInteger(10, 100)
    count_available_places = factory.SelfAttribute("count_places")
