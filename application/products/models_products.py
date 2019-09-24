from application import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    desc = db.Column(db.Text, nullable=False)
    price = db.Column(db.Numeric(6, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)

    def __init__(self, name, desc, price, quantity, category_id):
        self.name = name
        self.desc = desc
        self.price = price
        self.quantity = quantity
        self.category_id = category_id