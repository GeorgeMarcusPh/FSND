from flask import jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
from models import Question, Category
from utility_methods import paginate_questions, map_categories_to_dict
import random

# A function that takes app as argument and implements all the questions related handlers endpoints

def questions_controller(app):

    @app.route('/questions')
    def get_questions():
        '''This endpoint gets a list of all questions and their count.
        
        Also it returns a list of all categories

        and checkes for empty results'''

        all_questions = Question.query.order_by(Question.id).all()
        paginated_questions = paginate_questions(request, all_questions)

        all_categories = Category.query.order_by(Category.id).all()

        if (len(paginated_questions) == 0 or len(all_categories) == 0):
            abort(404, "This collection of questions could not be found")

        data = {
            'success': True,
            'questions': paginated_questions,
            'questions_count': len(all_questions),
            'categories': map_categories_to_dict(all_categories)
        }

        return jsonify(data)

    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        '''This endpoint deletes a questions based on its id
        and checkes for errors.
        
        If an error occured all changes to db are reverted'''

        question = Question.query.filter_by(id=id).one_or_none()
        
        try:
            question.delete()

            all_questions = Question.query.order_by(Question.id).all()
            paginated_questions = paginate_questions(request, all_questions)

            all_categories = Category.query.order_by(Category.id).all()

            data = {
                'success': True,
                'deleted': id,
                'questions': paginated_questions,
                'questions_count': len(all_questions),
                'categories': map_categories_to_dict(all_categories)
            }

            return jsonify(data)

        except:
            if question is not None:
                question.rollback()
            abort(400, "bad request")

    @app.route('/questions/create', methods=['POST'])
    def create_question():
        '''This endpoint adds a questions based to db
        and checkes for errors.
        
        If an error occured all changes to db are reverted'''

        data = request.get_json()

        new_question = data.get('question', None)
        new_answer = data.get('answer', None)
        new_difficulty = data.get('difficulty', None)
        new_category = data.get('category', None)
        new_rating = data.get('rating', None)

        if(new_question is None or new_answer is None or new_difficulty is None or new_category is None):
            abort(422, 'unprocessable')
            
        question = Question(question=new_question, answer=new_answer,
                            difficulty=new_difficulty, category=new_category,
                            rating=new_rating)
        try:

            question.insert()

            all_questions = Question.query.order_by(Question.id).all()
            paginated_questions = paginate_questions(request, all_questions)

            data = {
                'success': True,
                'created': question.id,
                'question_created': question.question,
                'questions': paginated_questions,
                'questions_count': len(all_questions)
            }

            return jsonify(data)

        except:
            question.rollback()
            abort(400, "bad request")

    @app.route('/questions/search', methods=['POST'])
    def search_question():
        '''This endpoint looks for questions based on any combination of characters in the question
        or the answer.

        Also it checkes for errors.
        
        If an error occured all changes to db are reverted'''        
        data = request.get_json()

        search_term = data.get('searchTerm', "")

        queried_questions = Question.query.filter(
                Question.question.ilike(f'%{search_term}%')).all()

        if(queried_questions is None):
            queried_questions = Question.answer.ilike(f'%{search_term}%')

        if (len(queried_questions) == 0):
            abort(404,"Couldn't find queried questions")

        paginated_questions = paginate_questions(request, queried_questions)

        data = {
                'success': True,
                'questions': paginated_questions,
                'questions_count': len(queried_questions),
            }
        return jsonify(data)

    @app.route('/categories/<int:id>/questions')
    def get_questions_by_category(id):
        '''This endpoint looks for questions based on their category id

        Also it checkes for empty results.'''

        selected_questions = Question.query.filter_by(category=str(id)).all()
        selected_category = Category.query.filter_by(id=id).one_or_none()

        if (selected_questions is None or selected_category is None):
            abort(404, "This collection of questions could not be found")
        
        paginated_questions = paginate_questions(request, selected_questions)

        data = {
            'success': True,
            'questions': paginated_questions,
            'questions_count': len(selected_questions),
            'current_category': selected_category.type
        }

        return jsonify(data)

    @app.route('/quizzes', methods=['POST'])
    def get_random_quiz_question():
        '''This endpoint returns a randomly chosen question while excluding 
        previously chosen questions

        Also it checkes for empty results.'''
        
        data = request.get_json()

        previous_questions = data.get('previous_questions', None)
        
        if (previous_questions is None or len(previous_questions) == 0):
            abort(400, "bad request")

        category = data.get('quiz_category', None)

        if (category is None or category['id'] == 0):
            questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
        else:
            questions = Question.query.filter(Question.category==category['id'], Question.id.notin_(previous_questions)).all()

        question = random.choice(questions)

        data = {
            'success': True,
            'question': question.format()
        }
        
        return jsonify(data)
