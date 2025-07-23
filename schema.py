from flask_marshmallow import Marshmallow
from models import Book

ma = Marshmallow()

class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Book
        load_instance = True
