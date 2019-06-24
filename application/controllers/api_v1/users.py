from flask import request, Blueprint, jsonify, abort
from application.models import db, User
from application.extensions import jwt_auth

bp = Blueprint('api_v1_user', __name__, url_prefix='/api/v1')

def find_by_username(username):
    user = User.query.filter_by(username=username).first()

    print(user)
    if not user:
        raise Exception('User {} doesn\'s exit'.format(username))
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
def get_token():
    try:
        user_name = request.json.get('username')
        email = request.json.get('email')
        password = request.json.get('password')
        if not user_name:
            raise Exception('username is empty')
        elif not password:
            raise Exception('password is empty')

        user = find_by_username(user_name)
        if user.password == password:
            jwttoken = jwt_auth.generate_token(user.id)
            jwtrefreshtoken = jwt_auth.generate_refresh_token(user.id)
            return jsonify(dict(message='Logged in as {}'.format(user.username),
            JWTToken=jwttoken, JWTRToken=jwtrefreshtoken, code=200))
        else:
            raise Exception('Wrong credentials')


    except Exception as e:
        return jsonify(dict(message=str(e), code=404))
