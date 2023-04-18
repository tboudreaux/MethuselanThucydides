from MT.config import uri
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import secrets
import datetime as dt


app = Flask(__name__)
app.config['SECRET_KEY']='d2abea1a8d8dfdf4c25f2dd3099463e1'
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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

