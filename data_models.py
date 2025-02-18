from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'

    author_id = Column(Integer, primary_key=True, autoincrement=True)
    author_name = Column(String)
    birth_date = Column(Date)
    date_of_death = Column(Date)

    def __repr__(self):
        return f"Author(author_id = {self.author_id}, name = {self.author_name})"

class Book(db.Model):
    __tablename__ = 'books'

    book_id = Column(Integer, primary_key=True, autoincrement=True)
    book_isbn = Column(Integer)
    title = Column(String)
    publication_year = Column(Date)

    def __repr__(self):
        return f"Book(book_id = {self.book_id}, title = {self.title})"