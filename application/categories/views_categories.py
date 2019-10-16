from application import app, db
from flask import render_template, request, redirect, url_for
from application.views_main import all_categories
from application.categories.models_categories import Category
from application.products.models_products import Product
from sqlalchemy import exists, asc, desc
from application.categories.forms_categories import CategoryFormNew, CategoryFormUpdate, CategoryFormDelete
from application.forms_main import OrderByForm
from flask_login import current_user, login_required

@app.route("/categories/new/")
@login_required
def categories_new():
    if not admin():
        return redirect(url_for("index"))

    return render_template("categories/new_categories.html", categories = all_categories(), form = CategoryFormNew())

@app.route("/categories/new/", methods=["POST"])
@login_required
def categories_create():
    if not admin():
        return redirect(url_for("index"))

    form = CategoryFormNew(request.form)

    # Validoidaan syöte
    if not form.validate():
        return render_template("categories/new_categories.html", categories = all_categories(), form = form)

    # Estetään duplikaattien lisääminen
    if category_name_exists(form.name.data):
        form.name.errors.append("The database already contains a category named " + form.name.data)
        return render_template("categories/new_categories.html", categories = all_categories(), form = form)

    # Lisätään uusi kategoria
    ctgr = Category(form.name.data)

    db.session().add(ctgr)
    db.session().commit()

    return redirect(url_for("index", action_message = "Lisättiin kategoria " + ctgr.name))

@app.route("/categories/update/")
@login_required
def categories_update_form():
    if not admin():
        return redirect(url_for("index"))

    form = CategoryFormUpdate()
    form.categories.choices = [(c.id, c.name) for c in all_categories()]

    return render_template("categories/update_categories.html", categories = all_categories(), form = form)

@app.route("/categories/update/", methods=["POST"])
@login_required
def categories_update():
    if not admin():
        return redirect(url_for("index"))

    updateForm = CategoryFormUpdate(request.form)
    updateForm.categories.choices = [(c.id, c.name) for c in all_categories()]

    if not updateForm.validate():
        return render_template("categories/update_categories.html", categories = all_categories(), form = updateForm)

    # Tarkistetaan päivitettävän kategorian olemassaolo
    if category_id_exists(updateForm.categories.data):
        # Päivitetään kategoria
        ctgr = db.session().query(Category).filter(Category.id == updateForm.categories.data).first()
        ctgr.name = updateForm.newName.data
        db.session().commit()
        return redirect(url_for("index", action_message = "Päivitettiin kategoria " + ctgr.name))

    print(updateForm.categories.data)
    updateForm.categories.errors.append("Kategorian päivittäminen epäonnistui")
    return render_template("categories/update_categories.html", categories = all_categories(), form = updateForm)

@app.route("/categories/delete/")
@login_required
def categories_delete_form():
    if not admin():
        return redirect(url_for("index"))

    form = CategoryFormDelete()
    form.categories.choices = [(c.id, c.name) for c in all_categories()]

    return render_template("categories/delete_categories.html", categories = all_categories(), form = form)

@app.route("/categories/delete/", methods=["POST"])
@login_required
def categories_delete():
    if not admin():
        return redirect(url_for("index"))

    deleteForm = CategoryFormDelete(request.form)
    deleteForm.categories.choices = [(c.id, c.name) for c in all_categories()]

    # Tarkistetaan poistettavan kategorian olemassaolo
    if category_id_exists(deleteForm.categories.data):
        # Poistetaan kategoria
        ctgr = db.session().query(Category).filter(Category.id == deleteForm.categories.data).first()
        db.session().delete(ctgr)
        db.session().commit()
        return redirect(url_for("index", action_message = "Poistettiin kategoria " + ctgr.name))

    return render_template("categories/delete_categories.html", categories = all_categories(), form = CategoryFormDelete(), error = "Kategorian poistaminen epäonnistui")

@app.route("/categories/<category_id>/", methods=["GET", "POST"])
def category_show(category_id):
    if request.method == "GET":
        return render_template("index.html", categories = all_categories(),\
                                products = Product.query.filter(Product.category_id == category_id),\
                                order_by_form = OrderByForm(), ctgr_page = category_id, title = request.args.get("title"))

    order_by_form = OrderByForm(request.form)
    i = int(order_by_form.options.data)

    products = []

    if i is 0:
        products = Product.query.filter(Product.category_id == category_id)
    elif i is 1:
        products = Product.query.order_by(asc(Product.price)).filter(Product.category_id == category_id)
    elif i is 2:
        products = Product.query.order_by(desc(Product.price)).filter(Product.category_id == category_id)

    return render_template("index.html", categories = all_categories(), products = products,\
                            order_by_form = order_by_form, ctgr_page = category_id, title = request.args.get("title"))

def category_id_exists(id):
    return db.session().query(exists().where(Category.id == id)).scalar()

def category_name_exists(name):
    return db.session().query(exists().where(Category.name == name)).scalar()

def admin():
    if not current_user.is_admin:
        return False

    return True