from flask import render_template, request
from application import app
from application.categories.models_categories import Category
from application.products.models_products import Product

@app.route("/")
def index():
    return render_template("index.html", categories = Category.query.all(), products = Product.query.limit(8).all(), message = request.args.get("action_message"))