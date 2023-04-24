from MT.setup import app, db
from MT.search import relational
from MT.models.models import User
from MT.utils.auth import auth_requested

from flask import jsonify, request
import asyncio

@app.route('/search', methods=['GET', 'POST'])
@auth_requested
def search(current_user):
    if request.method == 'GET':
        return jsonify({'message': 'Please use POST method to search.'})
    else:
        query = request.get_json()
        query = query['query']
        if current_user != None:
            isAdmin = current_user.admin
        else:
            isAdmin = False
        result = asyncio.run(relational.distribute_search(query))
        results = {
                'users': [x.to_dict() for x in result[0]],
                'papers': [x.to_dict() for x in result[1]],
                'authors': [x.to_dict() for x in result[2]],
                }
        if not isAdmin:
            results.pop('users')
        return jsonify({'results': results}), 200

