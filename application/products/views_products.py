from application import app, db
from flask import render_template, request, redirect, url_for
from application.categories.models_categories import Category
from application.products.models_products import Product
from application.categories.views_categories import category_exists
from sqlalchemy import exists
from application.products.forms_products import ProductFormNew, ProductFormUpdate, ProductFormDelete
from flask_login import current_user, login_required

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

#@app.route("/products/update")
#@login_required
#def products_update_form():
#    if not current_user.is_admin:
#        return redirect(url_for("index"))
#
#    return render_template("products/update_products.html", categories = Category.query.all(), form = ProductFormUpdate())
#
#@app.route("/products/update", methods=["POST"])
#@login_required
#def products_update():
#    if not current_user.is_admin:
#        return redirect(url_for("index"))
#
#    updateForm = ProductFormUpdate(request.form)
#
#    # Tarkistetaan päivitettävän tuotteen olemassaolo
#    if product_exists(updateForm.oldName.data):
#        # Päivitetään tuote
#        product = db.session().query(Product).filter(Product.name == updateForm.oldName.data).first()
#        product.name = updateForm.newName.data
#        db.session().commit()
#        return redirect(url_for("index", action_message = "Päivitettiin tuote " + product.name))
#
#    return render_template("products/update_products.html", categories = Category.query.all(), form = ProductFormUpdate(), error = "Tuotteen päivittäminen epäonnistui")

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

def product_exists(name):
    return db.session().query(exists().where(Product.name == name)).scalar()