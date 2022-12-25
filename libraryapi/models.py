from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Book(db.Model):
  id = db.Column(db.Integer, primary_key=True)


# class Journal(db.Model):
#   pass


# class Admin(db.Model):
#   pass


# class User(db.Model):
#   pass