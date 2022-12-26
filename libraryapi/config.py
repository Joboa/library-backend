""" 
settings for the flask application object
"""

import os
from dotenv import load_dotenv

load_dotenv()


class BaseConfig(object):
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get(
        'SQLALCHEMY_TRACK_MODIFICATIONS')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
