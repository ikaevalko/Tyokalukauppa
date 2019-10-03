from application import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), nullable=False)

    products = db.relationship("Product", cascade="all, delete-orphan", backref="category")

    def __init__(self, name):
        self.name = name