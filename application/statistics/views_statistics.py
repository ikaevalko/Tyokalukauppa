from application import app, db
from flask import render_template, redirect, url_for
from application.views_main import all_categories
from application.categories.models_categories import Category
from application.products.models_products import Product
from flask_login import login_required, current_user

@app.route("/statistics/")
@login_required
def list_statistics():
    if not current_user.is_admin:
        return redirect(url_for("index"))

    most_sold = Product.find_most_sold_products()
    least_sold = Product.find_least_sold_products()
    avg_prices = Category.find_average_prices_by_category()

    return render_template("statistics/list_statistics.html", categories = all_categories(),\
                            most_sold = most_sold, least_sold = least_sold, avg_prices = avg_prices)