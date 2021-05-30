from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired, Length

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