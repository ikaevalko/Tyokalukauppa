from application import db
from sqlalchemy.sql import text

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), nullable=False)

    products = db.relationship("Product", cascade="all, delete-orphan", backref="category")

    def __init__(self, name):
        self.name = name

    @staticmethod
    def find_average_prices_by_category():
        stmt = text("SELECT category.name, ROUND(AVG(product.price), 2) FROM category"
                    " JOIN product ON category.id = product.category_id"
                    " GROUP BY category.name;")

        result = db.engine.execute(stmt)
        response = []

        for row in result:
            response.append((row[0], row[1]))

        return response