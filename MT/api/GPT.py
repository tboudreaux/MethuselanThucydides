from MT.setup import app, db, TDELTLOOKUP
from MT.models.models import Paper, User, Query
from MT.GPT.chat import ask, direct_ask
from MT.utils.auth import token_required, key_required
from MT.api.arxiv import fetch_arxiv_long_api
from MT.config import catNameLookup

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
        gptResponse = ask(query, document_id=arxiv_id)
        if paper.full_page_text is None:
            paper.gpt_summary_short = gptResponse
        else:
            paper.gpt_summary_long = gptResponse
            paper.gpt_summary_short = gptResponse
        db.session.commit()
        return jsonify({'summary':ask(query)})

@app.route('/api/gpt/summarize/all')
@key_required
def summarize_all(current_user):
    """
    Return a GPT summary for all papers.
    If the paper has not been summarized before, it will be summarized and stored in the database.
    If the paper has been summarized before, the stored summary will be returned.
    """
    papers = Paper.query.all()
    for paper in papers:
        if paper.gpt_summary_long is not None:
            continue
        elif paper.gpt_summary_short is not None:
            continue
        else:
            query = f"Please summarize, in 1-2 sentences, the paper titled {paper.title}."
            gptResponse = ask(query, document_id=paper.arxiv_id)
            if paper.full_page_text is None:
                paper.gpt_summary_short = gptResponse
            else:
                paper.gpt_summary_long = gptResponse
                paper.gpt_summary_short = gptResponse
            db.session.commit()
    return jsonify({'summary':'All papers summarized'})

@app.route('/api/gpt/summarize/latest')
@key_required
def summarize_latest(current_user):
    """
    Return a GPT summary for the latest papers.
    If the paper has not been summarized before, it will be summarized and stored in the database.
    If the paper has been summarized before, the stored summary will be returned.
    """
    TDELT = TDELTLOOKUP[dt.datetime.today().weekday()]
    papers = Paper.query.order_by(Paper.published_date.desc()).limit(500).all()
    summarized = list()
    for paper in papers:
        if paper.published_date < dt.date.today() - dt.timedelta(days=TDELT):
            print(f"Skipping {paper.arxiv_id} because it was published on {paper.published_date}") 
            continue
        if paper.gpt_summary_long is not None:
            print(f"Skipping {paper.arxiv_id} because it has already been summarized (long)")
            continue
        elif paper.gpt_summary_short is not None:
            print(f"Skipping {paper.arxiv_id} because it has already been summarized (short)")
            continue
        else:
            summarized.append(paper.arxiv_id)
            query = f"Please summarize, in 1-2 sentences, the paper titled {paper.title}."
            gptResponse = ask(query, document_id=paper.arxiv_id)
            if paper.full_page_text is None:
                paper.gpt_summary_short = gptResponse
            else:
                paper.gpt_summary_long = gptResponse
                paper.gpt_summary_short = gptResponse
            db.session.commit()
    return jsonify({'summary':'Latest papers summarized', 'papers':summarized})

@app.route('/api/gpt/summarize/missing')
@key_required
def summarize_missing(current_user):
    """
    Return a GPT summary for all papers that have not been summarized.
    If the paper has not been summarized before, it will be summarized and stored in the database.
    If the paper has been summarized before, the stored summary will be returned.
    """
    papers = Paper.query.filter_by(gpt_summary_short=None).all()
    for paper in papers:
        if paper.gpt_summary_long is not None:
            continue
        elif paper.gpt_summary_short is not None:
            continue
        else:
            query = f"Please summarize, in 1-2 sentences, the paper titled {paper.title}."
            gptResponse = ask(query, document_id=paper.arxiv_id)
            if paper.full_page_text is None:
                paper.gpt_summary_short = gptResponse
            else:
                paper.gpt_summary_long = gptResponse
                paper.gpt_summary_short = gptResponse
            db.session.commit()
    return jsonify({'summary':'Missing papers summarized'})

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

@app.route('/api/gpt/homepage')
def homepage():
    """
    Return a list of the most recent papers that have been summarized.
    """
    TDELT = TDELTLOOKUP[dt.date.today().weekday()]

    subjectSummaries = dict()
    for key, catName in catNameLookup.items():
        papers = Paper.query.filter(
                Paper.gpt_summary_short.isnot(None),
                Paper.subjects==key,
                Paper.published_date == (dt.date.today() - dt.timedelta(TDELT))
                ).all()
        papersDict = [paper.to_dict() for paper in papers]

        if len(papersDict) > 0:
            print(f"Summarizing {key}")
            subjectQuery = f"I have provided you summaries of the {len(papersDict)} paper(s) posted today in the field of {catName}. Using these, generate a breif (4-5) sentence summary of the overall research posted today"
            fullContextQuery = list()
            for paper in papersDict:
                fullContextQuery.append(f"Title {paper['title']}\nSummary {paper['gpt_summary_short']}\n")
            fullContextQuery.append(subjectQuery)
            subjectAnswer = direct_ask(fullContextQuery)
            subjectSummaries[key] = subjectAnswer
    return jsonify({'subjectSummaries':subjectSummaries})

