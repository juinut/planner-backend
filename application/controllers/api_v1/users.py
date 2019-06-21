from flask import request, Blueprint, jsonify, abort
from application.models import db, User
# from ...extensions import jwt_auth

bp = Blueprint('api_v1_user', __name__, url_prefix='/api/v1')

@classmethod
def find_by_username(username):
    user = User.query.get(username).first()
    if not user:
        raise Exception('User not found')
    else:
        return user


@bp.route('/test', methods=['GET'])
def test():
    return jsonify(dict(users="OK OK", code=200))


@bp.route('/user', methods=['GET'])
def list_users():
    data = User.query.all()
    return jsonify(dict(users=data, code=200))


@bp.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify(dict(user=dict(name=user.name, email=user.email), code=200))
    else:
        abort(400)

@bp.route('/login', methods=['POST'])
def get_token(user):
    try:
        token = False
        user_name = request.json.get('username')
        password = request.json.get('password')
        if not user_name:
            raise Exception('username is empty')
        elif not password:
            raise Exception('password is empty')
        
        user = find_by_username(user_name)
        
        if user.password == password:
            token = True
        return jsonify(dict(success=token), code=200)
    except Exception as e:
        return jsonify(dict(message=str(e)), code=404)
                
