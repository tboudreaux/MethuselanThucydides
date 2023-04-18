from MT.setup import app

from flask import render_template

@app.route('/')
def index():
    """
    Render the index page
    """
    return render_template("index.html")
