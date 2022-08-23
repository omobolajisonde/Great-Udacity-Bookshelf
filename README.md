# Great Udacity Bookshelf

Great Udacity bookshelf is a project in course 2: API Development and Documentation of the Udacity Full Stack Web Developer Nanodegree.
It is a virtual bookshelf of Udacity, where one can Create a new book, Read all the books avaliable (paginated), Update book ratings and Delete books.
As a student of the Nanodegree, building this project helped solidify all the knlowedge I gained on API development and documentation.

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/). 

## Getting Started

### Pre-requisites and Local Development 
Developers using this project should already have Python3, pip and node installed on their local machines.

#### Backend

From the backend folder run `pip install requirements.txt`. All required packages are included in the requirements file. 

To run the application run the following commands: 
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration. 

#### Frontend

From the frontend folder, run the following commands to start the client: 
```
npm install // only once to install dependencies
npm start 
```

By default, the frontend will run on localhost:3000. 

### Tests
In order to run tests navigate to the backend folder and run the following commands: 

```
dropdb bookshelf_test
createdb bookshelf_test
psql bookshelf_test < books.psql
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command. 

All tests are kept in that file and should be maintained as updates are made to app functionality. 


## API DOCS

### Getting Started
- Base URL: The app is currently not deployed and can only be tested out if setup on your local machine. The backend runs on `http://127.0.0.1:5000/` and connected as proxy to the frontend.

- Authentication: No authentication or any sort of unique keys for this version of the application

### Error Handling
- Format: All responses to requests including failed ones are returned in JSON (JavaScript Object Notation) format.
```
{
    "success": false,
    "error": code,
    "message": "error message"
}
```

Potential error types that could be encountered on failed request
- 404: Not Found
- 400: Bad Request
- 500: Internal Server Error

### Endpoints
#### GET /books
- General:
    - Responds with a list of book objects, success value and total books
    - List of book objects that are part of the response are paginated. Therefore, the list of books returned varies with the page specified in the query parameter, default page is 1.
- Sample: `-curl http://127.0.0.1:5000/books` or `http://127.0.0.1:5000/books?page=1`

```
{
  "books": [
    {
      "author": "Amitava Kumar",
      "id": 7,
      "rating": 5,
      "title": "Immigrant, Montana"
    },
    {
      "author": "Gregory Blake Smith",
      "id": 16,
      "rating": 2,
      "title": "The Maze at Windermere"
    },
    {
      "author": "Tara Westover",
      "id": 4,
      "rating": 5,
      "title": "Educated: A Memoir"
    },
    {
      "author": "Tayari Jones",
      "id": 10,
      "rating": 5,
      "title": "An American Marriage"
    },
    {
      "author": "Madeline Miller",
      "id": 8,
      "rating": 5,
      "title": "CIRCE"
    },
    {
      "author": "Jordan B. Peterson",
      "id": 11,
      "rating": 5,
      "title": "12 Rules for Life: An Antidote to Chaos"
    },
    {
      "author": "Lisa Halliday",
      "id": 2,
      "rating": 4,
      "title": "Asymmetry: A Novel"
    },
    {
      "author": "Gina Apostol",
      "id": 9,
      "rating": 5,
      "title": "Insurrecto: A Novel"
    }
  ],
  "success": true,
  "total_books": 15
}

```
### POST /books
-   General:
    - Expects a JSON body, with the required parameters as part of the request.
    - Creates a new book in the database if provided with adequate parameters in the request body.
    - Returns the id of the created book, success value, total books, and list of books based on the current page to update the frontend
    Typically, the request body sent should be like this:
    ```
    {
      "author": "Gina Apostol",
      "rating": 5,
      "title": "Insurrecto: A Novel"
    }   

    ```
- Sample: `curl http://127.0.0.1:5000/books?page=2 -X POST -H "Content-Type: application/json" -d '{"title":"Things fall apart", "author":"Chinu Achebe", "rating":"5"}'`

```
{
  "books": [
    {
      "author": "Tayari Jones",
      "id": 10,
      "rating": 5,
      "title": "An American Marriage"
    },
    {
      "author": "Gina Apostol",
      "id": 9,
      "rating": 5,
      "title": "Insurrecto: A Novel"
    },
    {
      "author": "Madeline Miller",
      "id": 8,
      "rating": 5,
      "title": "CIRCE"
    },
    {
      "author": "Amitava Kumar",
      "id": 7,
      "rating": 5,
      "title": "Immigrant, Montana"
    },
    {
      "author": "Jojo Moyes",
      "id": 5,
      "rating": 5,
      "title": "Still Me: A Novel"
    },
    {
      "author": "Tara Westover",
      "id": 4,
      "rating": 5,
      "title": "Educated: A Memoir"
    },
    {
      "author": "Kristin Hannah",
      "id": 3,
      "rating": 5,
      "title": "The Great Alone"
    },
    {
      "author": "Lisa Halliday",
      "id": 2,
      "rating": 4,
      "title": "Asymmetry: A Novel"
    }
  ],
  "created": 45,
  "success": true,
  "total_books": 16
}

```
- PATCH /books/{book_id}
- General:
    - Updates just the rating of a particular book.
    - Expects a JSON body, with "rating" parameter as part of the request.
    - Retrieves the book ID off the URL and updates the book's rating based on the value of the "rating" parameter.
    - Returns success value
- Sample: `curl http://127.0.0.1:5000/books/10 -X PATCH -H "Content-Type: application/json" -d '{"rating":"3"}'`
```
{
  "success": true
}

```
- DELETE /books/{book_id}
- General:
    - Deletes book with same ID as in the URL
    - Returns list of books based on the current page, success value, id of deleted book and total books to update the frontend

```

{
  "books": [
    {
      "author": "Amitava Kumar",
      "id": 7,
      "rating": 5,
      "title": "Immigrant, Montana"
    },
    {
      "author": "Gregory Blake Smith",
      "id": 16,
      "rating": 2,
      "title": "The Maze at Windermere"
    },
    {
      "author": "Tara Westover",
      "id": 4,
      "rating": 5,
      "title": "Educated: A Memoir"
    },
    {
      "author": "Madeline Miller",
      "id": 8,
      "rating": 5,
      "title": "CIRCE"
    },
    {
      "author": "Jordan B. Peterson",
      "id": 11,
      "rating": 5,
      "title": "12 Rules for Life: An Antidote to Chaos"
    },
    {
      "author": "Lisa Halliday",
      "id": 2,
      "rating": 4,
      "title": "Asymmetry: A Novel"
    },
    {
      "author": "Gina Apostol",
      "id": 9,
      "rating": 5,
      "title": "Insurrecto: A Novel"
    },
    {
      "author": "Jojo Moyes",
      "id": 5,
      "rating": 5,
      "title": "Still Me: A Novel"
    }
  ],
  "deleted": 45,
  "success": true,
  "total_books": 15
}

```

## Deployment N/A

## Authors
My dear instructor, [Coach Caryn McCarthy](https://www.linkedin.com/in/carynmccarthy) and [my humble self](https://github.com/omobolajisonde) 

## Acknowledgements 
The awesome team at Udacity and Coach Caryn McCarthy!