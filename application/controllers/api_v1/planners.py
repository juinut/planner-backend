from flask import request, Blueprint, jsonify, abort
from application.models import db, Planner, User
from application.extensions import jwt_auth
import datetime as dt

bp = Blueprint('api_v1_planner', __name__, url_prefix='/planner')

@bp.route('/create_plan', methods=['POST'])
def create_plan():
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

@bp.route('/view_all_plan', methods=['GET'])
def view_all_plan():
    try:
        jwttoken = request.json.get('jwttoken')
        user = jwt_auth.get_user_from_token(jwttoken)
        plannerlist = Planner.query.filter_by(user_id=user.id).all()
        print(plannerlist)
        return jsonify(dict(success=True)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify(dict(success=False, message=str(e))), 400
