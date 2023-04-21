from MT.setup import app, TDELTLOOKUP
from MT.models.models import Paper
from MT.arxiv.queryArxiv import is_paper_posted_today

from flask import jsonify
import datetime as dt
from sqlalchemy import and_

@app.route('/api/papers/all')
def papers_all():
    """
    Return all papers in the database
    """
    papers = Paper.query.all()
    papers = [paper.__dict__ for paper in papers]
    papers = [dict(filter(lambda x: x[0] != '_sa_instance_state', d.items())) for d in papers]
    return jsonify({'papers':papers})

@app.route('/api/papers/date/<date>')
def papers_date(date):
    """
    Return all papers in the database for a given date
    """
    papers = Paper.query.filter_by(published_date=date).all()
    papers = [paper.__dict__ for paper in papers]
    papers = [dict(filter(lambda x: x[0] != '_sa_instance_state', d.items())) for d in papers]
    return jsonify({'papers':papers})

@app.route('/api/papers/date/today')
def papers_date_today():
    """
    Return all papers in the database for today
    """
    papers = Paper.query.filter_by(published_date=dt.datetime.today().date()-dt.timedelta(1)).all()
    papers = [paper.__dict__ for paper in papers]
    papers = [dict(filter(lambda x: x[0] != '_sa_instance_state', d.items())) for d in papers]
    return jsonify({'papers':papers})

@app.route('/api/papers/date/latest')
def papers_date_latest():
    """
    Return all papers in the database for the latest date
    """
    TD = TDELTLOOKUP[dt.datetime.today().weekday()]
    papers = Paper.query.filter_by(published_date=dt.datetime.today().date()-dt.timedelta(TD)).all()
    papers = [paper.__dict__ for paper in papers]
    papers = [dict(filter(lambda x: x[0] != '_sa_instance_state', d.items())) for d in papers]
    return jsonify({'papers':papers})

@app.route('/api/papers/category/<category>')
def papers_category(category):
    """
    Return all papers in the database for a given category
    """
    papers = Paper.query.filter_by(subjects=category).all()
    papers = [paper.__dict__ for paper in papers]
    papers = [dict(filter(lambda x: x[0] != '_sa_instance_state', d.items())) for d in papers]
    return jsonify({'papers':papers})

@app.route('/api/papers/date/category/<date>/<category>')
def papers_date_category(date, category):
    """
    Return all papers in the database for a given date and a given category
    """
    papers = Paper.query.filter_by(published_date=date, subjects=category).all()
    papers = [paper.__dict__ for paper in papers]
    papers = [dict(filter(lambda x: x[0] != '_sa_instance_state', d.items())) for d in papers]
    return jsonify({'papers':papers})

@app.route('/api/papers/date/category/latest/<category>')
def papers_date_category_latest(category):
    """
    Return all papers in the database for the latest date and in a given category
    """
    papers = Paper.query.filter(
            Paper.subjects==category
    ).order_by(Paper.published_date.desc()).limit(200).all()
    papers = [paper.__dict__ for paper in papers if is_paper_posted_today(paper.published_date)]
    papers = [dict(filter(lambda x: x[0] != '_sa_instance_state', d.items())) for d in papers]
    return jsonify({'papers':papers})

@app.route('/api/papers/date/category/today/<category>')
def papers_date_category_today(category):
    """
    Return all papers in the database for today and in a given category
    """
    papers = Paper.query.filter_by(published_date=dt.datetime.today().date()-dt.timedelta(1), subjects=category).all()
    papers = [paper.__dict__ for paper in papers]
    papers = [dict(filter(lambda x: x[0] != '_sa_instance_state', d.items())) for d in papers]
    return jsonify({'papers':papers})

@app.route('/api/papers/id/<arxiv_id>')
def papers_id(arxiv_id):
    """
    Return a paper in the database for a given arxiv_id
    """
    paper = Paper.query.filter_by(arxiv_id=arxiv_id).first()
    paper = paper.__dict__
    paper = dict(filter(lambda x: x[0] != '_sa_instance_state', paper.items()))
    return jsonify({'paper':paper})

@app.route('/api/papers/title/<title>')
def papers_title(title):
    """
    Return all papers in the database for a given title
    """
    papers = Paper.query.filter_by(title=title).all()
    papers = [paper.__dict__ for paper in papers]
    papers = [dict(filter(lambda x: x[0] != '_sa_instance_state', d.items())) for d in papers]
    return jsonify({'papers':papers})
