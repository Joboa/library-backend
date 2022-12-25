"""
Books api 
"""
from flask import Blueprint, request, jsonify

books = Blueprint("books", __name__, url_prefix="/api/v1/")


@books.get('/books/')
def fetch_books():
    return jsonify({"books": "book 1"})
