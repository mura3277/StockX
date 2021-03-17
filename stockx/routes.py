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

@app.route("/insert", methods=["GET", "POST"])
def insert():
    form = ShoeInsertForm()
    if form.validate_on_submit():
        shoe = Shoe()
        form.populate_obj(shoe)
        db.session.add(shoe)
        db.session.commit()
    return render_template("insert.jinja", form=form)