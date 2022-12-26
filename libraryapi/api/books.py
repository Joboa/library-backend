"""
Books api 
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from libraryapi.models import db, Book

books = Blueprint("books", __name__, url_prefix="/api/v1/")


@books.route('/books/', methods=['POST', 'GET'])
@jwt_required()
def get_or_add_books():
    
    current_user = get_jwt_identity()

    if request.method == 'POST':
        title = request.get_json().get('title', '')
        edition = request.get_json().get('edition', '')
        book_type = request.get_json().get('book_type', '')

        # check if book already exist
        if Book.query.filter_by(title=title).first():
            return jsonify({"error": "book already exist in the database"}), 409

        book = Book(title=title, edition=edition,
                    book_type=book_type, user_id=current_user)
        db.session.add(book)
        db.session.commit()

        return jsonify({
            "id": book.id,
            "title": book.title,
            "edition": book.edition,
            "book_type": book.book_type,
            "created_at": book.created_at,
            "updated_at": book.updated_at
        }), 201

    # get all books
    else:
        # pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        books = Book.query.filter_by(user_id=current_user).paginate(
            page=page, per_page=per_page)

        # metadata
        meta = {
            "page": books.page,
            "pages": books.pages,
            "total_count": books.total,
            "prev_page": books.prev_num,
            "next_page": books.next_num,
            "has_next": books.has_next,
            "has_prev": books.has_prev
        }

        return jsonify({"books": [book.to_dict() for book in books], "meta": meta}), 200


@books.get("/books/<int:id>/")
@jwt_required()
def get_book(id):
    current_user = get_jwt_identity()

    book = Book.query.filter_by(user_id=current_user, id=id).first()

    if not book:
        return jsonify({"message": "book not found!"}), 404

    return jsonify({
        "id": book.id,
        "title": book.title,
        "edition": book.edition,
        "book_type": book.book_type,
        "created_at": book.created_at,
        "updated_at": book.updated_at
    }), 200


@books.put("books/<int:id>/")
@jwt_required()
def edit_book(id):
    current_user = get_jwt_identity()

    book = Book.query.filter_by(user_id=current_user, id=id).first()

    if not book:
        return jsonify({"message": "book not found!"}), 404

    title = request.get_json().get('title', '')
    edition = request.get_json().get('edition', '')
    book_type = request.get_json().get('book_type', '')

    # update book
    book.title = title
    book.edition = edition
    book.book_type = book_type

    db.session.commit()

    return jsonify({
        "id": book.id,
        "title": book.title,
        "edition": book.edition,
        "book_type": book.book_type,
        "created_at": book.created_at,
        "updated_at": book.updated_at
    }), 200


@books.delete("books/<int:id>/")
@jwt_required()
def delete_book(id):
    current_user = get_jwt_identity()

    book = Book.query.filter_by(user_id=current_user, id=id).first()

    if not book:
        return jsonify({"message": "book not found!"}), 404

    db.session.delete(book)
    db.session.commit()

    return jsonify({}), 204
