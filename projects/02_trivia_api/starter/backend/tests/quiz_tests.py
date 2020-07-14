import json

# A test function for the game functionality

def test_play_quiz(self):
    '''This function tests the response of Post Request of /quizzes endpoint'''

    response = self.client().post('/quizzes',
                                  json={'previous_questions': [24],
                                        'quiz_category': {'id': '2'}})
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertIsNotNone(data['question'])


