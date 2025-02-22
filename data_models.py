from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship

# Initialize SQLAlchemy
db = SQLAlchemy()


class Author(db.Model):
    """
    Represents an author in the database.

    Attributes:
        author_id (int): The unique identifier for the author.
        name (str): The name of the author.
        birth_date (str): The birth date of the author.
        date_of_death (str): The date of death of the author (if applicable).
        books (relationship): The relationship to the Book model.
    """
    __tablename__ = "authors"

    # Columns for the "authors" table
    author_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)  # Name cannot be null
    birth_date = Column(String)
    date_of_death = Column(String)

    # Relationship to Book
    books = relationship("Book", back_populates="author")

    def __repr__(self):
        """
        Official representation of the object (for debugging).

        Returns:
            str: A string representation of the Author object.
        """
        return f"Author(id={self.author_id}, name={self.name})"

    def __str__(self):
        """
        User-friendly representation of the object (for print/str).

        Returns:
            str: The name of the Author.
        """
        return self.name


class Book(db.Model):
    """
    Represents a book in the database.

    Attributes:
        book_id (int): The unique identifier for the book.
        author_id (int): The unique identifier of the associated author.
        isbn (str): The ISBN of the book.
        title (str): The title of the book.
        publication_year (int): The year the book was published.
        author (relationship): The relationship to the Author model.
    """
    __tablename__ = "books"

    # Columns for the "books" table
    book_id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(Integer, ForeignKey("authors.author_id"), nullable=False)
    isbn = Column(String)
    title = Column(String, nullable=False)  # Title cannot be null
    publication_year = Column(Integer)

    # Relationship to Author
    author = relationship("Author", back_populates="books")

    def __repr__(self):
        """
        Official representation of the object (for debugging).

        Returns:
            str: A string representation of the Book object.
        """
        return f"Book(id={self.book_id}, title={self.title})"

    def __str__(self):
        """
        User-friendly representation of the object (for print/str).

        Returns:
            str: The title of the Book.
        """
        return self.title