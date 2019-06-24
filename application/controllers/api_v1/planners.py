from flask import request, Blueprint, jsonify, abort
from application.models import db, Planner, User
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
        jwttoken = request.json.get('jwttoken')
        user = jwt_auth.get_user_from_token(jwttoken)

        if not planner_name:
            raise Exception('planner_name cannot be empty')
        if not first_date:
            raise Exception('first_date cannot be empty')
        if not last_date:
            raise Exception('last_date cannot be empty')
        if not description:
            raise Exception('description cannot be empty')

        planner_object = Planner(name=planner_name,
        first_date=dt.datetime.strptime(first_date, '%d%m%Y').date(),
        last_date=dt.datetime.strptime(last_date, '%d%m%Y').date(),
        description=description, user_id=user.id)

        db.session.add(planner_object)
        db.session.commit()
        return jsonify(dict(success=True)), 201

    except Exception as e:
        db.session.rollback()
        return jsonify(dict(success=False, message=str(e))), 400

@bp.route('/view_all_planner', methods=['GET'])
def view_all_planner():
    try:
        jwttoken = request.json.get('jwttoken')
        user = jwt_auth.get_user_from_token(jwttoken)
        plannerlist = Planner.query.filter_by(user_id=user.id).all()
        print(plannerlist)
        planneridlist = []
        plannernamelist = []
        for x in plannerlist:
            planneridlist.append(x.id)
            plannernamelist.append(x.name)
        return jsonify(dict(id=planneridlist, name=plannernamelist)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify(dict(success=False, message=str(e))), 400

@bp.route('/view_planner/<planner_id>', methods=['GET'])
def view_planner(planner_id):
    try:
        jwttoken = request.json.get('jwttoken')
        user = jwt_auth.get_user_from_token(jwttoken)
        desiredplanner = Planner.query.filter_by(id=planner_id).one()
        if user.id == desiredplanner.user_id:
            returnplanner = [desiredplanner.id, desiredplanner.name,
            desiredplanner.first_date, desiredplanner.last_date,
             desiredplanner.description]
            return jsonify(dict(planner=returnplanner)), 201
        else:
            return jsonify(dict(message='no such planner in your id')), 400
    except Exception as e:
        db.session.rollback()
        return jsonify(dict(success=False, message=str(e))), 400

@bp.route('/edit_planner/<planner_id>', methods=['POST'])
def edit_planner(planner_id):
    try:
        planner_name = request.json.get('planner_name')
        first_date = request.json.get('first_date')
        last_date = request.json.get('last_date')
        description = request.json.get('description')
        jwttoken = request.json.get('jwttoken')
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
            return jsonify(dict(success=True)), 201
        else:
            return jsonify(dict(message='no such planner in your id')), 400
    except Exception as e:
        db.session.rollback()
        return jsonify(dict(success=False, message=str(e))), 400

@bp.route('/delete_planner/<planner_id>', methods=['GET'])
def delete_planner(planner_id):
    try:
        planner_name = request.json.get('planner_name')
        first_date = request.json.get('first_date')
        last_date = request.json.get('last_date')
        description = request.json.get('description')
        jwttoken = request.json.get('jwttoken')
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
            return jsonify(dict(success=True)), 201
        else:
            return jsonify(dict(message='no such planner in your id')), 400
    except Exception as e:
        db.session.rollback()
        return jsonify(dict(success=False, message=str(e))), 400
