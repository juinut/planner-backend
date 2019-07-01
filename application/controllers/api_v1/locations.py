from flask import request, Blueprint, jsonify, abort
from application.models import db, Location
from application.extensions import jwt_auth
import datetime as dt

bp = Blueprint('api_v1_location', __name__, url_prefix='/api/v1')

@bp.route('/add_location', methods=['POST'])
def add_location():
    try:
        name = request.json.get('name')
        latitude = request.json.get('latitude')
        longtitude = request.json.get('longtitude')
        # jwttoken = request.headers.get('Authorization').split(' ')[1]
        # user = jwt_auth.get_user_from_token(jwttoken)

        if not name:
            raise Exception('name cannot be empty')
        if not latitude:
            raise Exception('latitude cannot be empty')
        if not longtitude:
            raise Exception('longtitude cannot be empty')

        location_object = Location(name=name,latitude=latitude, longtitude=longtitude)

        db.session.add(location_object)
        db.session.commit()
        return jsonify(dict(success=True, code=201))

    except Exception as e:
        db.session.rollback()
        return jsonify(dict(success=False, message=str(e), code=400))


