from flask import request, current_app
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
        board_id = current_app.config["TRELLO_BOARD_ID"]
        list_id = current_app.config["TRELLO_TODO_LIST_ID"]
        trello_key = current_app.config["TRELLO_KEY"]
        trello_token = current_app.config["TRELLO_TOKEN"]
        trello_conector = TrelloConector(trello_key, trello_token)
        result = trello_conector.post_card(card, list_id, board_id)
        return {"card": result}, 200


api.add_resource(Card, "/card")
