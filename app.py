from flask import Flask, request, jsonify
from models import db, Book
from schema import ma, BookSchema
from flask import render_template


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
ma.init_app(app)

book_schema = BookSchema()
books_schema = BookSchema(many=True)

# Create DB tables within application context
with app.app_context():
    db.create_all()

# Routes
@app.route("/books", methods=["POST"])
def add_book():
    data = request.json
    new_book = Book(
        title=data["title"],
        author=data["author"],
        isbn=data["isbn"],
        published_year=data["published_year"]
    )
    db.session.add(new_book)
    db.session.commit()
    return book_schema.jsonify(new_book), 201

@app.route("/books", methods=["GET"])
def get_books():
    books = Book.query.all()
    return books_schema.jsonify(books)

@app.route("/books/<int:id>", methods=["GET"])
def get_book(id):
    book = Book.query.get_or_404(id)
    return book_schema.jsonify(book)

@app.route("/books/<int:id>", methods=["PUT"])
def update_book(id):
    book = Book.query.get_or_404(id)
    data = request.json
    
    book.title = data.get("title", book.title)
    book.author = data.get("author", book.author)
    book.isbn = data.get("isbn", book.isbn)
    book.published_year = data.get("published_year", book.published_year)
    
    db.session.commit()
    return book_schema.jsonify(book)

@app.route("/books/<int:id>", methods=["DELETE"])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted"}), 204

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

