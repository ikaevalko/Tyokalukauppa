from application import app, db
from flask import render_template, request, redirect, url_for
from application.categories.models_categories import Category
from application.products.models_products import Product
from sqlalchemy import exists
from application.categories.forms_categories import CategoryFormNew, CategoryFormUpdate, CategoryFormDelete
from flask_login import current_user, login_required

@app.route("/categories/new/")
@login_required
def categories_new():
    if not current_user.is_admin:
        return redirect(url_for("index"))

    return render_template("categories/new_categories.html", categories = Category.query.all(), form = CategoryFormNew())

@app.route("/categories/new/", methods=["POST"])
@login_required
def categories_create():
    if not current_user.is_admin:
        return redirect(url_for("index"))

    form = CategoryFormNew(request.form)

    # Validoidaan syöte
    if not form.validate():
        return render_template("categories/new_categories.html", categories = Category.query.all(), form = form)

    # Estetään duplikaattien lisääminen
    if category_exists(form.name.data):
        form.name.errors.append("The database already contains a category named " + form.name.data)
        return render_template("categories/new_categories.html", categories = Category.query.all(), form = form)

    # Lisätään uusi kategoria
    ctgr = Category(form.name.data)

    db.session().add(ctgr)
    db.session().commit()

    return redirect(url_for("index", action_message = "Lisättiin kategoria " + ctgr.name))

@app.route("/categories/update")
@login_required
def categories_update_form():
    if not current_user.is_admin:
        return redirect(url_for("index"))

    return render_template("categories/update_categories.html", categories = Category.query.all(), form = CategoryFormUpdate())

@app.route("/categories/update", methods=["POST"])
@login_required
def categories_update():
    if not current_user.is_admin:
        return redirect(url_for("index"))

    updateForm = CategoryFormUpdate(request.form)

    if not updateForm.validate():
        return render_template("categories/update_categories.html", categories = Category.query.all(), form = updateForm)

    # Tarkistetaan päivitettävän kategorian olemassaolo
    if category_exists(updateForm.oldName.data):
        # Päivitetään kategoria
        ctgr = db.session().query(Category).filter(Category.name == updateForm.oldName.data).first()
        ctgr.name = updateForm.newName.data
        db.session().commit()
        return redirect(url_for("index", action_message = "Päivitettiin kategoria " + ctgr.name))

    updateForm.oldName.errors.append("Kategorian päivittäminen epäonnistui")
    return render_template("categories/update_categories.html", categories = Category.query.all(), form = updateForm)

@app.route("/categories/delete/")
@login_required
def categories_delete_form():
    if not current_user.is_admin:
        return redirect(url_for("index"))

    return render_template("categories/delete_categories.html", categories = Category.query.all(), form = CategoryFormDelete())

@app.route("/categories/delete/", methods=["POST"])
@login_required
def categories_delete():
    if not current_user.is_admin:
        return redirect(url_for("index"))

    deleteForm = CategoryFormDelete(request.form)

    # Tarkistetaan poistettavan kategorian olemassaolo
    if category_exists(deleteForm.name.data):
        # Poistetaan kategoria
        ctgr = db.session().query(Category).filter(Category.name == deleteForm.name.data).first()
        db.session().delete(ctgr)
        db.session().commit()
        return redirect(url_for("index", action_message = "Poistettiin kategoria " + ctgr.name))

    return render_template("categories/delete_categories.html", categories = Category.query.all(), form = CategoryFormDelete(), error = "Kategorian poistaminen epäonnistui")

@app.route("/categories/<category_id>/")
def category_show(category_id):
    category_products = Product.query.filter(Product.category_id == category_id).limit(8)

    return render_template("index.html", categories = Category.query.all(), products = category_products, title = request.args.get("title"))

def category_exists(name):
    return db.session().query(exists().where(Category.name == name)).scalar()