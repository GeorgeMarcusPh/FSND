from flask import Flask
from flask_cors import CORS

from models import setup_db
from controllers.category_controller import category_controller
from controllers.questions_controller import questions_controller
from controllers.error_handlers_controller import error_handlers_controler

database_name = "trivia"


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app, database_name)

    CORS(app, resources={r"/*": {'origins': 'localhost:5000'}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    # all imported functions which implement the app endpoints
    category_controller(app)
    questions_controller(app)
    error_handlers_controler(app)

    return app
