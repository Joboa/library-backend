
"""
Users registration and authentication
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

from werkzeug.security import generate_password_hash, check_password_hash
import validators

from libraryapi.models import db, User

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.post('/register/')
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    if len(password) < 6:
        return jsonify({"error": "Password is too short"}), 400

    if len(username) < 3:
        return jsonify({"error": "Username is too short"}), 400

    if not validators.email(email):
        return jsonify({"error": "Email is not valid"}), 400

    # check is user.email already exist
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"error": "Email is taken"}), 409

    # check is user.username already exist
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({"error": "User already exist"}), 409

    password_hash = generate_password_hash(password, method='sha256')
    user = User(username=username, password=password_hash, email=email)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User created",
        "user": {
            "username": username, "email": email
        }
    }), 201


@auth.post('/login/')
def login():
    email = request.json.get('email', '')
    password = request.json.get('password', '')

    user = User.query.filter_by(email=email).first()

    if user:
        is_password_correct = check_password_hash(user.password, password)

        if is_password_correct:
            refresh = create_refresh_token(identity=user.id)
            access = create_access_token(identity=user.id)
            return jsonify({
                "user": {
                    "refresh": refresh,
                    "access": access,
                    "username": user.username,
                    "email": user.email,
                }
            }), 200

    return jsonify({"error": "Incorrect credentials"}), 401


@auth.get('/me/')
@jwt_required()
def me():
    user_id = get_jwt_identity()

    user = User.query.filter_by(id=user_id).first()

    return jsonify({
        "email": user.email,
        "username": user.username
    }), 200


@auth.get('/token/refresh')
@jwt_required(refresh=True)
def refresh_users_token():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)

    return jsonify({
        "access": access
    }), 200
