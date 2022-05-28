import os
from os import path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Base config."""
    DEBUG = False
    TESTING = False
    RESTX_ERROR_404_HELP = False
    RESTX_MASK_SWAGGER = False
    TRELLO_KEY = os.environ.get("TRELLO_KEY")
    TRELLO_TOKEN = os.environ.get("TRELLO_TOKEN")
    TRELLO_BOARD_ID = os.environ.get("TRELLO_BOARD_ID")
    TRELLO_TODO_LIST_ID = os.environ.get("TRELLO_TODO_LIST_ID")


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
