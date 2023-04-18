from flask import Flask, render_template, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import uri, masterHash
import bcrypt
from chat import ask
import datetime as dt
from flask import request
import arxiv
import tempfile
import pypdf
import os
from utils import upsert
import hashlib
import jwt
import secrets

from models import Paper, User, enroll_user
from setup import app, db
from auth import token_required

from queryArxiv import fetch_latest, fetch_arxix_id



@app.route('/')
def index():
    """
    Render the index page
    """
    return render_template("index.html")

# @app.route('/ui')
# def indexUI():
#     """
#     Render the index page
#     """
#     return render_template("indexBS.html")

@app.route('/api/online')
def online():
    """
    Check if the API is online
    """
    return jsonify({'online':True})

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
    if dt.datetime.today().weekday() == 5:
        TD = 2
    elif dt.datetime.today().weekday() == 6:
        TD = 3
    elif dt.datetime.today().weekday() == 0:
        TD = 3
    else:
        TD = 1
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
    if dt.datetime.today().weekday() == 5:
        TD = 2
    elif dt.datetime.today().weekday() == 6:
        TD = 3
    elif dt.datetime.today().weekday() == 0:
        TD = 3
    else:
        TD = 1
    papers = Paper.query.filter_by(published_date=dt.datetime.today().date()-dt.timedelta(TD), subjects=category).all()
    papers = [paper.__dict__ for paper in papers]
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

@app.route('/api/summarize/<arxiv_id>')
def summarize(arxiv_id):
    """
    Return a GPT summary for a given arxiv_id.
    If the paper has not been summarized before, it will be summarized and stored in the database.
    If the paper has been summarized before, the stored summary will be returned.
    """
    paper = Paper.query.filter_by(arxiv_id=arxiv_id).first()

    if paper is None:
        return jsonify({'summary':'Paper not found'})

    if paper.gpt_summary_long is not None:
        return jsonify({'summary':paper.gpt_summary_long})
    elif paper.gpt_summary_short is not None:
        return jsonify({'summary':paper.gpt_summary_short})
    else:
        query = f"Please summarize, in 1-2 sentences, the paper titled {paper.title}."
        gptResponse = ask(query)
        if paper.full_page_text is None:
            paper.gpt_summary_short = gptResponse
        else:
            paper.gpt_summary_long = gptResponse
            paper.gpt_summary_short = gptResponse
        db.session.commit()
        return jsonify({'summary':ask(query)})

@app.route('/api/summarize/<arxiv_id>/force')
@token_required
def summarize_force(arxiv_id):
    """
    Return a GPT summary for a given arxiv_id.
    If the paper has not been summarized before, it will be summarized and stored in the database.
    If the paper has been summarized before, the stored summary will be overwritten and a new summary will be returned.
    """
    paper = Paper.query.filter_by(arxiv_id=arxiv_id).first()

    query = f"Please summarize, in 1-2 sentences, the paper titled {paper.title}."
    gptResponse = ask(query)
    if paper.full_page_text is None:
        paper.gpt_summary_short = gptResponse
    else:
        paper.gpt_summary_long = gptResponse
        paper.gpt_summary_short = gptResponse
    db.session.commit()
    return jsonify({'summary':ask(query)})

@app.route('/api/summarize/<arxiv_id>/clear')
@token_required
def summarize_clear(arxiv_id):
    """
    Clear the stored GPT summary for a given arxiv_id.
    """
    paper = Paper.query.filter_by(arxiv_id=arxiv_id).first()

    paper.gpt_summary_long = None
    paper.gpt_summary_short = None
    db.session.commit()
    return jsonify({'summary':None})

@app.route('/api/query/simple/<arxiv_id>', methods=['POST'])
@token_required
def query_simple(arxiv_id):
    """
    Return a GPT answer for a given arxiv_id and question.
    Will not fetch the full page text if it has not been fetched before.
    """
    question = request.form['query']
    paper = Paper.query.filter_by(arxiv_id=arxiv_id).first()
    query = f"Please the most recent question about the following question about the paper titled {paper.title}. Previous questions and answers have been provided as context for you. {question}"
    paper.last_used = dt.datetime.now().date()
    db.session.commit()

    answer = ask(query, document_id=arxiv_id)
    return jsonify({'query': question, 'answer':answer})

@app.route('/api/query/complex/<arxiv_id>', methods=['POST'])
@token_required
def query_complex(current_user, arxiv_id):
    """
    Return a GPT answer for a given arxiv_id and question.
    Will fetch the full page text if it has not been fetched before.
    """
    fetch_arxiv_long_api(arxiv_id)
    paper = Paper.query.filter_by(arxiv_id=arxiv_id).first()
    user = User.query.filter_by(username=current_user.username).first()
    user.num_queries += 1
    question = request.form['query']
    query = f"Please the most recent question about the following question about the paper titled {paper.title}. Previous questions and answers have been provided as context for you. {question}"
    paper.last_used = dt.datetime.now().date()
    db.session.commit()

    answer = ask(query, document_id=arxiv_id)
    return jsonify({'query': question, 'answer':answer})

@app.route('/api/categories')
def categories():
    """
    Return all categories in the database
    """
    categories = Paper.query.with_entities(Paper.subjects).distinct().all()
    categories = [category[0] for category in categories]
    return jsonify({'categories':categories})

@app.route('/api/fetch/latest')
def fetch_latest_api():
    """
    Fetch the latest papers from arxiv and store them in the database.
    """
    fetchResult = fetch_latest()
    return jsonify(fetchResult)

@app.route('/api/fetch/ID/<arxiv_id>/short')
def fetch_arxiv_api(arxiv_id):
    """
    Fetch a paper from arxiv and store it in the database.
    Only fetch the basic information (title, author, abstract, subjects, etc.)
    not the full text.
    """
    fetchResult = fetch_arxix_id(arxiv_id)
    return jsonify(fetchResult)

@app.route('/api/fetch/ID/<arxiv_id>/long')
def fetch_arxiv_long_api(arxiv_id):
    """
    Fetch a paper from arxiv and store it in the database.
    Fetch the basic information (title, author, abstract, subjects, etc.)
    and the full text.
    """
    fetchResult = fetch_arxix_id(arxiv_id)
    try:
        load_full_text(arxiv_id)
        fetchResult['full_text'] = "Loaded full text"
    except Exception as e:
        fetchResult['full_text'] = "Failed to load full text"
        fetchResult['error'] = str(e)
    return jsonify(fetchResult)

def load_full_text(arxiv_id):
    """
    Load the full text of a paper from arxiv and store it in the database.

    Parameters
    ----------
        arxiv_id : str

    Returns
    -------
        None
    """
    paper = Paper.query.filter_by(arxiv_id=arxiv_id).first()
    if not paper.full_page_text:
        tmpDir = tempfile.TemporaryDirectory()
        locatePaper = arxiv.Search(
            id_list = [arxiv_id],
            max_results = 1,
            )
        singlePaper = next(locatePaper.results())
        singlePaper.download_pdf(tmpDir.name, "paper.pdf")

        reader = pypdf.PdfReader(os.path.join(tmpDir.name, "paper.pdf"))
        text = "Paper Title: " + paper.title + "\n"
        for page in reader.pages:
            text += page.extract_text()
        cleanText = text.replace("\x00", "")
        paper.full_page_text = cleanText
        upsert(arxiv_id, cleanText, paper.subjects)
        db.session.commit()
    else:
        print("Already have full text")

@app.route('/api/fetch/ID/<arxiv_id>/hasFullText')
def has_full_text(arxiv_id):
    """
    Check if a paper has full text stored in the database.
    """
    paper = Paper.query.filter_by(arxiv_id=arxiv_id).first()
    if paper.full_page_text:
        return jsonify({'hasFullText':True})
    else:
        return jsonify({'hasFullText':False})

@app.route('/api/user/enroll_user', methods=['POST'])
@token_required
def enroll_user_endpoint(current_user):
    payload = request.get_json()
    if current_user.admin:
        newUser = payload['new_user']
        newPass = payload['new_pass']
        newEmail = payload['new_email']
        newUserIsAdmin = payload['new_user_is_admin']
        newUserIsEnabled = payload['new_user_is_enabled']

        checkNewUser = User.query.filter_by(username=newUser).first()
        if checkNewUser is not None:
            return jsonify({'message':'User already exists'}), 409

        newUser = enroll_user(newUser, newEmail, newPass, admin=newUserIsAdmin, enabled=newUserIsEnabled)
        db.session.add(newUser)
        db.session.commit()
        # check if the new user is in the database
        checkNewUser = User.query.filter_by(username=newUser.username).first()
        if checkNewUser:
            return jsonify({'success':True}), 201
        else:
            return jsonify({'success':False}), 500
    elif not current_user.admin:
        return jsonify({'message':'User is not an admin'}), 401
    return jsonify({'message':'Unknown error'}), 500

@app.route('/login', methods=['POST'])
def login():
    token_valid_time = 30 # minutes
    payload = request.get_json()
    username = payload.get('username', None)
    email = payload.get('email', None)

    if not username and not email:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    ID = username if username else email
    if not payload or not ID or not payload['password']:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    if username:
        user = User.query.filter_by(username=ID).first()
    else:
        user = User.query.filter_by(email=ID).first()
    if user.check_password(payload['password']):
        token = jwt.encode({'public_id': user.username, 'exp': dt.datetime.utcnow() + dt.timedelta(minutes=token_valid_time)}, app.config['SECRET_KEY'])
        return jsonify({'token': token, 'expires': dt.datetime.utcnow() + dt.timedelta(minutes=token_valid_time)})
    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

@app.route('/login/test')
@token_required
def login_test(current_user):
    return jsonify({'message': 'Login successful', 'username': current_user.username, 'email': current_user.email, 'admin': current_user.admin, 'enabled': current_user.enabled, 'auth': True});

@app.route('/login/revoke/all', methods=['POST'])
def revoke_all_tokens():
    payload = request.get_json()
    username = payload.get('username', None)
    email = payload.get('email', None)

    if not username and not email:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    ID = username if username else email
    if not payload or not ID or not payload['password']:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    if username:
        user = User.query.filter_by(username=ID).first()
    else:
        user = User.query.filter_by(email=ID).first()
    if user.check_password(payload['password']):
        app.config['SECRET_KEY'] = secrets.token_hex(16)
        db.session.commit()
        return jsonify({'message': 'All tokens revoked'})
    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

if __name__ == '__main__':
    port = os.environ.get("FLASK_PORT", 5515)
    app.run("0.0.0.0", int(port), debug=True)

