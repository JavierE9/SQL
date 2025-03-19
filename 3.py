from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
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
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    
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

# Rutas de la API
@app.route('/authors', methods=['GET'])
def get_all_authors():
    authors = Author.query.all()
    return jsonify([author.serialize() for author in authors])

@app.route('/books', methods=['GET'])
def get_all_books():
    books = Book.query.all()
    return jsonify([book.serialize() for book in books])

@app.route('/authors', methods=['POST'])
def create_author():
    data = request.get_json()
    new_author = Author(name=data['name'], nationality=data['nationality'])
    db.session.add(new_author)
    db.session.commit()
    return jsonify(new_author.serialize()), 201

@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    new_book = Book(title=data['title'], publication_year=data['publication_year'], author_id=data['author_id'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify(new_book.serialize()), 201

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True)
