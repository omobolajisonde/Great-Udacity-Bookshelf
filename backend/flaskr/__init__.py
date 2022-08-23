import os
from turtle import title
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy  # , or_
from flask_cors import CORS
import random

from models import setup_db, db_rollback, db_close, Book

BOOKS_PER_SHELF = 8

# @TODO: General Instructions
#   - As you're creating endpoints, define them and then search for 'TODO' within the frontend to update the endpoints there.
#     If you do not update the endpoints, the lab will not work - of no fault of your API code!
#   - Make sure for each route that you're thinking through when to abort and with which kind of error
#   - If you change any of the response body keys, make sure you update the frontend to correspond.


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    def paginate_books(books):
        page = request.args.get("page", 1, type=int)
        start = (page-1)*BOOKS_PER_SHELF
        end = start+BOOKS_PER_SHELF

        formatted_books = [book.format() for book in books]
        return formatted_books[start:end]

    # SEARCH Books
    @app.route("/books/search", methods=["POST"])
    def search_books():
        search = request.get_json()
        books = Book.query.filter(Book.title.ilike(
            "%{}%".format(search["search"]))).order_by(Book.id).all()
        selected_books = paginate_books(books)
        return jsonify({
            "success": True,
            "books": selected_books,
            "total_books": len(books),
        })

    # GET ALL BOOKS

    @app.route("/books", methods=["GET"])
    def get_books():
        books = Book.query.all()
        selected_books = paginate_books(books)
        if (not len(selected_books)):
            abort(404)
        else:
            return jsonify({
                "success": True,
                "books": selected_books,
                "total_books": len(books),
            })

    # UPDATES A SINGLE BOOK'S RATING
    @app.route("/books/<int:book_id>", methods=["PATCH"])
    def update_book_rating(book_id):
        try:
            rating = request.get_json()
            book = Book.query.filter(Book.id == book_id).one_or_none()
            print(book)
            if book is None:
                abort(404)
            if 'rating' in rating:
                book.rating = rating["rating"]
                book.update()
                return jsonify({
                    "success": True
                })
        except:
            abort(400)

    # DELETE A BOOK
    @app.route("/books/<int:book_id>", methods=["DELETE"])
    def delete_book(book_id):
        error = None
        try:
            book = Book.query.filter(Book.id == book_id).one_or_none()
            if book is None:
                abort(404)
            else:
                book.delete()
        except:
            error = True
            db_rollback()
        finally:
            db_close()
        if error:
            abort(500)
        else:
            books = Book.query.all()
            selected_books = paginate_books(books)
            return jsonify({
                "success": True,
                "deleted": book_id,
                "books": selected_books,
                "total_books": len(books)
            })

    # CREATE A NEW BOOK
    @app.route("/books", methods=["POST"])
    def add_book():
        error = None
        body = {}
        try:
            body = request.get_json()
            new_title = body.get("title", None)
            new_author = body.get("author", None)
            new_rating = body.get("rating", None)
            new_book = Book(title=new_title, author=new_author,
                            rating=new_rating)
            new_book.insert()
            body = {
                "id": new_book.id,
                "title": new_book.title,
                "author": new_book.author,
                "rating": new_book.rating
            }
        except:
            error = True
            db_rollback()
        finally:
            db_close()
        if error:
            abort(500)
        else:
            books = Book.query.order_by(Book.id.desc()).all()
            selected_books = paginate_books(books)
            return jsonify({
                "success": True,
                "created": body["id"],
                "books": selected_books,
                "total_books": len(Book.query.all())
            })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found!"
        }), 404

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method NOT allowed!"
        }), 405

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal server error"
        }), 500

    return app
