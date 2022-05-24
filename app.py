import os

from dotenv import load_dotenv
from flask import Flask

from apiv1 import blueprint_api_v1

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


def create_app():
    app = Flask(__name__)
    if os.environ.get("ENV") == "production":
        app.config.from_object("config.ProductionConfig")
    else:
        app.config.from_object("config.DevelopmentConfig")
    app.register_blueprint(blueprint_api_v1)
    return app


app = create_app()

if __name__ == '__main__':
    app.run()
