import requests

from flask import request
from flask_restx import Namespace, Resource

api = Namespace("cards", "Allows you to interact with Trello cards")


class Card(Resource):
    def post(self):
        data = request.get_json()
        try:
            type = data["type"]
            title = data["title"]
            description = data["description"]
        except KeyError:
            return {}, 400
        url = "https://api.trello.com/1/cards"
        headers = {
            "Accept": "application/json"
            }
        query = {
            'name': title,
            'description': description,
            'idList': '628c1cfd6595cd86a2a5af95',
            'key': 'b9be662af7fd7fa6cc4e31df81f53ca5',
            'token': 'bfe85944cab9a57dd7def1cb103a38d0b7766e655270f48a61f2838300c7b45a'
            }
        trello_response = requests.request(
            "POST",
            url,
            headers=headers,
            params=query
            )
        if trello_response.status_code == 200:
            return {}, 200
        else:
            return {}, 400


api.add_resource(Card, "/card")
