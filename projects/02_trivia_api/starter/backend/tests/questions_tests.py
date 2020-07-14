import json
from models import Question

# All the test functions related to questions endpoints

def test_get_questions(self):
    '''This function tests the response of Get Request of /questions endpoint'''

    response = self.client().get('/questions')
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertTrue(data['questions_count'])
    self.assertGreaterEqual(len(data['questions']), 1)
    self.assertIsNotNone(len(data['questions']))
    self.assertIsNotNone(data['categories'])

def test_delete_question(self):
    '''This function tests the response of Delete Request of /questions/<int:id> endpoint'''

    question = Question(
            question=self.new_question['question'],
            answer=self.new_question['answer'],
            category=self.new_question['category'],
            difficulty=self.new_question['difficulty'],
            rating = self.new_question['rating']
    )

    question.insert()
    question_id = question.id

    response = self.client().delete(f'/questions/{question_id}')
    data = json.loads(response.data)

    question = Question.query.filter(Question.id == question_id).one_or_none()

    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertEqual(data['deleted'], question_id)
    self.assertEqual(question, None)

def test_create_question(self):
    '''This function tests the response of Post Request of /questions/create endpoint'''

    response = self.client().post('/questions/create', json=self.new_question)
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertTrue(data['created'])
    self.assertIsNotNone(data['question_created'])
    self.assertIsNotNone(data['questions'])
    self.assertTrue(data['questions_count'])

def test_search_questions(self):
    '''This function tests the response of Post Request of /questions/search endpoint'''

    response = self.client().post('/questions/search',
                                  json={'searchTerm': 'Who'})

    data = json.loads(response.data)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertTrue(data['questions_count'])
    self.assertGreaterEqual(len(data['questions']), 1)
    self.assertIsNotNone(data['questions'])
