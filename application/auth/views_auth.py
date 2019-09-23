from application import app, db
from flask import render_template, request, redirect, url_for
from application.auth.models_auth import User
from application.auth.forms_auth import LoginForm, RegisterForm
from flask_login import login_user, logout_user
from application.categories.models_categories import Category

@app.route("/auth/login", methods=["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", categories = Category.query.all(), form = LoginForm())

    form = LoginForm(request.form)

    user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
    if not user:
        return render_template("auth/loginform.html", categories = Category.query.all(), form = form,
                                error = "Virheellinen käyttäjänimi tai salasana")

    login_user(user)
    return redirect(url_for("index"))

@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/auth/register", methods=["GET", "POST"])
def auth_register():
    if request.method == "GET":
        return render_template("auth/registerform.html", categories = Category.query.all(), form = RegisterForm())

    form = RegisterForm(request.form)

    if not form.validate():
        return render_template("auth.registerform.html", categories = Category.query.all(), form = form)

    user = User(form.name.data, form.username.data, form.password.data, False)

    db.session().add(user)
    db.session().commit()

    return redirect(url_for("index", action_message = "Rekisteröitiin käyttäjä " + user.username))