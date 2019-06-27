from flask import request, Blueprint, jsonify, abort
from application.models import db, Planner, User, Activity, MemberTakeService, Service, Location, Servicetype, Member
from application.extensions import jwt_auth
import datetime as dt

bp = Blueprint('api_v1_service', __name__, url_prefix='/service')

def check_service(num):
    service = Servicetype.query.filter_by(id=num).first()
    if not service:
        raise Exception('Not found {} type service'.format(num))
    return service.description

@bp.route('/<plannerid>/<activityid>/createservice', methods=['POST'])
def create_activity(activityid):
    try:
        name = request.json.get('name')
        activity_ID = activityid
        serviceType_ID = request.json.get("serviceType") 
        service_type = check_service(serviceType_ID)
        calType = request.json.get('calType')#True is multiple, False is mod

        if calType:
            kid_price = request.json.get("kidPrice")
            adute = request.json.get("adutPrice")
            elderly = request.json.get("elderlyPrice")
            if not kid_price and not adute and not elderly:
                raise Exception("Plase set price")

        else:
            price = request.json.get("price")
            if not price:
                raise Exception("Plase set price")

        if service_type == "travel":
            location_start = request.json.get("location_start")
            location_stop = request.json.get("location_stop")
            if not location_start or not location_stop:
                raise Exception("Location start or Stop is mission")
            #if this location is not in db
            # create End_location first
            endObj = Service(name=name, calType=calType, activity_ID=activity_ID,serviceType_ID=service_type\
                    ,location_ID=location_stop)
            db.session.add(endObj)
            db.session.commit()
            startObj = Service(name=name,kidPrice=kid_price,adutePrice=adute,elderlyProce=elderly\
                ,sumPrice=price,calType=calType,activity_ID=activity_ID,serviceType_ID=service_type\
                    ,location_ID=location_start,serviceRef=endObj.id)
            db.session.add(startObj)
            db.commit()
            serviceID = startObj.id
        
        else:
            location_in =  request.json.get("location_in")
            Obj = Service(name=name,kidPrice=kid_price,adutePrice=adute,elderlyProce=elderly\
                ,sumPrice=price,calType=calType,activity_ID=activity_ID,serviceType_ID=service_type\
                    ,location_ID=location_start)
            db.session.add(Obj)
            db.session.commit()
            serviceID = Obj.id

        members = request.json.get("user")
        # jwttoken = request.json.get('jwttoken')
        # user = jwt_auth.get_user_from_token(jwttoken)
        if calType:
            for member in members:
                mem = Member.query.filter_by(id=member).first()
                memAge = (dt.date.now()).year - (mem.DoB).year
                if memAge <= 12:
                    priceMember = kid_price
                elif memAge < 60:
                    priceMember = adute
                else:
                    priceMember = elderly
                memTake = MemberTakeService(member_ID="member", service_ID=serviceID, price=priceMember)
                db.session.add(memTake)
                db.commit()
        else:
            countMem = len(members)
            priceM = price/countMem
            for member in members:
                memTake = MemberTakeService(member_ID="member", service_ID=serviceID, price=priceM)
                db.session.add(memTake)
                db.commit()

        return jsonify(dict(success=True,code=200))

    except Exception as e:
        db.session.rollback()
        return jsonify(dict(success=False, message=str(e),code=400))

@bp.route('delete_service/<service_id>', methods=['DELETE'])
def delete_activity(service_id):
    try:
        MemberTakeService.query.filter_by(service_ID=service_id).delete()
        Service.query.filter_by(service_ID=service_id).delete()
        return jsonify(dict(success=True, code=200))

    except Exception as e:
        db.session.rollback()
        return jsonify(dict(success=False, message=str(e),code=400))