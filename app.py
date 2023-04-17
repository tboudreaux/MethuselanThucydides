from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import uri
from chat import ask
import datetime as dt
from flask import request
import arxiv
import tempfile
import pypdf
import os
from utils import upsert

from models import Paper
from setup import app, db

from queryArxiv import fetch_latest, fetch_arxix_id



@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/online')
def online():
    return jsonify({'online':True})

@app.route('/api/papers/all')
def papers_all():
    papers = Paper.query.all()
    papers = [paper.__dict__ for paper in papers]
    papers = [dict(filter(lambda x: x[0] != '_sa_instance_state', d.items())) for d in papers]
    return jsonify({'papers':papers})

@app.route('/api/papers/date/<date>')
def papers_date(date):
    papers = Paper.query.filter_by(published_date=date).all()
    papers = [paper.__dict__ for paper in papers]
    papers = [dict(filter(lambda x: x[0] != '_sa_instance_state', d.items())) for d in papers]
    return jsonify({'papers':papers})

@app.route('/api/papers/date/today')
def papers_date_today():
    papers = Paper.query.filter_by(published_date=dt.datetime.today().date()-dt.timedelta(1)).all()
    papers = [paper.__dict__ for paper in papers]
    papers = [dict(filter(lambda x: x[0] != '_sa_instance_state', d.items())) for d in papers]
    return jsonify({'papers':papers})

@app.route('/api/papers/date/latest')
def papers_date_latest():
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
    print(category)
    papers = Paper.query.filter_by(subjects=category).all()
    papers = [paper.__dict__ for paper in papers]
    papers = [dict(filter(lambda x: x[0] != '_sa_instance_state', d.items())) for d in papers]
    return jsonify({'papers':papers})

@app.route('/api/papers/date/category/<date>/<category>')
def papers_date_category(date, category):
    papers = Paper.query.filter_by(published_date=date, subjects=category).all()
    papers = [paper.__dict__ for paper in papers]
    papers = [dict(filter(lambda x: x[0] != '_sa_instance_state', d.items())) for d in papers]
    return jsonify({'papers':papers})

@app.route('/api/papers/date/category/latest/<category>')
def papers_date_category_latest(category):
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
    print(category)
    papers = Paper.query.filter_by(published_date=dt.datetime.today().date()-dt.timedelta(1), subjects=category).all()
    papers = [paper.__dict__ for paper in papers]
    papers = [dict(filter(lambda x: x[0] != '_sa_instance_state', d.items())) for d in papers]
    return jsonify({'papers':papers})

@app.route('/api/papers/id/<arxiv_id>')
def papers_id(arxiv_id):
    paper = Paper.query.filter_by(arxiv_id=arxiv_id).first()
    paper = paper.__dict__
    paper = dict(filter(lambda x: x[0] != '_sa_instance_state', paper.items()))
    return jsonify({'paper':paper})

@app.route('/api/papers/title/<title>')
def papers_title(title):
    papers = Paper.query.filter_by(title=title).all()
    papers = [paper.__dict__ for paper in papers]
    papers = [dict(filter(lambda x: x[0] != '_sa_instance_state', d.items())) for d in papers]
    return jsonify({'papers':papers})

@app.route('/api/summarize/<arxiv_id>')
def summarize(arxiv_id):
    paper = Paper.query.filter_by(arxiv_id=arxiv_id).first()

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
def summarize_force(arxiv_id):
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
def summarize_clear(arxiv_id):
    paper = Paper.query.filter_by(arxiv_id=arxiv_id).first()

    paper.gpt_summary_long = None
    paper.gpt_summary_short = None
    db.session.commit()
    return jsonify({'summary':None})

@app.route('/api/query/simple/<arxiv_id>', methods=['POST'])
def query_simple(arxiv_id):
    question = request.form['query']
    paper = Paper.query.filter_by(arxiv_id=arxiv_id).first()
    query = f"Please the most recent question about the following question about the paper titled {paper.title}. Previous questions and answers have been provided as context for you. {question}"
    paper.last_used = dt.datetime.now().date()
    db.session.commit()

    answer = ask(query, document_id=arxiv_id)
    return jsonify({'query': question, 'answer':answer})

@app.route('/api/query/complex/<arxiv_id>', methods=['POST'])
def query_complex(arxiv_id):
    fetch_arxiv_long_api(arxiv_id)
    paper = Paper.query.filter_by(arxiv_id=arxiv_id).first()
    question = request.form['query']
    query = f"Please the most recent question about the following question about the paper titled {paper.title}. Previous questions and answers have been provided as context for you. {question}"
    paper.last_used = dt.datetime.now().date()
    db.session.commit()

    answer = ask(query, document_id=arxiv_id)
    return jsonify({'query': question, 'answer':answer})

@app.route('/api/categories')
def categories():
    categories = Paper.query.with_entities(Paper.subjects).distinct().all()
    categories = [category[0] for category in categories]
    return jsonify({'categories':categories})

@app.route('/api/fetch/latest')
def fetch_latest_api():
    fetchResult = fetch_latest()
    return jsonify(fetchResult)

@app.route('/api/fetch/ID/<arxiv_id>/short')
def fetch_arxiv_api(arxiv_id):
    fetchResult = fetch_arxix_id(arxiv_id)
    return jsonify(fetchResult)

@app.route('/api/fetch/ID/<arxiv_id>/long')
def fetch_arxiv_long_api(arxiv_id):
    fetchResult = fetch_arxix_id(arxiv_id)
    try:
        load_full_text(arxiv_id)
        fetchResult['full_text'] = "Loaded full text"
    except Exception as e:
        fetchResult['full_text'] = "Failed to load full text"
        fetchResult['error'] = str(e)
    return jsonify(fetchResult)

def load_full_text(arxiv_id):
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
    paper = Paper.query.filter_by(arxiv_id=arxiv_id).first()
    if paper.full_page_text:
        return jsonify({'hasFullText':True})
    else:
        return jsonify({'hasFullText':False})

if __name__ == '__main__':
    port = os.environ.get("FLASK_PORT", 5515)
    app.run("0.0.0.0", int(port), debug=True)

