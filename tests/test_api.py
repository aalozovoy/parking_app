import pytest
from datetime import datetime
from tests.factories import ClientFactory, ParkingFactory
from app.models import Client, Parking, ClientParking


def test_get_clients(client, db_session):
    """
    Тест для получения списка клиентов.
    """
    # Создаем тестового клиента с помощью фабрики
    test_client = ClientFactory()
    db_session.commit()

    # Выполняем запрос
    response = client.get('/clients')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['name'] == test_client.name


def test_create_client(client, db_session):
    """
    Тест для создания клиента.
    """
    data = {
        "name": "Петр",
        "surname": "Петров",
        "credit_card": "9876-5432-1098-7654",
        "car_number": "B456CD"
    }
    response = client.post('/clients', json=data)
    assert response.status_code == 201
    assert response.json['id'] == 1

    # Проверяем, что клиент добавлен в базу
    client_in_db = db_session.get(Client, 1)
    assert client_in_db.name == "Петр"


def test_create_parking(client, db_session):
    """
    Тест для создания парковки.
    """
    data = {
        "address": "ул. Пушкина, 15",
        "count_places": 100
    }
    response = client.post('/parkings', json=data)
    assert response.status_code == 201
    assert response.json['id'] == 1

    # Проверяем, что парковка добавлена в базу
    parking_in_db = db_session.get(Parking, 1)
    assert parking_in_db.address == "ул. Пушкина, 15"


@pytest.mark.parking
def test_enter_parking(client, db_session):
    """
    Тест для заезда на парковку.
    """
    # Создаем клиента и парковку с помощью фабрик
    test_client = ClientFactory()
    test_parking = ParkingFactory()
    db_session.commit()

    # Выполняем запрос на заезд
    data = {
        "client_id": test_client.id,
        "parking_id": test_parking.id
    }
    response = client.post('/client_parkings', json=data)
    assert response.status_code == 201
    assert response.json['id'] == 1

    # Проверяем, что количество свободных мест уменьшилось
    parking_in_db = db_session.get(Parking, test_parking.id)
    assert parking_in_db.count_available_places == test_parking.count_places - 1


@pytest.mark.parking
def test_exit_parking(client, db_session):
    """
    Тест для выезда с парковки.
    """
    # Создаем клиента, парковку и лог заезда с помощью фабрик
    test_client = ClientFactory()
    test_parking = ParkingFactory(count_available_places=49)
    test_log = ClientParking(
        client_id=test_client.id,
        parking_id=test_parking.id,
        time_in=datetime.now()
    )
    db_session.add(test_log)
    db_session.commit()

    # Выполняем запрос на выезд
    data = {
        "client_id": test_client.id,
        "parking_id": test_parking.id
    }
    response = client.delete('/client_parkings', json=data)
    assert response.status_code == 204

    # Проверяем, что количество свободных мест увеличилось
    parking_in_db = db_session.get(Parking, test_parking.id)
    assert parking_in_db.count_available_places == 50
