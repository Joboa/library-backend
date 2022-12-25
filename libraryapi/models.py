"""
Data classes for the libraryapi application
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    edition = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return dict(id=self.id,
                    title=self.title,
                    edition=self.edition,
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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

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
                    created_at=self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    updated_at=self.created_at.strftime('%Y-%m-%d %H:%M:%S'))

# class Admin(db.Model):
#   pass


# class User(db.Model):
#   pass
