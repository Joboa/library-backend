
"""
Users registration and authentication
"""
from flask import Blueprint, request, jsonify

from libraryapi.models import db, User

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.post('/register/')
def register():
    data = request.get_json()
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@auth.get('/me/')
def me():
    return {"user": "me"}
