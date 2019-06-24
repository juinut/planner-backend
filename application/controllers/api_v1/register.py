from flask import request, Blueprint, jsonify, abort
from application.models import db, User
import datetime as dt
import re

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
        gender = request.json.get('gender')

        if not username:
            raise Exception('username is empty')
        if not firstname:
            raise Exception('firstname is empty')
        if not lastname:
            raise Exception('lastname is empty')
        if not password:
            raise Exception('password is empty')
        if not email:
            raise Exception('email is empty')
        if not dob:
            raise Exception('dob is empty')
        if not gender:
            raise Exception('gender is empty')
        if not re.match("^[a-zA-Z0-9]*$", username):
            raise Exception('username cant contain special characters')
        if not re.match("^[a-zA-Z]*$", firstname):
            raise Exception('firstname cant contain special characters or numbers')
        if not re.match("^[a-zA-Z]*$", lastname):
            raise Exception('lastname cant contain special characters or numbers')
        if not re.match("^[a-zA-Z0-9]*$", password):
            raise Exception('password cant contain special characters')
        if not re.match("^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
            raise Exception('email does not valid')
        if not re.match("^[0-9-]*$", dob):
            raise Exception('dob cant contain alphabets or special characters')
        if User.query.filter_by(username=username).all():
            raise Exception('username already existed')
        if User.query.filter_by(email=email).all():
            raise Exception('email already existed')

        tocreateuserobject = User(username=username, firstname=firstname,
        lastname=lastname, password=password,email=email,
        dob=dt.datetime.strptime(dob, '%Y-%m-%d').date(), gender=gender,
        is_admin=False)

        db.session.add(tocreateuserobject)
        db.session.commit()
        return jsonify(dict(success=True)), 201

    except Exception as e:
        db.session.rollback()
        return jsonify(dict(success=False, message=str(e),code=400))

@bp.route('/', methods=['GET'])
def get():
    return jsonify(dict(message="Hi")), 201
