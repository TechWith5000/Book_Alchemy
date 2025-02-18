from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/library.db'
db.init_app(app)


with app.app_context():
  db.create_all()

