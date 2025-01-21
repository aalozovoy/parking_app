import pytest
from app import create_app, db


@pytest.fixture
def app():
    """
    Фикстура для создания тестового приложения.
    """
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """
    Фикстура для создания тестового клиента.
    """
    return app.test_client()


@pytest.fixture
def db_session(app):
    """
    Фикстура для работы с базой данных.
    """
    with app.app_context():
        yield db.session