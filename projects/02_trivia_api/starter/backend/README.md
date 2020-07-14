# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.8.2

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr # on windows use set instead of export
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## Testing

To run the tests, run after navigating to the backend folder

```bash
python -m unittest test_flaskr.py

```

## API Reference

### Getting Started

This api is served at port 5000, which is http://127.0.0.1:5000

### Error Handlers

You can expect the following types of errors from API:

- 400: Bad Request
- 404: Resource not found
- 422: Unprocessable
- 500: Internal Server Error

### Endpoints

#### Category

```bash
curl http://127.0.0.1:5000/categories
```

###### Response

```json
{
  "categories": {
    "1": "Politics",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```

#### Question

Requests for questions, including pagination (10 questions per page).

```bash
curl http://127.0.0.1:5000/categories/2/questions
```

###### Response

```json
{
  "categories": {
    "1": "Politics",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    }
  ],
  "success": true,
  "questions_count": 2
}
```

#### Add a new question

```bash
curl http://127.0.0.1:5000/questions/create -X POST -H "Content-Type: application/json" -d '{"answer":"yes", "question":"Are you doing this on your own?", "category":1, "difficulty": 1}'
```

###### Response

```json
{
  "success": true,
  "created": 24,
  "question_created": "Are you doing this on your own?",
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "rating": 7,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "yes",
      "category": 1,
      "difficulty": 1,
      "id": 24,
      "rating": 3,
      "question": "Are you doing this on your own?"
    }
  ],
  "questions_count": 3
}
```

#### Search for a question

```bash
curl http://127.0.0.1:5000/questions/search -X POST 'Content-Type: application/json' -d '{"searchTerm":"Clay"}'
```

###### Response

```json
{
  "success": true,
  "questions": [
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "rating": 5,
      "question": "What boxer's original name is Cassius Clay?"
    }
  ],
  "questions_count": 1
}
```

#### Delete a question

```bash
curl -X DELETE http://127.0.0.1:5000/questions/24
```

###### Response

```json
{
  "deleted": 24,
  "success": true
}
```

#### Play quizzes

```bash
curl 'http://127.0.0.1:5000/quizzes' -X POST -H
'Content-Type: application/json' -d '{"previous_questions":[],"quiz_category":{"type":"Politics","id":"1"}}'
```

###### Response

```json
{
  "previous_questions": [],
  "question": {
    "answer": "Scarab",
    "category": 4,
    "difficulty": 4,
    "id": 23,
    "rating": 2,
    "question": "Which dung beetle was worshipped by the ancient Egyptians"
  },
  "success": true
}
```

#### Add a new category

```bash
curl http://127.0.0.1:5000/categories/create -X POST -H "Content-Type: application/json" -d '{"type":"Computer Science"}'
```

###### Response

```json
{
  "success": true,
  "created": 7,
  "category_created": "Computer Science",
  "categories": {
    "1": "Politics",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports",
    "7": "Computer Science"
  },
  "category_count": 7
}
```

##### Author

George Marcus
