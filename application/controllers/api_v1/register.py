from flask import request, Blueprint, jsonify, abort
from application.models import db, User

bp = Blueprint('api_v1_register', __name__, url_prefix='/register')

@bp.route('/', methods=['POST'])
def create_user():
    try:
        # x = request.args.get('x')
        # TODO
        username = request.json.get('username')
        firstname = request.json.get('firstname')
        lastname = request.json.get('lastname')
        password = request.json.get('password')
        email = request.json.get('email')
        dob = request.json.get('dob')

        if not username or not password or not firstname or not lastname or not email or not email:
            raise Exception('invalid input data')

        db.session.add(User(id=1, username=username, firstname=firstname, lastname=lastname, password=password,email=email, dob=dob, is_admin=False))
        db.session.commit()
        return jsonify(dict(success=True)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify(dict(success=False, message=str(e))), 400

@bp.route('/', methods=['GET'])
def get():
    return jsonify(dict(message="Hi")), 201
