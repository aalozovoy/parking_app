from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Инициализация SQLAlchemy с указанием типа
db: SQLAlchemy = SQLAlchemy()


def create_app(config_var: str = "default") -> Flask:
    """
    Фабрика для создания Flask-приложения.

    :param config_var: Название конфигурации (по умолчанию 'default').
    :return: Экземпляр Flask-приложения.
    """
    app = Flask(__name__)

    # Загрузка конфигурации
    app.config.from_object(f"app.config.{config_var.capitalize()}Config")

    # Инициализация базы данных
    db.init_app(app)

    # Регистрация маршрутов
    from .routes import register_routes

    register_routes(app)

    return app
