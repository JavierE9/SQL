from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import  Integer, String, ForeignKey
from sqlalchemy.orm import relationship

# Configuración de Flask y base de datos
app = Flask(__name__)

# URI de la base de datos MySQL en localhost
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/test'  # Base de datos en localhost
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desactivar seguimiento de modificaciones (opcional)
db = SQLAlchemy(app)

# Definición de modelos

class Author(db.Model):
    __tablename__ = 'author'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    nationality = db.Column(db.String(100), nullable=False)
    
    # Relación con Book
    books = db.relationship("Book", back_populates="author")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "nationality": self.nationality,
        }

class Book(db.Model):
    __tablename__ = 'book'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.name'))
    
    # Relación inversa con Author
    author = db.relationship("Author", back_populates="books")

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "publication_year": self.publication_year,
            "author_id": self.author_id,
        }

# Crear las tablas
with app.app_context():
    db.create_all()

