import json

# All the test functions related to failed responses of all endpoints

def test_question_creation_failure(self):
    '''This function tests the failed response of /questions/create endpoint when invalid 
    body is sent via request'''

    response = self.client().post('/questions/create', json={})
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 422)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'unprocessable')

def test_question_deletion_failure(self):
    '''This function tests the failed response of /questions/<int:id> endpoint 
    when invalid id is set in route paramater'''

    response = self.client().delete('/questions/100')
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 400)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'bad request')

def test_search_questions_failure(self):
    '''This function tests the failed response of /questions/search endpoint 
    when a non existant char combination is set in the body of the request'''

    response = self.client().post('/questions/search',
                                  json={'searchTerm': 'abracadabra'})
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 404)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'resource not found')

def test_questions_by_category_failure(self):
    '''This function tests the failed response of /categories/<int:id>/questions endpoint 
    when an invalid category id is set to the route parameter'''

    response = self.client().get('/categories/100/questions')
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 404)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'resource not found')

def test_request_page_number(self):
    '''This function tests the failed response of /questions?page endpoint 
    when an invalid page number is set to the route arguments'''

    response = self.client().get('/questions?page=100')
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 404)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'resource not found')

def test_play_quiz_failure(self):
    '''This function tests the failed response of /quizzes endpoint 
    when an invalid request body is sent'''

    response = self.client().post('/quizzes', json={"previous_questions" : []})
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 400)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'bad request')  

def test_category_creation_failure(self):
    '''This function tests the failed response of /categories/create endpoint 
    when an invalid request body is sent'''

    response = self.client().post('/categories/create', json={})
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 422)
    self.assertEqual(data['success'], False)
    self.assertEqual(data['message'], 'unprocessable')    