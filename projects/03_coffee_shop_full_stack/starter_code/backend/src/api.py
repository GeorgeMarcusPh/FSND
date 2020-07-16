from flask import Flask
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db
from .controllers.error_handlers_controller import error_handlers
from .controllers.drinks_controller import drinks_controller

app = Flask(__name__)
setup_db(app)

# ALLOWING CORS
CORS(app, resources={r"/*": {'origins': 'http://localhost:5000'}})


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization, true')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,POST,DELETE,PATCH,OPTIONS')
    return response


'''
uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()


# ROUTES
drinks_controller(app)

# Error Handling
error_handlers(app)
