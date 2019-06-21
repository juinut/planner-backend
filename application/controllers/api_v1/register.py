from flask import request, Blueprint, jsonify, abort
from application.models import db, User
import datetime as dt

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
        confirmpassword = request.json.get('confirmpassword')
        email = request.json.get('email')
        dob = request.json.get('dob')

        if not username:
            raise Exception('username is empty')
        if not firstname:
            raise Exception('firstname is empty')
        if not lastname:
            raise Exception('lastname is empty')
        if not password:
            raise Exception('password is empty')
        if not confirmpassword:
            raise Exception('confirmpassword is empty')
        if not email:
            raise Exception('email is empty')
        if not dob:
            raise Exception('dob is empty')
        if password!=confirmpassword:
            raise Exception('passwords are not matched')

        # tocreateuserobject = User(username=username, firstname=firstname, lastname=lastname, password=password,email=email, dob=dt.date(1998,1,1), is_admin=False)

        tocreateuserobject = User(username=username, firstname=firstname,
        lastname=lastname, password=password,email=email,
        dob=dt.datetime.strptime(dob, '%d-%m-%Y').date(), is_admin=False)

        db.session.add(tocreateuserobject)
        db.session.commit()
        return jsonify(dict(success=True)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify(dict(success=False, message=str(e)+dob)), 400

@bp.route('/', methods=['GET'])
def get():
    return jsonify(dict(message="Hi")), 201
