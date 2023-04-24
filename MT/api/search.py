from MT.setup import app, db
from MT.search import relational
from MT.models.models import User

from flask import jsonify, request
import asyncio

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return jsonify({'message': 'Please use POST method to search.'})
    else:
        query = request.get_json()
        query = query['query']
        result = asyncio.run(relational.distribute_search(query))
        results = {
                'users': [x.to_dict() for x in result[0]],
                'papers': [x.to_dict() for x in result[1]],
                'authors': [x.to_dict() for x in result[2]],
                }
        return jsonify({'results': results}), 200

