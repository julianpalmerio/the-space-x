import requests
import json
from typing import List
import random

from exceptions.exeptions import GetMembersException, GetLabelsException, PostCardException
from models.card import CardModel


class TrelloConector():
    """Allows you to interact with the Trello API"""
    def __init__(self, key: str, token: str):
        self.__query = {"key": key, "token": token}
        self.__headers = {"Accept": "application/json"}

    def get_members(self, board_id: str) -> dict:
        """Obtain board members ids."""
        url = f"https://api.trello.com/1/boards/{board_id}/members"
        trello_response = requests.request(
            "GET",
            url,
            headers=self.__headers,
            params=self.__query
        )
        if trello_response.status_code == 200:
            response = json.loads(trello_response.text)
        else:
            message = f"status_code: {trello_response.status_code}, message: {trello_response.text}"
            raise GetMembersException(message)
        return response

    def get_label(self, board_id: str, label_name: str) -> List:
        """Gets the id of a label by name."""
        label_id = []
        if label_name is not None:
            url = f"https://api.trello.com/1/boards/{board_id}/labels"
            trello_response = requests.request(
                "GET",
                url,
                headers=self.__headers,
                params=self.__query
            )
            if trello_response.status_code == 200:
                response = json.loads(trello_response.text)
                label_id = [label["id"] for label in response if label["name"] == label_name]
            else:
                message = f"status_code: {trello_response.status_code}, message: {trello_response.text}"
                raise GetLabelsException(message)
        return label_id

    def post_card(self, card: CardModel, list_id: str, board_id: str) -> str:
        """"Post a card to a Trello board"""
        url = "https://api.trello.com/1/cards"
        query = self.__query.copy()
        query.update({
            'name': card.title,
            'description': card.description,
            'idList': list_id,
            'idLabels': self.get_label(board_id, card.label_name)
            })
        query['idLabels'].extend(self.get_label(board_id, card.category))
        if card.random_member:
            members = self.get_members(board_id)
            random_member = members[random.randint(0, len(members) - 1)]
            query['idMembers'] = random_member["id"]
        trello_response = requests.request(
            "POST",
            url,
            headers=self.__headers,
            params=query
            )
        if trello_response.status_code == 200:
            card = card.json(exclude_none=True)
        else:
            message = f"status_code: {trello_response.status_code}, message: {trello_response.text}"
            raise PostCardException(message)
        return card
