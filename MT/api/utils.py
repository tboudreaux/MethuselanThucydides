from MT.setup import app
from MT.config import catNameLookup
from MT.models.models import Paper

from flask import jsonify

@app.route('/api/utils/categories')
def categories():
    """
    Return all categories in the database
    """
    return jsonify({'categories':catNameLookup})


@app.route('/api/utils/hasFullText/<arxiv_id>')
def has_full_text(arxiv_id):
    """
    Check if a paper has full text stored in the database.
    """
    paper = Paper.query.filter_by(arxiv_id=arxiv_id).first()
    if paper.full_page_text:
        return jsonify({'hasFullText':True})
    else:
        return jsonify({'hasFullText':False})
