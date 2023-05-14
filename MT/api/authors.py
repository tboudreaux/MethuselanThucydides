from MT.setup import app
from MT.utils.auth import auth_requested
from MT.models.models import Author, Paper

from flask import jsonify
import datetime as dt

@app.route('/api/authors/all')
def authors_all():
    """
    Return all authors in the database
    """
    authors = Author.query.all()
    authors = [author.__dict__ for author in authors]
    authors = [dict(filter(lambda x: x[0] != '_sa_instance_state', d.items())) for d in authors]
    return jsonify({'authors':authors})

# Return all the authors of a given paper
@app.route('/api/authors/paper/<arxiv_id>')
def authors_paper(arxiv_id):
    """
    Return all the authors of a given paper
    """
    authors = Paper.query.filter_by(arxiv_id=arxiv_id).first().authors
    authors = [
            {
                'fullname': " ".join(author.full_name),
                'firstname': author.first_name,
                'uuid': author.uuid,
            }
            for author in authors
            ]
    return jsonify({'authors':authors})

@app.route('/api/authors/uuid/<uuid>')
@auth_requested
def authors_uuid(current_user, uuid):
    """
    Return all the papers written by a given author and 
    the queries made by the current user

    Also return all author information
    """
    papers = Author.query.filter_by(uuid=uuid).first().papers
    currentUUID = current_user.uuid if current_user else None
    papers = [
            {
                'title': paper.title,
                'arxiv_id': paper.arxiv_id,
                'published_date': paper.published_date,
                'abstract': paper.abstract,
                'subjects': paper.subjects,
                'authors': [
                    {
                        'fullname': " ".join(author.full_name),
                        'firstname': author.first_name,
                        'uuid': author.uuid,
                        }
                    for author in paper.authors
                    ],
                'gpt-summary-short': paper.gpt_summary_short,
                'gpt-summary-long': paper.gpt_summary_long,
                'queries': [
                    {
                        'query': query.query,
                        'response': query.response,
                        'chunks': query.chunks,
                        'created_at': query.created_at,
                    }
                    for query in paper.queries if query.user_uuid == currentUUID
                    ],

            }
            for paper in papers
            ]
    info = Author.query.filter_by(uuid=uuid).first().to_dict()
    return jsonify({'papers':papers, 'info':info})

