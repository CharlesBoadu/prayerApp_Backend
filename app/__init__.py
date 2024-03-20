from flask import Flask
from app.views import auth


def create_app(test_config=None):
    app = Flask(__name__)

    @app.route('/')
    def index():
        return 'Welcome to the Prayer Application Backend! 🙏🏽'

    app.register_blueprint(auth.auth_bp)
    return app