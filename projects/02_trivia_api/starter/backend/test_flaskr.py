from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db
import unittest


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        setup_db(self.app, self.database_name)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

        self.new_question = {
            'question': 'Are you doing this on your own?',
            'answer': 'Yes',
            'category': 1,
            'difficulty': 1,
            'rating': 5
        }

        self.new_category = {
            'type': 'Computer Science'
        }

    def tearDown(self):
        """Executed after reach test"""
        pass
    
    # import all test function in other script files and inject them in the test class 
    from tests.category_tests import test_get_questions_by_category, test_create_category
    from tests.questions_tests import test_create_question, test_delete_question, test_get_questions, test_search_questions
    from tests.quiz_tests import test_play_quiz
    from tests.failure_tests import test_question_creation_failure, test_question_deletion_failure, test_questions_by_category_failure, test_request_page_number, test_search_questions_failure, test_play_quiz_failure, test_category_creation_failure


if __name__ == "__main__":
    unittest.main()
