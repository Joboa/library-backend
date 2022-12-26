"""
Journals API 
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from libraryapi.models import db, Journal

journals = Blueprint("journals", __name__, url_prefix="/api/v1/")


@journals.route('/journals/', methods=['POST', 'GET'])
@jwt_required()
def get_or_add_journals():

    current_user = get_jwt_identity()

    if request.method == 'POST':
        title = request.get_json().get('title', '')
        publisher = request.get_json().get('publisher', '')
        publication_date = request.get_json().get('publication_date', '')
        first_author = request.get_json().get('first_author', '')
        second_author = request.get_json().get('second_author', '')
        last_author = request.get_json().get('last_author', '')
        url_to_journal = request.get_json().get('url_to_journal', '')

        # check if journal already exist
        if Journal.query.filter_by(title=title).first():
            return jsonify({"error": "Journal already exist in the database"}), 409

        journal = Journal(title=title, publisher=publisher,
                          publication_date=publication_date,
                          first_author=first_author,
                          second_author=second_author,
                          last_author=last_author,
                          url_to_journal=url_to_journal,
                          user_id=current_user)

        db.session.add(journal)
        db.session.commit()

        return jsonify({
            "id": journal.id,
            "title": journal.title,
            "publisher": journal.publisher,
            "publication_date": journal.publication_date,
            "first_author": journal.first_author,
            "second_author": journal.second_author,
            "last_author": journal.last_author,
            "authors_shorten": journal.authors_shorten,
            "url_to_journal": journal.url_to_journal,
            "created_at": journal.created_at,
            "updated_at": journal.updated_at
        }), 201

    # get all journals
    else:
        # pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        journals = Journal.query.filter_by(user_id=current_user).paginate(
            page=page, per_page=per_page)

        # metadata
        meta = {
            "page": journals.page,
            "pages": journals.pages,
            "total_count": journals.total,
            "prev_page": journals.prev_num,
            "next_page": journals.next_num,
            "has_next": journals.has_next,
            "has_prev": journals.has_prev
        }

        return jsonify({"journals": [journal.to_dict() for journal in journals], "meta": meta}), 200


@journals.get("/journals/<int:id>/")
@jwt_required()
def get_journal(id):
    current_user = get_jwt_identity()

    journal = Journal.query.filter_by(user_id=current_user, id=id).first()

    if not journal:
        return jsonify({"message": "journal not found!"}), 404

    return jsonify({
        "id": journal.id,
        "title": journal.title,
        "publisher": journal.publisher,
        "publication_date": journal.publication_date,
        "first_author": journal.first_author,
        "second_author": journal.second_author,
        "last_author": journal.last_author,
        "url_to_journal": journal.url_to_journal,
        "authors_shorten": journal.authors_shorten,
        "created_at": journal.created_at,
        "updated_at": journal.updated_at
    }), 201


@journals.patch("journals/<int:id>/")
@journals.put("journals/<int:id>/")
@jwt_required()
def edit_journal(id):
    current_user = get_jwt_identity()

    journal = Journal.query.filter_by(user_id=current_user, id=id).first()

    if not journal:
        return jsonify({"message": "Journal not found!"}), 404

    title = request.get_json().get('title', '')
    publisher = request.get_json().get('publisher', '')
    publication_date = request.get_json().get('publication_date', '')
    first_author = request.get_json().get('first_author', '')
    second_author = request.get_json().get('second_author', '')
    last_author = request.get_json().get('last_author', '')
    url_to_journal = request.get_json().get('url_to_journal', '')

    # update journal
    journal.title = title
    journal.publisher = publisher
    journal.publication_date = publication_date
    journal.first_author = first_author
    journal.second_author = second_author
    journal.last_author = last_author
    journal.url_to_journal = url_to_journal

    db.session.commit()

    return jsonify({
        "id": journal.id,
        "title": journal.title,
        "publisher": journal.publisher,
        "publication_date": journal.publication_date,
        "first_author": journal.first_author,
        "second_author": journal.second_author,
        "last_author": journal.last_author,
        "url_to_journal": journal.url_to_journal,
        "authors_shorten": journal.authors_shorten,
        "created_at": journal.created_at,
        "updated_at": journal.updated_at
    }), 200


@journals.delete("journals/<int:id>/")
@jwt_required()
def delete_journal(id):
    current_user = get_jwt_identity()

    journal = Journal.query.filter_by(user_id=current_user, id=id).first()

    if not journal:
        return jsonify({"message": "Journal not found!"}), 404

    db.session.delete(journal)
    db.session.commit()

    return jsonify({}), 204
