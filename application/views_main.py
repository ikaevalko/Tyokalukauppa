from flask import render_template, request
from application import app
from application.categories.models_categories import Category

@app.route("/")
def index():
    return render_template("index.html", categories = Category.query.all(), message = request.args.get("action_message"))