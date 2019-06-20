from flask import request, Blueprint, jsonify, abort
from application.models import db, User
from ...extensions import jwt_auth

bp = Blueprint('api_v1_user', __name__, url_prefix='/api/v1')

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

@bp.route('/login' methods=['POST'])
def get_token(user):
    try:
        name = request.json.get('username')
        password = request.json.get('password')
        
