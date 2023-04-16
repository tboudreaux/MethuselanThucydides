from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import uri

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
