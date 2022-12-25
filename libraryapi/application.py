""" 
creates a Flask app instance and registers the database object
"""

from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS

from libraryapi.models import db
from libraryapi.api import auth, books, journals

migrate = Migrate()


def create_app(app_name='LIBRARY_API'):
    # instantiate flask app
    app = Flask(app_name)
    app.config.from_object('libraryapi.config.BaseConfig')

    # Allow cross-origin
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # database setup
    db.init_app(app)
    migrate.init_app(app, db)

    # register apps
    app.register_blueprint(auth.auth)
    app.register_blueprint(books.books)
    app.register_blueprint(journals.journals)

    return app
