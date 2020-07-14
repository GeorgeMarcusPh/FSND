import json

# All the test functions related to categories endpoints

def test_get_questions_by_category(self):
    '''This function tests the response of Get request of /categories/<int:id>/questions endpoint'''

    response = self.client().get('/categories/1/questions')
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertIsNotNone(data['current_category'])

def test_create_category(self):
    '''This function tests the response of Post request of /categories/create endpoint'''

    response = self.client().post('/categories/create', json=self.new_category)
    data = json.loads(response.data)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertTrue(data['created'])
    self.assertIsNotNone(data['category_created'])
    self.assertIsNotNone(data['categories'])
    self.assertTrue(data['categories_count'])