import json

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
        api.logger.debug("Processing Card Post Request")
        data = request.get_json()
        api.logger.debug(f"Request Payload: {data}")
        try:
            card = factory.create(data)
            api.logger.debug(f"Factory.create result: {card.json()}")
        except ValueError or ValidationError as ex:
            api.logger.exception("An error occurred while loading the card model")
            return {"message": str(ex)}, 400
        board_id = current_app.config["TRELLO_BOARD_ID"]
        list_id = current_app.config["TRELLO_TODO_LIST_ID"]
        trello_key = current_app.config["TRELLO_KEY"]
        trello_token = current_app.config["TRELLO_TOKEN"]
        try:
            trello_conector = TrelloConector(trello_key, trello_token)
            api.logger.debug("Instanced trello connector")
            result = trello_conector.post_card(card, list_id, board_id)
            api.logger.debug(f"Successfully published card, result: {result}")
        except Exception as ex:
            api.logger.exception("An error occurred")
            raise ex
        return {"card": json.loads(result)}, 200


api.add_resource(Card, "/card")
