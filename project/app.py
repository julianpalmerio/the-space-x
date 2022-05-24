from flask import Flask

def create_app():
    app = Flask(__name__)
    app.register_blueprint(blueprint_api_v1)
    return app


app = create_app()

if __name__ == '__main__':
    app.run()
