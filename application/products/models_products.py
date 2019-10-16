from application import db
from sqlalchemy.sql import text

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Numeric(6, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=True)

    orders = db.relationship("Order", secondary="order_product")

    def __init__(self, name, description, price, quantity, category_id):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
        self.category_id = category_id

    @staticmethod
    def find_most_sold_products():
        stmt = text("SELECT product.name, product.price, COUNT(orders.id) AS amount_sold FROM product"
                    " JOIN order_product ON product.id = order_product.product_id"
                    " JOIN orders on order_product.order_id = orders.id"
                    " GROUP BY product.name"
                    " ORDER BY amount_sold DESC;")

        result = db.engine.execute(stmt)
        response = []
        num_of_rows = 10

        for row in result:
            if num_of_rows <= 0:
                break

            response.append((row[0], row[1], row[2]))
            num_of_rows -= 1

        return response

    @staticmethod
    def find_least_sold_products():
        stmt = text("SELECT product.name, product.price, COUNT(orders.id) AS amount_sold FROM product"
                    " JOIN order_product ON product.id = order_product.product_id"
                    " JOIN orders on order_product.order_id = orders.id"
                    " GROUP BY product.name"
                    " ORDER BY amount_sold ASC;")

        result = db.engine.execute(stmt)
        response = []
        num_of_rows = 10

        for row in result:
            if num_of_rows <= 0:
                break

            response.append((row[0], row[1], row[2]))
            num_of_rows -= 1

        return response