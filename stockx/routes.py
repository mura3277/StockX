from flask import render_template, request
from werkzeug.exceptions import abort

from stockx import app, db
from stockx.forms import ShoeForm, SearchForm, AddCartForm, EmptyCartForm, RemCartForm, DecCartForm, IncCartForm
from stockx.helper import to_img64, update_cart, get_cart, purge_cart
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
@app.route("/items/<brand>", methods=["GET", "POST"])
def inventory(brand=None):
    # If brand exists, show brand specific entries
    if brand:
        return render("items.jinja", items=Shoe.query.filter_by(brand=brand).all())
    return render("items.jinja", items=Shoe.query.all())

@app.route("/item/<int:item_id>", methods=["GET", "POST"])
def item(item_id):
    cart_form = AddCartForm()
    item = Shoe.query.get_or_404(item_id)
    # If we are posting to this route and the cart form is valid, push item into the session cart
    if request.method == "POST" and cart_form.validate_on_submit():
        update_cart(item, cart_form.quantity.data)
    return render("item.jinja", item=item, cart_form=cart_form)

@app.route("/cart", methods=["GET", "POST"])
@app.route("/cart/<item_id>/<count>", methods=["GET", "POST"])
def cart(item_id=None, count=None):
    #If item_id and count exists, we are updating a specific cart entry
    if item_id and count:
        update_cart(Shoe.query.get_or_404(item_id), count, True)
    #Build the subtotal for rendering with Jinja
    subtotal = 0
    for i in get_cart():
        subtotal += (i["item"].price * i["quantity"])
    #Check if the user wants to clear the cart
    empty_cart_form = EmptyCartForm()
    if not item_id and request.method == "POST" and empty_cart_form.validate_on_submit():
        purge_cart()
    return render("cart.jinja", items=get_cart(), empty_cart_form=empty_cart_form, inc_cart_form=IncCartForm(), dec_cart_form=DecCartForm(), rem_cart_form=RemCartForm(), subtotal=subtotal)

@app.route("/about")
def about():
    return render("about.jinja")

@app.route("/contact")
def contact():
    return render("contact.jinja")

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