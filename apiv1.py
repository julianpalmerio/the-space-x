from flask import Blueprint
from flask_restx import Api

from namespaces.cards.cards import api as nscards

blueprint_api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')
api = Api(
    blueprint_api_v1,
    title='The Space X',
    version='1.0',
    description='The Space X API 1.0',
)

api.add_namespace(nscards)
