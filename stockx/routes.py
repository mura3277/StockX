from flask import render_template, request
from werkzeug.exceptions import abort

from stockx import app, db
from stockx.forms import ShoeForm, SearchForm
from stockx.helper import to_img64
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
def inventory():
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

"""
Development route. Used for making inserting data easy

(None) -> template
"""
@app.route("/insert", methods=["GET", "POST"])
def insert():
    #Only allow this route in debug mode
    if not app.debug:
        abort(404)
    form = ShoeForm()
    if form.validate_on_submit():
        #Build and insert image files into kb object
        img64_small = to_img64(request.files["image"], 400)
        img64_large = to_img64(request.files["image"], -1)
        kb = Shoe(img_small=img64_small, img_large=img64_large)
        #Populate kb object with the data from the completed form
        form.populate_obj(kb)
        #Commit to the database
        db.session.add(kb)
        db.session.commit()
        return inventory()
    return render("insert.jinja", form=form)