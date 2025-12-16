import os
from dotenv import load_dotenv
load_dotenv()


class Config:
    """Configuration de base."""
    MONGODB_SETTINGS = {
        'db': 'sales',
        'collection': 'sales_madrid',
        'host': os.environ.get('MONGODB_HOST') or 'mongodb',
        'port': os.environ.get('MONGODB_PORT') or 27017,
        'username': os.environ.get('MONGODB_USERNAME'),
        'password': os.environ.get('MONGODB_PASSWORD')
    }


class DevelopmentConfig(Config):
    DEBUG = True
    MONGODB_SETTINGS = {
        **Config.MONGODB_SETTINGS
    }


class TestingConfig(Config):
    """Configuration pour les tests."""
    TESTING = True
    MONGODB_SETTINGS = {
        **Config.MONGODB_SETTINGS,
        'db': 'sales_test',
        'collection': 'sales_madrid_test'
    }


config = {
    'testing': TestingConfig,
    'default': Config,
    'development': DevelopmentConfig
}
