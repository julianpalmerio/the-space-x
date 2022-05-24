from os import path
from dotenv import load_dotenv


class Config:
    """Base config."""
    DEBUG = False
    TESTING = False
    ERROR_404_HELP = False
    RESTX_MASK_SWAGGER = False


class ProductionConfig(Config):
    FLASK_ENV = "production"
    ENV = "production"


class DevelopmentConfig(Config):
    FLASK_ENV = "development"
    ENV = "development"
    DEBUG = True


class TestingConfig(Config):
    FLASK_ENV = "testing"
    ENV = "testing"
    TESTING = True
