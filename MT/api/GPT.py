from MT.setup import app, db
from MT.models.models import Paper, User, Query
from MT.GPT.chat import ask
from MT.utils.auth import token_required
from MT.api.arxiv import fetch_arxiv_long_api

from flask import jsonify, request
import datetime as dt


@app.route('/api/gpt/summarize/<arxiv_id>')
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

@app.route('/api/gpt/summarize/<arxiv_id>/force')
@token_required
def summarize_force(current_user, arxiv_id):
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

@app.route('/api/gpt/summarize/<arxiv_id>/clear')
@token_required
def summarize_clear(current_user, arxiv_id):
    """
    Clear the stored GPT summary for a given arxiv_id.
    """
    paper = Paper.query.filter_by(arxiv_id=arxiv_id).first()

    paper.gpt_summary_long = None
    paper.gpt_summary_short = None
    db.session.commit()
    return jsonify({'summary':None})

@app.route('/api/gpt/query/simple/<arxiv_id>', methods=['POST'])
@token_required
def query_simple(current_user, arxiv_id):
    """
    Return a GPT answer for a given arxiv_id and question.
    Will not fetch the full page text if it has not been fetched before.
    """
    question = request.form['query']
    user = User.query.filter_by(uuid=current_user.uuid).first()
    user.num_queries += 1
    paper = Paper.query.filter_by(arxiv_id=arxiv_id).first()
    query = f"Please the most recent question about the following question about the paper titled {paper.title}. Previous questions and answers have been provided as context for you. {question}"
    paper.last_used = dt.datetime.now().date()
    answer = ask(query, document_id=arxiv_id)

    query = Query(user.uuid, paper.uuid, question, answer)
    db.session.add(query)
    db.session.commit()

    return jsonify({'query': question, 'answer':answer})

@app.route('/api/gpt/query/complex/<arxiv_id>', methods=['POST'])
@token_required
def query_complex(current_user, arxiv_id):
    """
    Return a GPT answer for a given arxiv_id and question.
    Will fetch the full page text if it has not been fetched before.
    """
    fetch_arxiv_long_api(arxiv_id)
    paper = Paper.query.filter_by(arxiv_id=arxiv_id).first()
    user = User.query.filter_by(uuid=current_user.uuid).first()
    user.num_queries += 1
    question = request.form['query']
    query = f"Please the most recent question about the following question about the paper titled {paper.title}. Previous questions and answers have been provided as context for you. {question}"
    paper.last_used = dt.datetime.now().date()

    answer = ask(query, document_id=arxiv_id)
    query = Query(user.uuid, paper.uuid, question, answer)
    db.session.add(query)
    db.session.commit()
    return jsonify({'query': question, 'answer':answer})

