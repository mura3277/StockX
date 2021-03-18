from flask import render_template
from stockx import app, db
from stockx.forms import ShoeInsertForm
from stockx.models import Shoe


@app.route("/")
def index():
    return render_template("index.jinja")

@app.route("/items")
def items():
    return render_template("items.jinja", items=Shoe.query.all())

@app.route("/about")
def about():
    return render_template("about.jinja")

@app.route("/contact")
def contact():
    return render_template("contact.jinja")

@app.route("/cart")
def cart():
    return render_template("cart.jinja")

@app.route("/insert", methods=["GET", "POST"])
def insert():
    form = ShoeInsertForm()
    if form.validate_on_submit():
        shoe = Shoe()
        form.populate_obj(shoe)
        db.session.add(shoe)
        db.session.commit()
    return render_template("insert.jinja", form=form)