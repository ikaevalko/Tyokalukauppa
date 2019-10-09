from application import app, db
from flask import render_template, request, redirect, url_for, session
from application.categories.models_categories import Category
from application.products.models_products import Product
from application.categories.views_categories import category_exists
from sqlalchemy import exists
from application.products.forms_products import ProductFormNew, ProductFormUpdate, ProductFormDelete
from flask_login import current_user, login_required
from decimal import Decimal

@app.route("/products/new/")
@login_required
def products_new():
    if not current_user.is_admin:
        return redirect(url_for("index"))

    return render_template("products/new_products.html", categories = Category.query.all(), form = ProductFormNew())

@app.route("/products/new/", methods=["POST"])
@login_required
def products_create():
    if not current_user.is_admin:
        return redirect(url_for("index"))

    form = ProductFormNew(request.form)

    # Validoidaan syöte
    if not form.validate():
        return render_template("products/new_products.html", categories = Category.query.all(), form = form)

    # Tarkistetaan lomakkeen kategorian olemassaolo
    if not category_exists(form.category.data):
        form.category.errors.append("No such category found")
        return render_template("products/new_products.html", categories = Category.query.all(), form = form)

    ctgr = db.session().query(Category).filter(Category.name == form.category.data).first()

    # Lisätään uusi tuote
    product = Product(form.name.data, form.desc.data, form.price.data, form.quantity.data, ctgr.id)

    db.session().add(product)
    db.session().commit()

    return redirect(url_for("index", action_message = "Lisättiin tuote " + product.name))

@app.route("/products/update/")
@login_required
def products_update_get():
    if not current_user.is_admin:
        return redirect(url_for("index"))

    return render_template("products/update_products.html", categories = Category.query.all(), form = ProductFormUpdate(), valid_product = False)

@app.route("/products/update/form/", methods=["POST"])
@login_required
def products_update_form():
    if not current_user.is_admin:
        return redirect(url_for("index"))

    form = ProductFormUpdate(request.form)

    # Tarkistetaan päivitettävän tuotteen olemassaolo
    if not product_exists(form.oldName.data):
        error_list = list(form.oldName.errors)
        error_list.append("Tuotetta ei löytynyt")
        form.oldName.errors = tuple(error_list)
        return render_template("products/update_products.html", categories = Category.query.all(), form = form, valid_product = False)

    # Jos tuote löytyi, tuodaan sen nykyiset tiedot lomakkeelle
    old_product = db.session().query(Product).filter(Product.name == form.oldName.data).first()
    form.name.data = old_product.name
    form.desc.data = old_product.desc
    form.price.data = old_product.price
    form.quantity.data = old_product.quantity
    form.category.data = Category.query.filter(Category.id == old_product.category_id).first().name

    form.hiddenName.data = old_product.name

    return render_template("products/update_products.html", categories = Category.query.all(), form = form, valid_product = True)

@app.route("/products/update/", methods=["POST"])
@login_required
def products_update():
    if not current_user.is_admin:
        return redirect(url_for("index"))

    updateForm = ProductFormUpdate(request.form)

    # Validoidaan syöte
    if not updateForm.validate():
           return render_template("products/update_products.html", categories = Category.query.all(), form = updateForm, valid_product = True)

    # Tarkistetaan lomakkeen kategorian olemassaolo
    if not category_exists(updateForm.category.data):
        updateForm.category.errors.append("No such category found")
        return render_template("products/update_products.html", categories = Category.query.all(), form = updateForm, valid_product = True)

    # Päivitetään tuote
    ctgr = db.session().query(Category).filter(Category.name == updateForm.category.data).first()
    product = db.session().query(Product).filter(Product.name == updateForm.hiddenName.data).first()
    product.name = updateForm.name.data
    product.desc = updateForm.desc.data
    product.price = updateForm.price.data
    product.quantity = updateForm.quantity.data
    product.category_id = ctgr.id
    db.session().commit()

    return redirect(url_for("index", action_message = "Päivitettiin tuote " + product.name))

@app.route("/products/delete/")
@login_required
def products_delete_form():
    if not current_user.is_admin:
        return redirect(url_for("index"))

    return render_template("products/delete_products.html", categories = Category.query.all(), form = ProductFormDelete())

@app.route("/products/delete/", methods=["POST"])
@login_required
def products_delete():
    if not current_user.is_admin:
        return redirect(url_for("index"))

    deleteForm = ProductFormDelete(request.form)

    # Tarkistetaan poistettavan tuotteen olemassaolo
    if product_exists(deleteForm.name.data):
        # Poistetaan tuote
        product = db.session().query(Product).filter(Product.name == deleteForm.name.data).first()
        db.session().delete(product)
        db.session().commit()
        return redirect(url_for("index", action_message = "Poistettiin tuote " + product.name))

    return render_template("products/delete_products.html", categories = Category.query.all(), form = ProductFormDelete(), error = "Tuotteen poistaminen epäonnistui")

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
        return render_template("orders/list_cart.html", categories = Category.query.all())

    total = 0
    values = []

    for value in session["cart"].values():
        values.append(Decimal(value["price"]))

    total = sum(values)

    return render_template("orders/list_cart.html", categories = Category.query.all(), products = session["cart"], total = total)

@app.route("/cart/empty/")
@login_required
def empty_cart():
    if current_user.is_admin:
        return redirect(url_for("index"))

    # Tyhjennetään ostoskori
    session.pop("cart", None)
    return redirect(url_for("index", action_message = "Tyhjennettiin ostoskori"))

def product_exists(name):
    return db.session().query(exists().where(Product.name == name)).scalar()