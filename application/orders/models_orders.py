from application import db

orderProduct = db.Table("orderProduct",\
                        db.Column("order_id", db.Integer, db.ForeignKey("order.id"), primary_key=True),\
                        db.Column("product_id", db.Integer, db.ForeignKey("product.id"), primary_key=True),\
                        db.Column("amount", db.Integer, nullable=False))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=db.func.current_date())
    address = db.Column(db.String(32), nullable=False)
    postal_code = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(32), nullable=False)
    completed = db.Column(db.Boolean, nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey("account.id"))

    products = db.relationship("Product", secondary=orderProduct, backref="orders")

    def __init__(self, address, postal_code, city, account_id):
        self.account_id = account_id
        self.address = address
        self.postal_code = postal_code
        self.city = city