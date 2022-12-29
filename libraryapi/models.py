"""
Data classes for the libraryapi application
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()



class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    books = db.relationship('Book', backref="users")
    journals = db.relationship('Journal', backref="users")
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    
    @property
    def is_admin(self):
        return self.id == 1

    @property
    def is_user(self):
        return self.id != 1

    def to_dict(self):
        return dict(id=self.id, username=self.username, email=self.email)


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    edition = db.Column(db.String(255))
    book_type = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def to_dict(self):
        return dict(id=self.id,
                    title=self.title,
                    edition=self.edition,
                    book_type=self.book_type,
                    user_id=self.user_id,
                    created_at=self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    updated_at=self.created_at.strftime('%Y-%m-%d %H:%M:%S'))


class Journal(db.Model):
    __tablename__ = 'journals'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    publisher = db.Column(db.String(500), nullable=False)
    publication_date = db.Column(db.String(100))
    first_author = db.Column(db.String(255), nullable=False)
    second_author = db.Column(db.String(255))
    last_author = db.Column(db.String(255))
    authors_shorten = db.Column(db.Text)
    url_to_journal = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def get_last_name(self, args):
        if args:
            return args.split()[-1].capitalize()
        return ""

    def generate_authors(self):
        f_author = self.get_last_name(self.first_author)
        s_author = self.get_last_name(self.second_author)
        l_author = self.get_last_name(self.last_author)

        if f_author != "" and s_author != "" and l_author != "":
            self.authors_shorten = f_author + " " + "et" + " .al"
        elif f_author != "" and s_author != "":
            self.authors_shorten = f_author + " and " + s_author
        else:
            self.authors_shorten = f_author
        return self.authors_shorten

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.authors_shorten = self.generate_authors()

    def to_dict(self):
        return dict(id=self.id,
                    title=self.title,
                    publisher=self.publisher,
                    publication_date=self.publication_date,
                    first_author=self.first_author,
                    second_author=self.second_author,
                    last_author=self.last_author,
                    authors_shorten=self.authors_shorten,
                    url_to_journal=self.url_to_journal,
                    user_id=self.user_id,
                    created_at=self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    updated_at=self.created_at.strftime('%Y-%m-%d %H:%M:%S'))
