from models import User
from setup import app
from flask import jsonify, request
from functools import wraps
import jwt

def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
       token = None
       if 'x-access-tokens' in request.headers:
           token = request.headers['x-access-tokens']

       if not token:
           print("No token")
           return jsonify({'message': 'a valid token is missing', 'auth': False}), 401
       try:
           data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
           current_user = User.query.filter_by(username=data['public_id']).first()
       except:
           print("Invalid token")
           return jsonify({'message': 'token is invalid', 'auth': False}), 401

       return f(current_user, *args, **kwargs)
   return decorator
