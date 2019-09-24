from application import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)

    products = db.relationship("Product", backref="category", lazy=True)

    def __init__(self, name):
        self.name = name