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
    jwttoken = request.headers.get('Authorization').split(' ')[1]
    user = jwt_auth.get_user_from_token(jwttoken)
    data = Member.query.filter_by(user_id=user.id)
    member_list = []
    memberid_list = []
    for i in data: 
        member_list.append(i.firstname)
        memberid_list.append(i.id)
        print(i)
    return jsonify(dict(members=member_list,id=memberid_list, code=200))

@bp.route('/delete_member/<id>', methods=['DELETE'])
def delete_member(id):
    try:
        jwttoken = request.headers.get('Authorization').split(' ')[1]
        user = jwt_auth.get_user_from_token(jwttoken)
        user_id = user.id
        member = Member.query.filter_by(id=id)
        user_id_member = Member.query.filter_by(user_id=user_id).first()
        if user_id == user_id_member.user_id:
            if not member:
                raise Exception('member has been deleted')
            
            member.delete()
            db.session.commit()
            return jsonify(dict(success=True, code=201))
        else:
            raise Exception('no such member in your id')

    except Exception as e:
        db.session.rollback()
        return jsonify(dict(success=False, message=str(e),code=400))
        

@bp.route('/create_member', methods=['POST'])
def create_member():
    try:
        jwttoken = request.headers.get('Authorization').split(' ')[1]
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
        lastname=lastname,DoB=dt.datetime.strptime(dob, '%Y-%m-%d').date(), gender=gender, user_id=int(user_id))

        db.session.add(tocreateuserobject)
        db.session.commit()
        return jsonify(dict(success=True, code=201))

    except Exception as e:
        db.session.rollback()
        return jsonify(dict(success=False, message=str(e),code=400))
    