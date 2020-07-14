from flask import jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from models import Category
from utility_methods import map_categories_to_dict


# A function that takes app as argument and implements all the category related endpoints (get and create)

def category_controller(app):
    
    @app.route('/categories')
    def get_categories():
        '''This endpoint gets a list of all categories
        and checkes for empty results'''


        all_categories = Category.query.order_by(Category.id).all()
        
        if (len(all_categories) == 0):
            abort(404, "Couldn;t find this list of categories")

        data =  {
            'success': True,
            'categories': map_categories_to_dict(all_categories)
        }

        return jsonify(data)

    @app.route('/categories/create', methods=['POST'])
    def create_category():
        '''This endpoint adds new category to db and checks for errors.
        
        If an error occured all changes to db are reverted'''

        data = request.get_json()
        new_type = data.get('type', None)

        if new_type is None:
            abort(422, 'unprocessable')
        
        category = Category(type=new_type)

        try:
            category.insert()
            all_categories = Category.query.order_by(Category.id).all()
           
            data = {
                'success': True,
                'created': category.id,
                'category_created': category.type,
                'categories': map_categories_to_dict(all_categories),
                'categories_count': len(all_categories)
            }

            return jsonify(data)

        except:
            category.rollback()
            abort(400, "bad request")
