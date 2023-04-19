from MT.setup import db, app
from MT.models.models import User, Paper, Category, Summary

from flask import jsonify, make_response, request
import datetime as dt

@app.route('/api/category/summary/today')
def category_summary_today():
    """
    Return a summary of papers added today.
    """
    papers = Paper.query.filter_by(date_added=dt.date.today()).all()
    return jsonify({'papers':papers})
