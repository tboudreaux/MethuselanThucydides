from MT.models.models import User, Key
from MT.setup import app, db
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

def key_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        key = None
        if 'x-access-key' in request.headers:
            key = request.headers['x-access-key']

        if not key:
            print("No key")
            return jsonify({'message': 'a valid key is missing', 'auth': False}), 401
        keyUUID = key.split(":")[0]
        keyPlain = key.split(":")[1]
        key = db.session.query(Key).filter_by(uuid=keyUUID).first()
        if not key:
            print("Invalid key")
            return jsonify({'message': 'key is invalid', 'auth': False}), 401
        if not key.check_key(keyPlain):
            print("Invalid key")
            return jsonify({'message': 'key is invalid', 'auth': False}), 401
        current_user = db.session.query(User).filter_by(uuid=key.user_uuid).first()

        return f(current_user, *args, **kwargs)
    return decorator
