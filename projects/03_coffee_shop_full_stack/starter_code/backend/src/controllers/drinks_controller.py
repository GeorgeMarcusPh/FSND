from flask import jsonify, request, abort
from ..database.models import Drink
from ..auth.auth import requires_auth
import json


def drinks_controller(app):
    @app.route('/drinks', methods=['GET'])
    def get_drinks():
        '''A public function which gets all drinks '''

        # map each drink to a function called short and store them in a list
        drinks = list(map(Drink.short, Drink.query.order_by(Drink.id).all()))

        data = {
            'success': True,
            'drinks': drinks
        }
        return jsonify(data), 200

    @app.route('/drinks-detail', methods=['GET'])
    @requires_auth('get:drinks-detail')
    def get_drinks_detail(payload):
        ''' Authorized function to get more details about drinks'''

        # map each drink to a function called long and store them in a list
        drinks = list(map(Drink.long, Drink.query.order_by(Drink.id).all()))

        data = {
            'success': True,
            'drinks': drinks
        }
        return jsonify(data), 200

    @app.route('/drinks', methods=['POST'])
    @requires_auth('post:drinks')
    def create_drink(payload):
        ''' Authorized function to create new drinks'''
        request_body = request.get_json()

        recipe = request_body.get('recipe', None)
        title = request_body.get('title', None)

        # json.dumps converts a dict object to a json string to be able to store the recipe in db
        drink = Drink(title=title, recipe=json.dumps(recipe))

        try:
            drink.insert()
        except:
            drink.rollback()
            abort(422)

        drinks = [drink.long()]

        data = {
            'success': True,
            'drinks': drinks
        }

        return jsonify(data), 200

    @app.route('/drinks/<int:id>', methods=['PATCH'])
    @requires_auth('patch:drinks')
    def update_drink(payload, id):
        ''' Authorized function to update a drink using its id'''

        request_body = request.get_json()
        drink = Drink.query.filter_by(id=id).one_or_none()

        if drink is None:
            abort(404)

        try:
            title = request_body.get('title', None)
            recipe = request_body.get('recipe', None)

            drink.title = title
            drink.recipe = json.dumps(recipe)
            drink.update()

        except:
            drink.rollback()
            abort(400)

        drinks = [drink.long()]

        data = {
            'success': True,
            'drinks': drinks
        }

        return jsonify(data), 200

    @app.route('/drinks/<int:id>', methods=['DELETE'])
    @requires_auth('delete:drinks')
    def delete_drink(payload, id):
        ''' Authorized function to delete a drink using its id'''

        drink = Drink.query.filter_by(id=id).one_or_none()

        if drink is None:
            abort(404)
        try:
            drink.delete()
        except:
            drink.rollback()
            abort(400)

        data = {
            'success': True,
            'delete': drink.id
        }
        return jsonify(data), 200
