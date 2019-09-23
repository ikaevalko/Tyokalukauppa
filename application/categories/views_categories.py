from application import app, db
from flask import render_template, request, redirect, url_for
from application.categories.models_categories import Category
from sqlalchemy import exists
from application.categories.forms_categories import CategoryFormNew, CategoryFormUpdate, CategoryFormDelete

@app.route("/categories", methods=["GET"])
def categories_index():
    return render_template("categories/list_categories.html", categories = Category.query.all(), message = request.args.get("action_message"))


@app.route("/categories/new/")
def categories_new():
    return render_template("categories/new_categories.html", categories = Category.query.all(), form = CategoryFormNew())

@app.route("/categories/new/", methods=["POST"])
def categories_create():
    form = CategoryFormNew(request.form)

    #Validoidaan syöte
    if not form.validate():
        return render_template("categories/new_categories.html", categories = Category.query.all(), form = form)

    # Lisätään uusi kategoria
    ctgr = Category(form.name.data)

    db.session().add(ctgr)
    db.session().commit()

    return redirect(url_for("index", action_message = "Lisättiin kategoria " + ctgr.name))

@app.route("/categories/update")
def categories_update_form():
    return render_template("categories/update_categories.html", categories = Category.query.all(), form = CategoryFormUpdate())

@app.route("/categories/update", methods=["POST"])
def categories_update():
    updateForm = CategoryFormUpdate(request.form)

    # Tarkistetaan päivitettävän kategorian olemassaolo
    if category_exists(updateForm.oldName.data):
        # Päivitetään kategoria
        ctgr = db.session().query(Category).filter(Category.name == updateForm.oldName.data).first()
        ctgr.name = updateForm.newName.data
        db.session().commit()
        return redirect(url_for("index", action_message = "Päivitettiin kategoria " + ctgr.name))

    return render_template("categories/update_categories.html", categories = Category.query.all(), form = CategoryFormUpdate(), error = "Kategorian päivittäminen epäonnistui")

@app.route("/categories/delete/")
def categories_delete_form():
    return render_template("categories/delete_categories.html", categories = Category.query.all(), form = CategoryFormDelete())

@app.route("/categories/delete/", methods=["POST"])
def categories_delete():
    deleteForm = CategoryFormDelete(request.form)

    # Tarkistetaan poistettavan kategorian olemassaolo
    if category_exists(deleteForm.name.data):
        # Poistetaan kategoria
        ctgr = db.session().query(Category).filter(Category.name == deleteForm.name.data).first()
        db.session().delete(ctgr)
        db.session().commit()
        return redirect(url_for("index", action_message = "Poistettiin kategoria " + ctgr.name))

    return render_template("categories/delete_categories.html", categories = Category.query.all(), form = CategoryFormDelete(), error = "Kategorian poistaminen epäonnistui")

def category_exists(name):
    return db.session().query(exists().where(Category.name == name)).scalar()