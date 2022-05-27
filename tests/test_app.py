import json


def test_issue_card_ok(client):
    """
    Test if the request is ok if it receives the issue type, title and description.
    """
    data_json = {"type": "issue", "title": "Send message", "description": "Let pilots send messages to Central"}
    response = client.post("api/v1/cards/card", json=data_json)
    assert response.status_code == 200
    card = json.loads(response.json["card"])
    assert card == data_json


def test_issue_card_fail_miss_title(client):
    """
    Test if the request fails if it receives the issue type and description.
    """
    data_json = {"type": "issue", "description": "Let pilots send messages to Central"}
    response = client.post("api/v1/cards/card", json=data_json)
    assert response.status_code == 400


def test_issue_card_fail_miss_description(client):
    """
    Test if the request fails if it receives the issue type and title.
    """
    data_json = {"type": "issue",  "title": "Send message"}
    response = client.post("api/v1/cards/card", json=data_json)
    assert response.status_code == 400


def test_issue_card_fail_miss_description_and_title(client):
    """
    Test if the request fails if it receives only the issue type.
    """
    data_json = {"type": "issue"}
    response = client.post("api/v1/cards/card", json=data_json)
    assert response.status_code == 400


def test_bug_card_ok(client):
    """
    Test if the request is ok if it receives the bug type and description.
    """
    data_json = {"type": "bug", "description": "Cockpit is not depressurizing correctly"}
    response = client.post("api/v1/cards/card", json=data_json)
    assert response.status_code == 200
    card = json.loads(response.json["card"])
    assert card["type"] == data_json["type"]
    assert card["description"] == data_json["description"]
    title = card["title"].split("-")
    assert title[0] == "bug"
    assert isinstance(title[1], str)
    assert title[1]
    assert title[2].isdigit()


def test_bug_card_fail_miss_description(client):
    """
    Test if the request fails if it receives the bug type.
    """
    data_json = {"type": "bug"}
    response = client.post("api/v1/cards/card", json=data_json)
    assert response.status_code == 400


def test_bug_card_fail_description_and_title(client):
    """
    Test if the request fails if it receives the bug type.
    """
    data_json = {"type": "bug", "title": "some_title", "description": "Cockpit is not depressurizing correctly"}
    response = client.post("api/v1/cards/card", json=data_json)
    assert response.status_code == 400


def test_task_card_ok(client):
    """
    Test if the request is ok if it receives the task type, title and a category.
    """
    data_json = {"type": "task", "title": "Clean the Rocket", "category": "Maintenance"}
    response = client.post("api/v1/cards/card", json=data_json)
    assert response.status_code == 200
    card = json.loads(response.json["card"])
    assert card == data_json


def test_task_card_fail_miss_title_and_category(client):
    """
    Test if the request is ok if it receives the task type, title and a category.
    """
    data_json = {"type": "task"}
    response = client.post("api/v1/cards/card", json=data_json)
    assert response.status_code == 400


def test_task_card_fail_miss_title(client):
    """
    Test if the request is ok if it receives the task type, title and a category.
    """
    data_json = {"type": "task", "category": "Maintenance"}
    response = client.post("api/v1/cards/card", json=data_json)
    assert response.status_code == 400


def test_task_card_fail_miss_category(client):
    """
    Test if the request is ok if it receives the task type, title and a category.
    """
    data_json = {"type": "task", "title": "Clean the Rocket"}
    response = client.post("api/v1/cards/card", json=data_json)
    assert response.status_code == 400


def test_task_card_fail_invalid_category(client):
    """
    Test if the request is ok if it receives the task type, title and a category.
    """
    data_json = {"type": "task", "title": "Clean the Rocket", "category": "Some invalid category"}
    response = client.post("api/v1/cards/card", json=data_json)
    assert response.status_code == 400


def test_task_card_fail_description_title_and_category(client):
    """
    Test if the request fails if it receives the task type, title, description and category.
    """
    data_json = {"type": "task", "title": "Clean the Rocket",
                 "description": "Some description", "category": "Maintenance"}
    response = client.post("api/v1/cards/card", json=data_json)
    assert response.status_code == 400
