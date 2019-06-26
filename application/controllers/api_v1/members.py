from flask import request, Blueprint, jsonify, abort
from application.models import db, Member
from application.extensions import jwt_auth
import datetime as dt

bp = Blueprint('api_v1_member', __name__, url_prefix='/api/v1')

def find_by_firstname(firstname):
    member = Member.query.filter_by(firstname=firstname).first()

    print(user)
    if not member:
        raise Exception('Member {} doesn\'s exit'.format(firstname))
    else:
        return member

@bp.route('/member', methods=['GET'])
def list_users():
    data = Member.query.all()
    member_list = []
    for i in data:
        member_list.append(i.username)
    return jsonify(dict(members=member_list, code=200))

@bp.route('/create_member', methods=['POST'])
def create_member():
    try:
        jwttoken = request.json.get('jwttoken')
        user = jwt_auth.get_user_from_token(jwttoken)
        user_id = user.id
        firstname = request.json.get('firstname')
        lastname = request.json.get('lastname')
        dob = request.json.get('dob')
        gender = request.json.get('gender')

        if not firstname:
            raise Exception('firstname is empty')
        if not lastname:
            raise Exception('lastname is empty')
        if not dob:
            raise Exception('dob is empty ')
        if not gender:
            raise Exception('gender is empty')

        tocreateuserobject = Member(firstname=firstname,
        lastname=lastname,DoB=dt.datetime.strptime(dob, '%Y-%m-%d').date(), gender=gender, user_ID=user_id)

        db.session.add(tocreateuserobject)
        db.session.commit()
        return jsonify(dict(success=True, code=201))

    except Exception as e:
        db.session.rollback()
        return jsonify(dict(success=False, message=str(e),code=400))
    