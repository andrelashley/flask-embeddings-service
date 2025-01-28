from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import UserDefinedType

# Initialize SQLAlchemy instance (to be imported in app.py)
db = SQLAlchemy()


class VectorType(UserDefinedType):
    def get_col_spec(self, **kwargs):
        return "vector"

    def bind_expression(self, bindvalue):
        return bindvalue

    def column_expression(self, col):
        return col

    def bind_processor(self, dialect):
        def process(value):
            if value is not None:
                return list(value)  # Convert to a list before inserting
            return value
        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            if value is not None:
                return list(value)  # Convert database array to Python list
            return value
        return process


# Define the Item model
class Item(db.Model):
    __tablename__ = 'Items'  # Ensure this matches your database table name

    ItemId = db.Column(db.Integer, primary_key=True)
    Text = db.Column(db.String, nullable=False)
    Embedding = db.Column(VectorType)  # Represent the vector as an array of floats
