from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, FileField, IntegerField
from wtforms.validators import DataRequired, Length
from wtforms.widgets.html5 import NumberInput


class ShoeForm(FlaskForm):
    kw = {"title": "Shoe Form", "id": "item-form"}
    brand = StringField("Brand", validators=[DataRequired(), Length(min=2, max=64)])
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=64)])
    price = StringField("Price", validators=[DataRequired(), Length(min=2, max=64)])
    image = FileField("Image", validators=[FileAllowed(["jpg", "png", "webp"])])
    submit = SubmitField("Submit")

class SearchForm(FlaskForm):
    kw = {"id": "search-form", "ignore_labels": True}
    input = StringField("Search", validators=[DataRequired(), Length(min=2, max=64)])
    submit = SubmitField("Submit")

"""
A AddCartForm class, inheriting from FlaskForm
For rendering a cart to cart form on every item page
"""
class AddCartForm(FlaskForm):
    kw = {"id": "cart-form"}
    quantity = IntegerField(widget=NumberInput(min=1), default=1)
    submit = SubmitField("Add To Cart")

"""
A IncCartForm class, inheriting from FlaskForm
For rendering an increment item count button on every item in the user's cart
"""
class IncCartForm(FlaskForm):
    submit = SubmitField("+")

"""
A DecCartForm class, inheriting from FlaskForm
For rendering a decrement item count button on every item in the user's cart
"""
class DecCartForm(FlaskForm):
    submit = SubmitField("-")

"""
A RemCartForm class, inheriting from FlaskForm
For rendering a remove item button on every item in the user's cart
"""
class RemCartForm(FlaskForm):
    submit = SubmitField("Remove")

"""
A EmptyCartForm class, inheriting from FlaskForm
Quality of life button to clear the entire cart for the user
"""
class EmptyCartForm(FlaskForm):
    submit = SubmitField("Clear Cart")