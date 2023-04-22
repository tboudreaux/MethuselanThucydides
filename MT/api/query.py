from MT.setup import app, db
from MT.models.models import Query, User, Paper
from MT.utils.auth import token_required, auth_required

from flask import jsonify

@app.route('/api/query/all/user')
@auth_required
def get_all_queries_username(current_user):
    """
    Return all queries for a given user.
    """
    userQueries = current_user.queries
    arxivIDs = [query.paper.arxiv_id for query in userQueries]
    queryDict = [query.to_dict() for query, x in zip(userQueries, arxivIDs)]
    returnDict = dict()
    for query, arxivID in zip(queryDict, arxivIDs):
        if arxivID in returnDict:
            returnDict[arxivID].append(query)
        else:
            returnDict[arxivID] = [query]
    return jsonify({'queries':returnDict})

@app.route('/api/query/user')
@token_required
def get_query(current_user):
    """
    Return a query for a given user and paper.
    """
    uuid = current_user.uuid
    user = User.query.filter_by(uuid=uuid).first()
    userQueries = User.query.filter_by(uuid=uuid).first().queries
    queryDict = [query.to_dict() for query in userQueries]
    return jsonify({'queries':queryDict})

@app.route('/api/query/all/paper/<arxiv_id>')
@token_required
def get_all_queries_paper(current_user, arxiv_id):
    """
    Return all queries for a given paper.
    """
    paper = Paper.query.filter_by(arxiv_id=arxiv_id).first()
    if paper is None:
        return jsonify({'message':'Paper not found'})
    paperQueries = Paper.query.filter_by(arxiv_id=arxiv_id).first().queries
    return jsonify({'queries':[query.to_dict() for query in paperQueries]})

@app.route('/api/query/user/paper/<arxiv_id>')
@token_required
def get_all_queries_paper_user(current_user, arxiv_id):
    """
    Return a query for a given user and paper.
    """
    uuid = current_user.uuid
    paper = Paper.query.filter_by(arxiv_id=arxiv_id).first()
    if paper is None:
        return jsonify({'message':'Paper not found'})
    paper_uuid = paper.uuid
    queries = db.session.query(Query).filter_by(user_uuid=uuid, paper_uuid=paper_uuid).all()
    if queries is None:
        return jsonify({'message':'Query not found'})
    return jsonify({'queries': [query.to_dict() for query in queries]})
