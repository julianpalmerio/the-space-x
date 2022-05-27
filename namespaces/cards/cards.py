import requests

from flask import request
from flask_restx import Namespace, Resource, fields
from pydantic import ValidationError

from models.card import IssueCardModel

api = Namespace("cards", "Allows you to interact with Trello cards")

body_issue_card_post = api.model("BodyIssueCardPost", {
    "type": fields.String(example="issue", required=True),
    "title": fields.String(example="Send message"),
    "description": fields.String(example="Let pilots send messages to Central")
}, strict=True)


class Card(Resource):
    @api.expect(body_issue_card_post, description='Post a card on trello board', validate=True)
    def post(self):
        '''
        Post a card on trello board.
        '''
        data = request.get_json()
        if data["type"] == "issue":
            try:
                card = IssueCardModel(**data)
            except ValidationError:
                return {}, 400
        else:
            return {}, 400
        url = "https://api.trello.com/1/cards"
        headers = {
            "Accept": "application/json"
            }
        query = {
            'name': card.title,
            'description': card.description,
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
            return {"card": card.json()}, 200


api.add_resource(Card, "/card")
