from flask import Flask, jsonify, request
from datetime import datetime
from . import db
from .models import Client, Parking, ClientParking


def register_routes(app: Flask) -> None:
    """
    Регистрация маршрутов API.

    :param app: Экземпляр Flask-приложения.
    """

    @app.route('/clients', methods=['GET'])
    def get_clients() -> tuple[str, int]:
        """
        Получить список всех клиентов.
        """
        clients = Client.query.all()
        return jsonify([{
            'id': c.id,
            'name': c.name,
            'surname': c.surname,
            'credit_card': c.credit_card,
            'car_number': c.car_number
        } for c in clients]), 200

    @app.route('/clients/<int:client_id>', methods=['GET'])
    def get_client(client_id: int) -> tuple[str, int]:
        """
        Получить информацию о клиенте по ID.
        """
        client = Client.query.get_or_404(client_id)
        return jsonify({
            'id': client.id,
            'name': client.name,
            'surname': client.surname,
            'credit_card': client.credit_card,
            'car_number': client.car_number
        }), 200

    @app.route('/clients', methods=['POST'])
    def create_client() -> tuple[str, int]:
        """
        Создать нового клиента.
        """
        data = request.json
        new_client = Client(
            name=data['name'],
            surname=data['surname'],
            credit_card=data.get('credit_card'),
            car_number=data.get('car_number')
        )
        db.session.add(new_client)
        db.session.commit()
        return jsonify({'id': new_client.id}), 201

    @app.route('/parkings', methods=['POST'])
    def create_parking() -> tuple[str, int]:
        """
        Создать новую парковочную зону.
        """
        data = request.json
        new_parking = Parking(
            address=data['address'],
            opened=data.get('opened', True),
            count_places=data['count_places'],
            count_available_places=data['count_places']
        )
        db.session.add(new_parking)
        db.session.commit()
        return jsonify({'id': new_parking.id}), 201

    @app.route('/client_parkings', methods=['POST'])
    def enter_parking() -> tuple[str, int]:
        """
        Заезд на парковку.
        """
        data = request.json
        client_id = data['client_id']
        parking_id = data['parking_id']

        # Проверка наличия клиента и парковки
        Client.query.get_or_404(client_id)
        parking = Parking.query.get_or_404(parking_id)

        # Проверка, открыта ли парковка и есть ли свободные места
        if not parking.opened:
            return jsonify({'error': 'Парковка закрыта'}), 400
        if parking.count_available_places <= 0:
            return jsonify({'error': 'Нет свободных мест на парковке'}), 400

        # Уменьшение количества свободных мест
        parking.count_available_places -= 1

        # Фиксация времени заезда
        new_log = ClientParking(
            client_id=client_id,
            parking_id=parking_id,
            time_in=datetime.now()
        )
        db.session.add(new_log)
        db.session.commit()

        return jsonify({'id': new_log.id}), 201

    @app.route('/client_parkings', methods=['DELETE'])
    def exit_parking() -> tuple[str, int]:
        """
        Выезд с парковки.
        """
        data = request.json
        client_id = data['client_id']
        parking_id = data['parking_id']

        # Поиск активного лога (без времени выезда)
        log = ClientParking.query.filter_by(
            client_id=client_id,
            parking_id=parking_id,
            time_out=None
        ).first_or_404()

        # Увеличение количества свободных мест
        parking = Parking.query.get_or_404(parking_id)
        parking.count_available_places += 1

        # Фиксация времени выезда
        log.time_out = datetime.now()
        db.session.commit()

        return '', 204