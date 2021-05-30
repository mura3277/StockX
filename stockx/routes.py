from flask import render_template
from stockx import app, db
from stockx.forms import ShoeInsertForm, SearchForm
from stockx.models import Shoe

def render(template, **kwargs):
    search_form = SearchForm()
    if search_form.validate_on_submit():
        items = Shoe.query.filter(Shoe.name.contains(search_form.input.data)).all()
        return render_template("items.jinja", search_form=search_form, items=items)
    else:
        return render_template(template, search_form=search_form, **kwargs)

@app.route("/")
def index():
    return render("index.jinja")

@app.route("/items", methods=["GET", "POST"])
def items():
    return render("items.jinja", items=Shoe.query.all())

@app.route("/about")
def about():
    return render("about.jinja")

@app.route("/contact")
def contact():
    return render("contact.jinja")

@app.route("/cart")
def cart():
    return render("cart.jinja")

@app.route("/insert", methods=["GET", "POST"])
def insert():
    form = ShoeInsertForm()
    if form.validate_on_submit():
        shoe = Shoe()
        form.populate_obj(shoe)
        db.session.add(shoe)
        db.session.commit()
    return render_template("insert.jinja", form=form)