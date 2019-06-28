from flask import request, Blueprint, jsonify, abort
from application.models import db, Planner, User, Activity
from application.extensions import jwt_auth
import datetime as dt

bp = Blueprint('api_v1_activity', __name__, url_prefix='/planner')

@bp.route('/<plannerid>/create_activity', methods=['POST'])
def create_activity(plannerid):
    try:
        activity_name = request.json.get('activity_name')
        start_date = request.json.get('start_date')
        start_time = request.json.get('start_time')
        end_date = request.json.get('end_date')
        end_time = request.json.get('end_time')
        description = request.json.get('description')

        if not activity_name:
            raise Exception('activity_name cannot be empty')
        if not start_date:
            raise Exception('start_date cannot be empty')
        if not start_time:
            raise Exception('start_time cannot be empty')
        if not end_date:
            raise Exception('end_date cannot be empty')
        if not end_time:
            raise Exception('end_time cannot be empty')
        if not description:
            raise Exception('description cannot be empty')

        start_datetime = start_date+' '+start_time
        end_datetime = end_date+' '+end_time
        activity_object = Activity(name=activity_name,
        start=dt.datetime.strptime(start_datetime, '%Y-%m-%d %H:%M'),
        end=dt.datetime.strptime(end_datetime, '%Y-%m-%d %H:%M'),
        description=description, planner_ID=plannerid, serviceType_ID='0')

        db.session.add(activity_object)
        db.session.commit()
        return jsonify(dict(success=True, code=201))

    except Exception as e:
        db.session.rollback()
        return jsonify(dict(success=False, message=str(e), code=400))

@bp.route('/planner_id=<planner_id>/view_all_activity', methods=['GET'])
def view_all_activity(planner_id):
    try:
        jwttoken = request.json.get('jwttoken')
        user = jwt_auth.get_user_from_token(jwttoken)
        desiredplanner = Planner.query.filter_by(id=planner_id).one()
        listofactivity = Activity.query.filter_by(planner_ID=planner_id).all()
        if not desiredplanner: raise Exception('no such planner')
        if not listofactivity: raise Exception('no activity in planner')
        if user.id == desiredplanner.user_id:
            activityidlist = []
            activitynamelist = []
            activitystartdatetime = []
            activityenddatetime = []
            activityservicetypelist = []
            for x in listofactivity:
                activityidlist.append(x.id)
                activitynamelist.append(x.name)
                activitystartdatetime.append(x.start)
                activityenddatetime.append(x.end)
                activityservicetypelist.append(x.serviceType_ID)
            return jsonify(dict(id=activityidlist, name=activitynamelist,
            startdatetime=activitystartdatetime, end_datetime=activityenddatetime,
            servicetypeID=activityservicetypelist, code=200))
        else:
            raise Exception('no such user')
    except Exception as e:
        db.session.rollback()
        return jsonify(dict(success=False, message=str(e), code=400))

@bp.route('/<planner_id>/view_activity/<activity_id>', methods=['GET'])
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
