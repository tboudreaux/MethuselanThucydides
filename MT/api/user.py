from MT.setup import app, db
from MT.utils.auth import token_required, auth_required
from MT.models.models import User, Key

from flask import jsonify, request
import secrets

@app.route('/api/user/enroll_user', methods=['POST'])
@token_required
def enroll_user_endpoint(current_user):
    payload = request.get_json()
    if current_user.admin:
        newUser = payload['new_user']
        newPass = payload['new_pass']
        newEmail = payload['new_email']
        newUserIsAdmin = payload['new_user_is_admin']
        newUserIsEnabled = payload['new_user_is_enabled']

        # check if the new user is already in the database
        checkNewUser = User.query.filter_by(username=newUser).first()
        if checkNewUser:
            return jsonify({'message':'User already exists'}), 409

        newUser = User(newUser, newEmail, newPass, admin=newUserIsAdmin, enabled=newUserIsEnabled)
        db.session.add(newUser)
        db.session.commit()
        # check if the new user is in the database
        checkNewUser = User.query.filter_by(username=newUser.username).first()
        if checkNewUser:
            return jsonify({'success':True}), 201
        else:
            return jsonify({'success':False}), 500
    elif not current_user.admin:
        return jsonify({'message':'User is not an admin'}), 401
    return jsonify({'message':'Unknown error'}), 500

@app.route('/api/user/enroll_user/secret', methods=['POST'])
def enroll_user_with_secret():
    payload = request.get_json()
    if app.config['MT_NEW_USER_SECRET'] is None:
        return jsonify({'message':'No secret set'}), 401
    if payload['new_user_secret'] == app.config['MT_NEW_USER_SECRET']:
        newUser = payload['new_user']
        newPass = payload['new_pass']
        newEmail = payload['new_email']

        # check if the new user is already in the database
        checkNewUser = User.query.filter_by(username=newUser).first()
        if checkNewUser:
            return jsonify({'message':'User already exists'}), 409

        # count how many users there are in the database
        userCount = User.query.count()
        # if there are no users, make the new user an admin
        if userCount == 0:
            newUserIsAdmin = True
        else:
            newUserIsAdmin = False
        newUserIsAdmin = newUserIsAdmin
        newUserIsEnabled = True

        newUser = User(newUser, newEmail, newPass, admin=newUserIsAdmin, enabled=newUserIsEnabled)
        db.session.add(newUser)
        db.session.commit()
        # check if the new user is in the database
        checkNewUser = User.query.filter_by(username=newUser.username).first()
        if checkNewUser:
            return jsonify({'success':True}), 201
        else:
            return jsonify({'success':False}), 500
    else:
        return jsonify({'message':'Invalid secret'}), 401

@app.route('/api/user/is_admin', methods=['GET'])
@auth_required
def is_admin_endpoint(current_user):
    return jsonify({'admin':current_user.admin}), 200

@app.route('/api/user/genkey', methods=['GET'])
@token_required
def genkey_endpoint(current_user):
    if not current_user.admin:
        return jsonify({'message':'User is not an admin'}), 401
    unhashedKey = secrets.token_hex(16)
    key = Key(current_user.uuid, unhashedKey)
    db.session.add(key)
    db.session.commit()
    return jsonify({'key':unhashedKey, 'uuid':key.uuid}), 200

@app.route('/api/user/update/username/<username>', methods=['POST'])
@auth_required
def update_username_endpoint(current_user, username):
    payload = request.get_json()
    user = current_user
    if 'alternate_user' in payload and current_user.admin:
        user = User.query.filter_by(username=payload['alternate_user']).first()
    elif 'alternate_user' in payload and not current_user.admin:
        return jsonify({'message':'User is not an admin'}), 401
    if current_user.username == username:
        return jsonify({'message':'Username is the same'}), 409
    checkUser = User.query.filter_by(username=username).first()
    if checkUser:
        return jsonify({'message':'Username already exists'}), 409
    user.update_username(username)
    db.session.commit()
    return jsonify({'success':True}), 200

@app.route('/api/user/update/email/<email>', methods=['POST'])
@auth_required
def update_email_endpoint(current_user, email):
    payload = request.get_json()
    user = current_user
    if 'alternate_user' in payload and current_user.admin:
        user = User.query.filter_by(username=payload['alternate_user']).first()
    elif 'alternate_user' in payload and not current_user.admin:
        return jsonify({'message':'User is not an admin'}), 401
    if current_user.email == email:
        return jsonify({'message':'Email is the same'}), 409
    user.update_email(email)
    db.session.commit()
    return jsonify({'success':True}), 200

@app.route('/api/user/update/password', methods=['POST'])
@auth_required
def update_password_endpoint(current_user):
    payload = request.get_json()
    user = current_user
    if 'alternate_user' in payload and current_user.admin:
        user = User.query.filter_by(username=payload['alternate_user']).first()
    elif 'alternate_user' in payload and not current_user.admin:
        return jsonify({'message':'User is not an admin'}), 401
    if not user.check_password(payload['old_password']):
        return jsonify({'message':'Old password is incorrect'}), 401
    user.update_password(payload['old_password'], payload['new_password'])
    db.session.commit()
    return jsonify({'success':True}), 200

@app.route('/api/user/update/display_name', methods=['POST'])
@auth_required
def update_display_name_endpoint(current_user):
    payload = request.get_json()
    user = current_user
    if 'alternate_user' in payload and current_user.admin:
        user = User.query.filter_by(username=payload['alternate_user']).first()
    elif 'alternate_user' in payload and not current_user.admin:
        return jsonify({'message':'User is not an admin'}), 401
    if current_user.display_name == payload['display_name']:
        return jsonify({'message':'Display name is the same'}), 409
    user.update_display_name(payload['display_name'])
    db.session.commit()
    return jsonify({'success':True}), 200


