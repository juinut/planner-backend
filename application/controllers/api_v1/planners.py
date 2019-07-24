from flask import request, Blueprint, jsonify, abort
from application.models import db, Planner, User, joinMemberPlannerActivity, Member
from application.extensions import jwt_auth
import datetime as dt

bp = Blueprint('api_v1_planner', __name__, url_prefix='/planner')

@bp.route('/create_planner', methods=['POST'])
def create_planner():
    try:
        planner_name = request.json.get('planner_name')
        first_date = request.json.get('first_date')
        last_date = request.json.get('last_date')
        description = request.json.get('description')
        jwttoken = request.headers.get('Authorization').split(' ')[1]
        user = jwt_auth.get_user_from_token(jwttoken)
        friendlist = request.json.get('friendlist')
        print(friendlist)
        if not planner_name:
            raise Exception('planner_name cannot be empty')
        if not first_date:
            raise Exception('first_date cannot be empty')
        if not last_date:
            raise Exception('last_date cannot be empty')
        if not description:
            raise Exception('description cannot be empty')

        planner_object = Planner(name=planner_name,
        first_date=dt.datetime.strptime(first_date, '%Y-%m-%d').date(),
        last_date=dt.datetime.strptime(last_date, '%Y-%m-%d').date(),
        description=description, user_id=user.id)
        db.session.add(planner_object)
        db.session.commit()
        
        for i in friendlist:
            if(i['selected']):
                join = joinMemberPlannerActivity.Jointask(member_ID = i['id'], planner_ID = planner_object.id)
                db.session.add(join)
        
        db.session.commit()
        
        return jsonify(dict(success=True, code=201))

    except Exception as e:
        db.session.rollback()
        return jsonify(dict(success=False, message=str(e), code=400))

@bp.route('/view_all_planner', methods=['GET'])
def view_all_planner():
    try:
        jwttoken = request.headers.get('Authorization').split(' ')[1]
        user = jwt_auth.get_user_from_token(jwttoken)
        plannerlist = Planner.query.filter_by(user_id=user.id).all()
        planneridlist = []
        plannernamelist = []
        plannerfirstdatelist = []
        plannerlastdatelist = []
        for x in plannerlist:
            planneridlist.append(x.id)
            plannernamelist.append(x.name)
            plannerfirstdatelist.append(x.first_date)
            plannerlastdatelist.append(x.last_date)
        return jsonify(dict(id=planneridlist, name=plannernamelist,
        startdate=plannerfirstdatelist, enddate=plannerlastdatelist, code=200))
    except Exception as e:
        db.session.rollback()
        return jsonify(dict(success=False, message=str(e), code=400))

@bp.route('/view_planner/planner_id=<planner_id>', methods=['GET'])
def view_planner(planner_id):
    try:
        jwttoken = request.headers.get('Authorization').split(' ')[1]
        user = jwt_auth.get_user_from_token(jwttoken)
        desiredplanner = Planner.query.filter_by(id=planner_id).one()
        if user.id == desiredplanner.user_id:
            returnplanner = [desiredplanner.id, desiredplanner.name,
            desiredplanner.first_date, desiredplanner.last_date,
             desiredplanner.description, ]
            return jsonify(dict(planner=returnplanner, code=200))
        else:
            raise Exception('no such planner in your id')
    except Exception as e:
        db.session.rollback()
        return jsonify(dict(success=False, message=str(e), code=400))

@bp.route('/edit_planner/<planner_id>', methods=['PUT'])
def edit_planner(planner_id):
    try:
        planner_name = request.json.get('planner_name')
        first_date = request.json.get('first_date')
        last_date = request.json.get('last_date')
        description = request.json.get('description')
        jwttoken = request.headers.get('Authorization').split(' ')[1]
        user = jwt_auth.get_user_from_token(jwttoken)


        if not planner_name:
            raise Exception('planner_name cannot be empty')
        if not first_date:
            raise Exception('first_date cannot be empty')
        if not last_date:
            raise Exception('last_date cannot be empty')
        if not description:
            raise Exception('description cannot be empty')

        desiredplanner = Planner.query.filter_by(id=planner_id).one()
        if user.id == desiredplanner.user_id:
            Planner.query.filter(Planner.id == planner_id).\
            update({Planner.name: planner_name}, synchronize_session=False)
            db.session.commit()
            return jsonify(dict(success=True, code=201))
        else:
            raise Exception('no such planner in your id')
    except Exception as e:
        db.session.rollback()
        return jsonify(dict(success=False, message=str(e), code=400))

@bp.route('/delete_planner/<planner_id>', methods=['DELETE'])
def delete_planner(planner_id):
    try:
        jwttoken = request.headers.get('Authorization').split(' ')[1]
        user = jwt_auth.get_user_from_token(jwttoken)
        user_id = user.id
        planner = Planner.query.filter_by(id=planner_id)
        user_id_planner = Planner.query.filter_by(user_id=user_id).first()
        if user_id == user_id_planner.user_id:
            if not planner:
                raise Exception('planner has been deleted')

            planner.delete()
            db.session.commit()
            return jsonify(dict(success=True, code=201))
        else:
            raise Exception('no such planner in your id')

    except Exception as e:
        db.session.rollback()
        return jsonify(dict(success=False, message=str(e),code=400))

@bp.route('/checkplannerbelonging/planner_id=<planner_id>', methods=['GET'])
def planner_belonging(planner_id):
    try:
        jwttoken = request.headers.get('Authorization').split(' ')[1]
        user = jwt_auth.get_user_from_token(jwttoken)
        desiredplanner = Planner.query.filter_by(id=planner_id).one()
        if user.id == desiredplanner.user_id:
            return jsonify(dict(result=True, code=201))
        else:
            return jsonify(dict(result=False, code=201))
    except Exception as e:
        db.session.rollback()
        return jsonify(dict(success=False, message=str(e), code=400))

@bp.route('/getMember/planner_id=<planner_id>', methods=['GET'])
def getFriendinPlanner(planner_id):
    member_list = []
    memberid_list = []
    memberlastname_list = []
    membergender_list = []
    memberage=[]
    isownerlist=[]
    inplanner =  joinMemberPlannerActivity.Jointask.query.filter_by(planner_ID=planner_id)
    for i in inplanner:
        member = Member.query.filter_by(id=i.member_ID).one()
        member_list.append(member.firstname)
        memberid_list.append(member.id)
        memberlastname_list.append(member.lastname)
        membergender_list.append(member.gender)
        age = dt.datetime.now().year - i.DoB
        memberage.append(age)
        isownerlist.append(member.is_owner)
    return jsonify(dict(members=member_list,id=memberid_list,lastname=memberlastname_list,gender=membergender_list,age=memberage,owner=isownerlist, code=200))


