from application import app, db
from flask import render_template, redirect, url_for, request, session
from application.views_main import all_categories
from application.categories.models_categories import Category
from application.products.models_products import Product
from application.orders.models_orders import Order, OrderProduct
from application.orders.forms_orders import OrderFormNew
from sqlalchemy import desc
from flask_login import login_required, current_user

@app.route("/orders/")
@login_required
def list_orders():
    if admin():
        return render_template("orders/list_orders.html", categories = all_categories(), orders = Order.query.all())

    orders = db.session().query(Order).filter(Order.account_id == current_user.id)

    return render_template("orders/list_orders.html", categories = all_categories(), orders=orders)

@app.route("/orders/<order_id>")
@login_required
def show_order(order_id):
    if not admin():
        user_id = Order.query.filter(Order.id == order_id).first().account_id
        if user_id is not current_user.id:
            return redirect(url_for("index"))

    result = db.session().query(Order).join(OrderProduct).join(Product).filter(Order.id == order_id)

    return render_template("orders/show_order.html", categories = all_categories(), order_id = order_id, rows = result)

@app.route("/orders/new/", methods=["GET", "POST"])
@login_required
def orders_new():
    if admin() or "cart" not in session:
        return redirect(url_for("index"))

    if request.method == "GET":
        return render_template("orders/new_orders.html", categories = all_categories(), form = OrderFormNew())

    form = OrderFormNew(request.form)

    # Validoidaan syöte
    if not form.validate():
        return render_template("orders/new_orders.html", categories = all_categories(), form = form)

    # Luodaan uusi tilaus
    new_order = Order(form.address.data, form.postal_code.data, form.city.data, current_user.id)
    new_order.completed = False

    db.session().add(new_order)
    db.session().commit()

    order_id = Order.query.order_by(Order.id.desc()).first().id

    for key in session["cart"]:
        orderProduct = OrderProduct(order_id, int(key), int(session["cart"][key]["amount"]))
        db.session().add(orderProduct)

    db.session().commit()

    session.pop("cart", None)

    return redirect(url_for("index", action_message = "Tilaus lähetetty"))

@app.route("/orders/<order_id>/completed/")
@login_required
def order_change_completed_status(order_id):
    if not admin():
        return redirect(url_for("index"))

    order = Order.query.filter(Order.id == order_id).first()

    if order is not None:
        # Merkitään tilaus suoritetuksi tai päinvastoin
        order.completed = not order.completed
        db.session().commit()
        return redirect(url_for("list_orders"))

    return redirect(url_for("index"))

def admin():
    if not current_user.is_admin:
        return False

    return True