from MT.models.models import User, Key
from MT.setup import app, db

from flask import jsonify, request
from functools import wraps
import jwt
import datetime

def update_current_user(current_user):
    current_user.last_ip = request.remote_addr
    current_user.last_login = datetime.datetime.now()
    current_user.num_logins += 1
    current_user.last_user_agent = request.user_agent.string

    db.session.commit()


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
       update_current_user(current_user)

       return f(current_user, *args, **kwargs)
   return decorator

def token_requested(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        current_user = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
        else:
            print("No Token")
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(username=data['public_id']).first()
        except:
            print("Invalid token")

        update_current_user(current_user)
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
        update_current_user(current_user)

        return f(current_user, *args, **kwargs)
    return decorator

def key_requested(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        key = None
        current_user = None
        if 'x-access-key' in request.headers:
            key = request.headers['x-access-key']
            keyUUID = key.split(":")[0]
            keyPlain = key.split(":")[1]
            key = db.session.query(Key).filter_by(uuid=keyUUID).first()
            if not key:
                print("Invalid key")
                return f(current_user, *args, **kwargs)
            if not key.check_key(keyPlain):
                print("Invalid key")
                return f(current_user, *args, **kwargs)
            current_user = db.session.query(User).filter_by(uuid=key.user_uuid).first()
        else:
            print("No key")

        update_current_user(current_user)
        return f(current_user, *args, **kwargs)
    return decorator

def user_pass_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        user = None
        password = None
        if 'x-access-user' in request.headers:
            user = request.headers['x-access-user']
        if 'x-access-pass' in request.headers:
            password = request.headers['x-access-pass']

        if not user:
            print("No user")
            return jsonify({'message': 'a valid user is missing', 'auth': False}), 401
        if not password:
            print("No password")
            return jsonify({'message': 'a valid password is missing', 'auth': False}), 401
        user = db.session.query(User).filter_by(username=user).first()
        if not user:
            print("Invalid user")
            return jsonify({'message': 'user is invalid', 'auth': False}), 401
        if not user.check_password(password):
            print("Invalid user")
            return jsonify({'message': 'user is invalid', 'auth': False}), 401
        current_user = user
        update_current_user(current_user)

        return f(current_user, *args, **kwargs)
    return decorator

def user_pass_requested(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        user = None
        password = None
        current_user = None
        if 'x-access-user' in request.headers:
            user = request.headers['x-access-user']
        if 'x-access-pass' in request.headers:
            password = request.headers['x-access-pass']

        if not user:
            print("No user")
            return f(current_user, *args, **kwargs)
        if not password:
            print("No password")
            return f(current_user, *args, **kwargs)
        user = db.session.query(User).filter_by(username=user).first()
        if not user:
            print("Invalid user")
            return f(current_user, *args, **kwargs)
        if not user.check_password(password):
            print("Invalid password")
            return f(current_user, *args, **kwargs)
        current_user = user
        update_current_user(current_user)

        return f(current_user, *args, **kwargs)
    return decorator

def auth_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if 'x-access-tokens' in request.headers:
            return token_required(f)(*args, **kwargs)
        elif 'x-access-key' in request.headers:
            return key_required(f)(*args, **kwargs)
        elif 'x-access-user' in request.headers and 'x-access-pass' in request.headers:
            return user_pass_required(f)(*args, **kwargs)
        else:
            print("No auth")
            return jsonify({'message': 'a valid auth is missing', 'auth': False}), 401
    return decorator

def auth_requested(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if 'x-access-tokens' in request.headers:
            return token_requested(f)(*args, **kwargs)
        elif 'x-access-key' in request.headers:
            return key_requested(f)(*args, **kwargs)
        elif 'x-access-user' in request.headers and 'x-access-pass' in request.headers:
            return user_pass_requested(f)(*args, **kwargs)
        else:
            print("No auth")
        return f(None, *args, **kwargs)
    return decorator
