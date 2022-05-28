from flask import request
from flask_restx import Namespace, Resource, fields
from pydantic import ValidationError

from models import factory
from models.card import IssueCardModel, BugCardModel, TaskCardModel
from .service.trello_conector import TrelloConector

api = Namespace("cards", "Allows you to interact with Trello cards")

factory.register("issue", IssueCardModel)
factory.register("bug", BugCardModel)
factory.register("task", TaskCardModel)

body_issue_card_post = api.model("BodyIssueCardPost", {
    "type": fields.String(example="issue", required=True),
    "title": fields.String(example="Send message"),
    "description": fields.String(example="Let pilots send messages to Central"),
    "category": fields.String(example="Maintenance")
}, strict=True)


class Card(Resource):
    @api.expect(body_issue_card_post, description='Post a card on trello board', validate=True)
    def post(self):
        '''
        Post a card on trello board.
        '''
        data = request.get_json()
        try:
            card = factory.create(data)
        except ValueError or ValidationError:
            return {}, 400
        board_id = "628c1cfd6595cd86a2a5af94"
        list_id = "628c1cfd6595cd86a2a5af95"
        key = "b9be662af7fd7fa6cc4e31df81f53ca5"
        token = "bfe85944cab9a57dd7def1cb103a38d0b7766e655270f48a61f2838300c7b45a"
        trello_conector = TrelloConector(key, token)
        result = trello_conector.post_card(card, list_id, board_id)
        return {"card": result}, 200


api.add_resource(Card, "/card")
