import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Book


class BookTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "bookshelf_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "bolaji", "bolaji", "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)

        self.new_book = {"title": "Anansi Boys", "author": "Neil Gaiman", "rating": 5}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass
    
    # PRACTICE TDD
    def test_search_books(self):
        """Tests if the search functionality works as expected"""
        res = self.client().post("/books/search", json={"search":"we"})
        data = json.loads(res.data)


        self.assertEqual(res.status_code,200)
        self.assertEqual(data["success"],True)
        self.assertEqual(data["total_books"],2)
        self.assertTrue(len(data["books"]))

    def test_get_book_search_without_results(self):
        res = self.client().post("/books/search", json={"search":"rubbish"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data["success"],True)
        self.assertFalse(data["total_books"])
        self.assertFalse(len(data["books"]))

    def test_get_paginated_books(self):
        """Tests if the method and end point GET /books works properly"""
        res = self.client().get("/books")
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data["success"],True)
        self.assertTrue(data["total_books"])
        self.assertTrue(len(data["books"]))

    def test_404_requesting_invalid_page(self):
        res = self.client().get("/books?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"],"resource not found!")

    def test_update_book_rating(self):
        """Tests if the method and end point PATCH /books/book_id works properly"""
        res = self.client().patch("/books/4",json={"rating":4})
        data = json.loads(res.data)

        book = Book.query.get(4)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data["success"], True)
        self.assertEqual(book.format()["rating"],4)

    def test_400_updating_non_existence_book(self):
        res = self.client().patch("/books/1000",json={"rating":4})
        data = json.loads(res.data)

        self.assertEqual(data["success"], False)
        self.assertEqual(res.status_code,400)
        self.assertEqual(data["message"],"Bad request")

    def test_delete_book(self):
        """Tests if the method and end point DELETE /books/book_id works properly"""
        res = self.client().delete("/books/54")
        data = json.loads(res.data)

        book = Book.query.get(54)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data["success"],True)
        self.assertEqual(data["deleted"],54)
        self.assertTrue(data["total_books"])
        self.assertTrue(len(data["books"]))
        self.assertEqual(book,None)
    
    def test_500_deleting_non_existence_book(self):
        res = self.client().delete("/books/1000")
        data = json.loads(res.data)

        self.assertEqual(data["success"], False)
        self.assertEqual(res.status_code,500)
        self.assertEqual(data["message"],"Internal server error")

    def test_create_book(self):
        """Tests if the method and end point POST/books works properly"""
        res = self.client().post("/books",json=self.new_book)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(len(data["books"]))

    def test_500_book_creation_not_successful(self):
        res = self.client().post("/books/34",json=self.new_book)
        data = json.loads(res.data)

        self.assertEqual(data["success"], False)
        self.assertEqual(res.status_code,405)
        self.assertEqual(data["message"],"Method NOT allowed!")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
