class DefaultConfig:
    """
    Конфигурация по умолчанию.
    """

    SQLALCHEMY_DATABASE_URI = "sqlite:///parking.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
