from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import uri
import secrets

app = Flask(__name__)
app.config['SECRET_KEY']='d2abea1a8d8dfdf4c25f2dd3099463e1'
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


