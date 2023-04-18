from MT.setup import app, db
from MT.utils.auth import token_required
from MT.models.models import User

from flask import jsonify, request
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
