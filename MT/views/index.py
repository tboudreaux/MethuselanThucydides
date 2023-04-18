from MT.setup import app

from flask import render_template

@app.route('/classic')
def index():
    """
    Render the index page
    """
    return render_template("index.html")

@app.route('/')
def ui():
    """
    Render the UI page
    """
    return render_template("indexUI.html")
