from flask import render_template
from stockx import app

@app.route("/")
def index():
    return render_template("index.jinja")