import os
from dotenv import load_dotenv

load_dotenv(override=False)


class Config:
    """Configuration de base."""

    # MongoDB
    MONGODB_HOST = os.environ.get("MONGODB_HOST", "mongodb")
    MONGODB_PORT = int(os.environ.get("MONGODB_PORT", 27017))
    MONGODB_DATABASE = os.environ.get("MONGODB_DATABASE", "sales_db")
    MONGODB_COLLECTION = "sales_madrid"
    MONGODB_USERNAME = os.environ.get("MONGODB_USERNAME")
    MONGODB_PASSWORD = os.environ.get("MONGODB_PASSWORD")


class DevelopmentConfig(Config):
    """Configuration pour le développement."""

    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """Configuration pour les tests."""

    TESTING = True
    DEBUG = True

    # Base de données séparée pour les tests
    MONGODB_DATABASE = os.environ.get("MONGODB_TEST_DATABASE", "sales_test")
    MONGODB_COLLECTION = "sales_madrid_test"


class ProductionConfig(Config):
    """Configuration pour la production."""

    DEBUG = False
    TESTING = False
    # Ajouter d'autres configs prod (HTTPS, logging, etc.)


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
