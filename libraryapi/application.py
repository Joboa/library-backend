""" 
creates a Flask app instance and registers the database object
"""

from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_bootstrap import Bootstrap4

from libraryapi.models import db, User
from admin_page.admin import admin
from libraryapi.api import auth, books, journals

migrate = Migrate()
login_manager = LoginManager()


def create_app(app_name='LIBRARY_API'):
    # instantiate flask app
    app = Flask(app_name)
    app.config.from_object('libraryapi.config.BaseConfig')

    # Allow cross-origin
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}}, origins=["http://localhost:3000","https://j-library.netlify.app/"])

    # database setup
    db.init_app(app)
    migrate.init_app(app, db)

    # json web tokens
    JWTManager(app)

    # flask login manager
    login_manager.init_app(app)
    login_manager.login_view = 'admin.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    # register apps
    app.register_blueprint(admin)
    app.register_blueprint(auth.auth)
    app.register_blueprint(books.books)
    app.register_blueprint(journals.journals)
    
    bootstrap = Bootstrap4(app)

    # handle application errors
    # url error
    @app.errorhandler(404)
    def handle_404(e):
        return jsonify({"error": "Not found!"}), 404

    # server error
    @app.errorhandler(500)
    def handle_500(e):
        return jsonify({"error": "Something went wrong and we are working on it"}), 500

    return app
