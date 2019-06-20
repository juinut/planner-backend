from flask import request, Blueprint, jsonify, abort
from application.models import db, User


bp = Blueprint('api_v1_register', __name__, url_prefix='/api/v1')

@bp.route('/register', methods=['POST'])
def register(user):
    user = 



@bp.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify(dict(user=dict(name=user.name, email=user.email), code=200))
    else:
        abort(400)

