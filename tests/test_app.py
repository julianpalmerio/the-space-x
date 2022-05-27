def test_issue_card_ok(client):
    """
    Test if the request is ok if it receives the issue type, title and description.
    """
    data_json = {"type": "issue", "title": "Send message", "description": "Let pilots send messages to Central"}
    response = client.post("api/v1/cards/card", json=data_json)
    assert response.status_code == 200


def test_issue_card_fail_miss_title(client):
    """
    Test if the request fails if it receives the issue type and description.
    """
    data_json = {"type": "issue", "description": "Let pilots send messages to Central"}
    response = client.post("api/v1/cards/card", json=data_json)
    assert response.status_code == 400


def test_issue_card_fail_miss_description(client):
    """
    Test if the request fails if it receives only the issue type.
    """
    data_json = {"type": "issue"}
    response = client.post("api/v1/cards/card", json=data_json)
    assert response.status_code == 400