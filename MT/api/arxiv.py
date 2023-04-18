from MT.setup import app
from MT.arxiv.queryArxiv import fetch_latest
from MT.arxiv.queryArxiv import fetch_arxix_id
from MT.arxiv.queryArxiv import load_full_text

from flask import jsonify
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
