from MT.config import uri
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import secrets
import datetime as dt
from jinja2.utils import markupsafe
import os


app = Flask(__name__)
app.config['SECRET_KEY']='d2abea1a8d8dfdf4c25f2dd3099463e1'
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MT_NEW_USER_SECRET'] = os.environ.get('MT_NEW_USER_SECRET', None)

db = SQLAlchemy(app)

TDELTLOOKUP = {
    1: 1,
    2: 1,
    3: 1,
    4: 1,
    5: 2,
    6: 3,
    0: 3,
    }

app.jinja_env.globals['include_raw'] = lambda filename : markupsafe.Markup(app.jinja_loader.get_source(app.jinja_env, filename)[0])
