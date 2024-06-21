from flask import Flask
def create_app():
    app = Flask(__name__)
    with app.app_context():
        from . import Endpoint
        app.register_blueprint(Endpoint.bp)

    return app
