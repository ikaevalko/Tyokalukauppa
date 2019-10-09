from application import app, db
from flask import render_template, redirect, url_for, request
from application.categories.models_categories import Category
from application.orders.models_orders import Order
from application.orders.forms_orders import OrderFormNew
from flask_login import login_required

@app.route("/orders/")
# LOGIN REQUIRED
def list_orders(account_id = 0):

    orders = db.session().query(Order).filter(Order.account_id == account_id)

    return render_template("orders/list_orders.html", categories = Category.query.all(), orders=orders)

@app.route("/orders/new/", methods=["GET", "POST"])
@login_required
def orders_new():

    if request.method == "GET":
        return render_template("orders/new_orders.html", categories = Category.query.all(), form = OrderFormNew())

    return render_template("orders/new_orders.html", categories = Category.query.all(), form = OrderFormNew())