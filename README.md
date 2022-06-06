The Space X API
=================

This API allows you to create cards within a Trello board

The API was developed in python 3.8.10

Usage
-----

Clone the repo:

    git clone https://github.com/julianpalmerio/the-space-x
    cd the-space-x

Create virtualenv:

    virtualenv venv
    source venv/bin/activate
    pip install -r ./requirements/requirements.txt

Create an .env file based on .env.template

Run the api:

    python app.py

Try the endpoints:

    curl \
    -H "Content-Type: application/json" \
    -d '{"type": "issue", "title": "Send message", "description": "Let pilots send messages to Central"}' \
    "http://localhost:5000/api/v1/cards/card"

    curl \
    -H "Content-Type: application/json" \
    -d '{"type": "bug", "description": "Cockpit is not depressurizing correctly"}' \
    "http://localhost:5000/api/v1/cards/card"

    curl \
    -H "Content-Type: application/json" \
    -d '{"type": "task", "title": "Clean the Rocket", "category": "Maintenance"}' \
    "http://localhost:5000/api/v1/cards/card"

Swagger docs available at `http://localhost:5000/api/v1/`


Running Tests
-----

    python -m pytest

Project structure
-----
    .
    ├── README.md
    ├── .gitignore
    ├── .env.template
Template to take as a model of the .env file

    ├── .env
We must create this file. There we must put the environment configuration.

    ├── config.py
Configuration for different environments are there.

    ├── app.py
Here we define the create_app function that loads the configurations, registers the blueprints, and returns the app.
Use this file also to run the application.

    ├── apiv1.py
Here we create the main Blueprint with the flask-restx api object, at this point we register the flask-restx namespaces.

    ├── exceptions
    │   ├── exceptions.py
Here are the custom exceptions.

    ├── models
    │   ├── card.py
Here you will find the models for the different cards. In case you want to add a new type of card, it is highly recommended to extend from the base model.

    │   ├── factory.py
Inside are the necessary functions to be able to register new models in the api, following a plugin pattern. This way we can add new models by registering them without having to modify the endpoints.

    ├── namespaces
    │   ├── cards
    │   │   ├── service
    │   │   │   ├── trello_conector.py
    │   │   ├── cards.py
We define the namespaces that the api will use, in individual folders. In namespaces.cards.cards.py we define the endpoints of the cards namespace and in namespaces.cards.service the necessary logic.

    ├── requirements
    │   ├── requirements.txt
    ├── tests
    │   ├── __init__.py    
    │   ├── conftest.py
    │   ├── test_app.py

TO DO
-----

This is a list of pending tasks that it is highly recommended to do in the near future, to have a more robust project:


- Migrate to Docker to improve production stability, ease of deployment and maintenance.

- Add the necessary configurations to use a Uwsgi server or similar.

- It would be a good idea to use Nginex as a load balancer and reverse proxy for docker.

- Add an authentication layer.

- Improve documentation in swagger.

- It would be nice to use poetry.