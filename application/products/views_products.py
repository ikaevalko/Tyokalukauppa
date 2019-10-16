from application import app, db
from flask import render_template, request, redirect, url_for, session
from application.views_main import all_categories
from application.categories.models_categories import Category
from application.products.models_products import Product
from application.categories.views_categories import category_name_exists, category_id_exists
from sqlalchemy import exists
from application.products.forms_products import ProductFormNew, ProductFormUpdate
from flask_login import current_user, login_required
from decimal import Decimal

@app.route("/products/new/")
@login_required
def products_new():
    if not current_user.is_admin:
        return redirect(url_for("index"))

    form = ProductFormNew()
    form.category.choices = [(c.id, c.name) for c in all_categories()]

    return render_template("products/new_products.html", categories = all_categories(), form = form)

@app.route("/products/new/", methods=["POST"])
@login_required
def products_create():
    if not current_user.is_admin:
        return redirect(url_for("index"))

    form = ProductFormNew(request.form)
    form.category.choices = [(c.id, c.name) for c in all_categories()]

    # Validoidaan syöte
    if not form.validate():
        return render_template("products/new_products.html", categories = all_categories(), form = form)

    # Tarkistetaan lomakkeen kategorian olemassaolo
    if not category_id_exists(form.category.data):
        form.category.errors.append("Kategoriaa ei löytynyt")
        return render_template("products/new_products.html", categories = all_categories(), form = form)

    ctgr = db.session().query(Category).filter(Category.id == form.category.data).first()

    # Lisätään uusi tuote
    product = Product(form.name.data, form.desc.data, form.price.data, form.quantity.data, ctgr.id)

    db.session().add(product)
    db.session().commit()

    return redirect(url_for("index", action_message = "Lisättiin tuote " + product.name))

@app.route("/products/update/<product_id>/")
@login_required
def products_update_form(product_id):
    if not current_user.is_admin:
        return redirect(url_for("index"))

    form = ProductFormUpdate()

    # Tarkistetaan päivitettävän tuotteen olemassaolo
    if not product_id_exists(product_id):
        error_list = list(form.name.errors)
        error_list.append("Tuotetta ei löytynyt")
        form.name.errors = tuple(error_list)
        return render_template("products/update_products.html", categories = all_categories(), form = form, product_id = product_id)

    # Jos tuote löytyi, tuodaan sen nykyiset tiedot lomakkeelle
    old_product = db.session().query(Product).filter(Product.id == product_id).first()
    form.name.data = old_product.name
    form.desc.data = old_product.desc
    form.price.data = old_product.price
    form.quantity.data = old_product.quantity
    form.category.choices = [(c.id, c.name) for c in all_categories()]
    form.category.data = old_product.category_id

    return render_template("products/update_products.html", categories = all_categories(), form = form, product_id = product_id)

@app.route("/products/update/<product_id>/", methods=["POST"])
@login_required
def products_update(product_id):
    if not current_user.is_admin:
        return redirect(url_for("index"))

    updateForm = ProductFormUpdate(request.form)
    updateForm.category.choices = [(c.id, c.name) for c in all_categories()]

    # Validoidaan syöte
    if not updateForm.validate():
           return render_template("products/update_products.html", categories = all_categories(), form = updateForm, product_id = product_id)

    # Tarkistetaan lomakkeen kategorian olemassaolo
    if not category_id_exists(updateForm.category.data):
        updateForm.category.errors.append("Kategoriaa ei löytynyt")
        return render_template("products/update_products.html", categories = all_categories(), form = updateForm, product_id = product_id)

    # Päivitetään tuote
    ctgr = db.session().query(Category).filter(Category.id == updateForm.category.data).first()
    product = db.session().query(Product).filter(Product.id == product_id).first()
    product.name = updateForm.name.data
    product.desc = updateForm.desc.data
    product.price = updateForm.price.data
    product.quantity = updateForm.quantity.data
    product.category_id = ctgr.id
    db.session().commit()

    return redirect(url_for("index", action_message = "Päivitettiin tuote " + product.name))

@app.route("/products/delete/<product_id>")
@login_required
def products_delete(product_id):
    if not current_user.is_admin:
        return redirect(url_for("index"))

    # Tarkistetaan poistettavan tuotteen olemassaolo
    if product_id_exists(product_id):
        # Poistetaan tuote
        product = db.session().query(Product).filter(Product.id == product_id).first()
        db.session().delete(product)
        db.session().commit()
        return redirect(url_for("index", action_message = "Poistettiin tuote " + product.name))

    return redirect(url_for("index", action_message = "Tuotteen poistaminen epäonnistui"))

@app.route("/cart/add/<product_id>/")
@login_required
def add_product_to_cart(product_id):
    if current_user.is_admin:
        return redirect(url_for("index"))

    product = db.session().query(Product).filter(Product.id == product_id).first()
    amount = 1
    cartDict = {str(product.id) : {"name" : product.name, "price" : str(product.price), "amount" : str(amount)}}

    session.modified = True

    # Lisätään tuote ostoskoriin
    if "cart" not in session:
        session["cart"] = cartDict
    else:
        session["cart"].update(cartDict)

    return redirect(url_for("show_cart"))

@app.route("/cart/")
@login_required
def show_cart():
    if current_user.is_admin:
        return redirect(url_for("index"))

    if "cart" not in session:
        return render_template("orders/list_cart.html", categories = all_categories())

    total = 0
    values = []

    for value in session["cart"].values():
        values.append(Decimal(value["price"]))

    total = sum(values)

    return render_template("orders/list_cart.html", categories = all_categories(), products = session["cart"], total = total)

@app.route("/cart/empty/")
@login_required
def empty_cart():
    if current_user.is_admin:
        return redirect(url_for("index"))

    # Tyhjennetään ostoskori
    session.pop("cart", None)
    return redirect(url_for("index", action_message = "Tyhjennettiin ostoskori"))

def product_id_exists(id):
    return db.session().query(exists().where(Product.id == id)).scalar()