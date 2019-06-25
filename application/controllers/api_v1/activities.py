from flask import request, Blueprint, jsonify, abort
from application.models import db, Planner, User, Activity
from application.extensions import jwt_auth
import datetime as dt

bp = Blueprint('api_v1_activity', __name__, url_prefix='/activity')

@bp.route('/create_activity', methods=['POST'])
def create_activity():
    try:
        activity_name = request.json.get('activity_name')
        start_datetime = request.json.get('start_datetime')
        end_datetime = request.json.get('end_datetime')
        description = request.json.get('description')

        if not activity_name:
            raise Exception('activity_name cannot be empty')
        if not start_datetime:
            raise Exception('start_datetime cannot be empty')
        if not end_datetime:
            raise Exception('end_datetime cannot be empty')
        if not description:
            raise Exception('description cannot be empty')

        activity_object = Activity(name=activity_name,
        start=dt.datetime.strptime(start_datetime, '%Y-%m-%d %H:%M:%S.%f'),
        end=dt.datetime.strptime(end_datetime, '%Y-%m-%d %H:%M:%S.%f'),
        description=description)

        db.session.add(activity_object)
        db.session.commit()
        return jsonify(dict(success=True, code=201))

    except Exception as e:
        db.session.rollback()
        return jsonify(dict(success=False, message=str(e), code=400))

@bp.route('/view_activity/<planner_id>/<activity_id>', methods=['GET'])
def view_activity(planner_id, activity_id):
    try:
        jwttoken = request.json.get('jwttoken')
        user = jwt_auth.get_user_from_token(jwttoken)
        desiredplanner = Planner.query.filter_by(id=planner_id).one()
        desiredactiity = Activity.query.filter_by(id=activity_id).one()
        if user.id == desiredplanner.user_id:
            if desiredplanner.id == desiredactiity.planner_ID:
                returnactivity = [desiredactiity.id, desiredactiity.name, desiredactiity.start,
                desiredactiity.end, desiredactiity.description]
                return jsonify(dict(activity=returnactivity, code=201))
            else:
                raise Exception('no such activity')
        else:
            raise Exception('no such user')
    except Exception as e:
        db.session.rollback()
        return jsonify(dict(success=False, message=str(e), code=400))

@bp.route('/edit_activity/<activity_id>', methods=['POST'])
def edit_planner(activity_id):
    try:
        activity_name = request.json.get('activity_name')
        start_datetime = request.json.get('start_datetime')
        end_datetime = request.json.get('end_datetime')
        description = request.json.get('description')
        jwttoken = request.json.get('jwttoken')
        user = jwt_auth.get_user_from_token(jwttoken)

        if not activity_name:
            raise Exception('activity_name cannot be empty')
        if not start_datetime:
            raise Exception('start_datetime cannot be empty')
        if not end_datetime:
            raise Exception('end_datetime cannot be empty')
        if not description:
            raise Exception('description cannot be empty')

        desiredactiity = Activity.query.filter_by(id=activity_id).one()

        if user.id == desiredplanner.user_id:
            if desiredplanner.id == desiredactiity.planner_ID:
                Activity.query.filter(Activity.id == activity_id).\
                update({Activity.name: activity_name}, synchronize_session=False)
                db.session.commit()
                return jsonify(dict(success=True), 201)
            else:
                return jsonify(dict(message='no such activity in your id')), 400
        else:
            raise Exception('no such user in your id')
    except Exception as e:
        db.session.rollback()
        return jsonify(dict(success=False, message=str(e))), 400
