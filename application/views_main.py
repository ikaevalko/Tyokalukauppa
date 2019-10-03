from flask import render_template, request
from application import app
from application.categories.models_categories import Category
from application.products.models_products import Product
from application.forms_main import OrderByForm
from sqlalchemy import asc, desc

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", categories = Category.query.all(), products = Product.query.limit(8).all(),\
                                message = request.args.get("action_message"), order_by_form = OrderByForm())

    order_by_form = OrderByForm(request.form)
    i = int(order_by_form.options.data)

    if i is 0:
        return render_template("index.html", categories = Category.query.all(), products = Product.query.limit(8).all(),\
                                message = request.args.get("action_message"), order_by_form = order_by_form)
    elif i is 1:
        return render_template("index.html", categories = Category.query.all(), products = Product.query.order_by(asc(Product.price)).all(),\
                                message = request.args.get("action_message"), order_by_form = order_by_form)
    elif i is 2:
        return render_template("index.html", categories = Category.query.all(), products = Product.query.order_by(desc(Product.price)).all(),\
                                message = request.args.get("action_message"), order_by_form = order_by_form)

    return render_template("index.html", categories = Category.query.all(), products = Product.query.limit(8).all(),\
                                message = request.args.get("action_message"), order_by_form = order_by_form)