from MT.setup import app
from MT.config import catNameLookup
from MT.models.models import Paper, User
from MT.utils.auth import key_required

from flask import jsonify, request

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

@app.route('/api/utils/first_time_setup')
def first_time_setup():
    """
    Run the first time setup script.
    """
    # Count if there are any users in the database
    if User.query.count() == 0:
        return jsonify({'ft': True});
    else:
        return jsonify({'ft': False});

@app.route('/api/utils/apikey/verify')
@key_required
def verify_api_key(current_user):
    """
    Verify an API key
    """
    return jsonify({'valid':True, 'user': current_user.username}), 200
