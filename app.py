from flask import Flask, render_template, request, redirect, url_for, flash
from data_models import db, Author, Book
import os

app = Flask(__name__)
app.secret_key = "books_and_authors"  # Required for flash messages

# Database configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "data", "library.")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app
db.init_app(app)

'''# Run once at the start for populating the authors table, then mark this code as comment again
# Create an application context
with app.app_context():
    db.create_all()  # Ensures tables are created

    # Add an example author
    new_author = Author(name="J.K. Rowling", birth_date="1965-07-31")
    db.session.add(new_author)
    db.session.commit()'''


# Home route - Display books with sorting options
@app.route('/', methods=['GET', 'POST'])
def home():
    sort_by = request.args.get('sort_by', 'title')  # Default sorting by title
    search_query = request.form.get('search_query', '')  # Get search query from the form

    books_query = Book.query.join(Author)

    # Apply search filter if a query is provided
    if search_query:
        books_query = books_query.filter(Book.title.ilike(f"%{search_query}%"))

    # Apply sorting
    if sort_by == 'author':
        books = books_query.order_by(Author.name).all()
    else:
        books = books_query.order_by(Book.title).all()

    # Generate cover image URLs using Open Library API
    for book in books:
        if book.isbn:
            book.cover_url = f"https://covers.openlibrary.org/b/isbn/{book.isbn}-L.jpg"
        else:
            book.cover_url = None

    return render_template('home.html', books=books, search_query=search_query)


# Route to add a new author
@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        name = request.form['name']
        birth_date = request.form['birth_date']
        date_of_death = request.form.get('date_of_death', None)

        new_author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)
        db.session.add(new_author)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('add_author.html')


# Route to add a new book
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    authors = Author.query.all()

    if request.method == 'POST':
        title = request.form['title']
        author_id = request.form['author_id']
        isbn = request.form.get('isbn', None)
        publication_year = request.form.get('publication_year', None)

        new_book = Book(title=title, author_id=author_id, isbn=isbn, publication_year=publication_year)
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('add_book.html', authors=authors)


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)  # Fetch the book or return 404

    author = book.author  # Get the book's author
    db.session.delete(book)  # Delete the book
    db.session.commit()

    # Check if the author has any other books
    if not author.books:
        db.session.delete(author)  # Delete the author if they have no other books
        db.session.commit()

    flash(f'Book "{book.title}" has been deleted successfully!', 'success')  # Success message
    return redirect(url_for('home'))  # Redirect to homepage


# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)