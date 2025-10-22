from app import db
from typing import TypedDict
from datetime import date

class LivrosData(TypedDict):
    book_name: str
    publisher: str
    published_date: str
    author: str
    isbn: str

class Book(db.Model):
    __tablename__ = "livros"

    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String, nullable=False)
    publisher = db.Column(db.String, nullable=False)
    published_date = db.Column(db.Date, nullable=False)
    author = db.Column(db.String, nullable=False)
    isbn = db.Column(db.String, unique=True, nullable=False)

    def __init__(self, book_name, publisher, published_date, author, isbn):
        self.book_name = book_name
        self.publisher = publisher
        self.published_date = published_date
        self.author = author
        self.isbn = isbn

class authors_data(TypedDict):
    author_name: str
    birth_date: str
    nationality: str

class Author(db.Model):
    __tablename__ = "autores"
    id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String, nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    nationality = db.Column(db.String, nullable=True)

    def __init__(self, author_name, birth_date, nationality):
            self.author_name = author_name
            self.birth_date = birth_date
            self.nationality = nationality
    