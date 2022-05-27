import requests
import json
import random

from flask import request
from flask_restx import Namespace, Resource, fields
from pydantic import ValidationError

from models import factory
from models.card import IssueCardModel, BugCardModel, TaskCardModel

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


def get_label(label_name):
    """Gets the id of a label by name."""
    if label_name is not None:
        board_id = '628c1cfd6595cd86a2a5af94'
        url = f"https://api.trello.com/1/boards/{board_id}/labels"
        headers = {
                "Accept": "application/json"
                }
        query = {
            'key': 'b9be662af7fd7fa6cc4e31df81f53ca5',
            'token': 'bfe85944cab9a57dd7def1cb103a38d0b7766e655270f48a61f2838300c7b45a'
            }
        trello_response = requests.request(
            "GET",
            url,
            headers=headers,
            params=query
            )
        response_json = json.loads(trello_response.text)
        label_id = [label["id"] for label in response_json if label["name"] == label_name]
        return label_id
    else:
        return []


def get_members():
    """Obtain board members ids."""
    board_id = '628c1cfd6595cd86a2a5af94'
    url = f"https://api.trello.com/1/boards/{board_id}/members"
    headers = {
            "Accept": "application/json"
            }
    query = {
        'key': 'b9be662af7fd7fa6cc4e31df81f53ca5',
        'token': 'bfe85944cab9a57dd7def1cb103a38d0b7766e655270f48a61f2838300c7b45a'
        }
    trello_response = requests.request(
        "GET",
        url,
        headers=headers,
        params=query
        )
    response_json = json.loads(trello_response.text)
    return response_json


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
        url = "https://api.trello.com/1/cards"
        headers = {
            "Accept": "application/json"
            }
        query = {
            'name': card.title,
            'description': card.description,
            'idList': '628c1cfd6595cd86a2a5af95',
            'key': 'b9be662af7fd7fa6cc4e31df81f53ca5',
            'token': 'bfe85944cab9a57dd7def1cb103a38d0b7766e655270f48a61f2838300c7b45a',
            'idLabels': get_label(card.label_name)
            }
        query['idLabels'].extend(get_label(card.category))
        if card.random_member:
            members = get_members()
            random_member = members[random.randint(0, len(members) - 1)]
            query['idMembers'] = random_member["id"]
        trello_response = requests.request(
            "POST",
            url,
            headers=headers,
            params=query
            )
        if trello_response.status_code == 200:
            return {"card": card.json(exclude_none=True)}, 200


api.add_resource(Card, "/card")
