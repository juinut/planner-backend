from flask import request, Blueprint, jsonify, abort
from application.models import db, Planner, User, Activity, MemberTakeService, Service, Location, Servicetype, Member, joinMemberPlannerActivity
from application.extensions import jwt_auth
import datetime as dt

bp = Blueprint('api_v1_service', __name__, url_prefix='/service')

@bp.route('/<plannerid>/<activityid>/createservice', methods=['POST'])
def create_service(plannerid,activityid):
    try:
        name = request.json.get('name')
        activity_ID = activityid
        calType = request.json.get('calType')#True is multiple, False is mod
        price = request.json.get("price")
        kid_price = request.json.get("kidPrice")
        adute = request.json.get("adutePrice")
        elderly = request.json.get("elderlyPrice")

        if not calType:
            if not kid_price and not adute and not elderly:
                raise Exception("Plase set price")

        else:
            if not price:
                raise Exception("Plase set price")

        Obj = Service(name=name,kidPrice=kid_price,adultPrice=adute,elderlyPrice=elderly\
            ,sumPrice=price,calType=calType,activity_ID=activity_ID)

        db.session.add(Obj)
        db.session.commit()
        serviceID = Obj.id

        members = request.json.get("user")
        # jwttoken = request.json.get('jwttoken')
        # user = jwt_auth.get_user_from_token(jwttoken)
        if not calType:
            for member in members:
                mem = Member.query.filter_by(id = member['id']).first()
                memAge = int((dt.datetime.now()).year) - int(mem.DoB)
                if memAge <= 12:
                    priceMember = kid_price
                elif memAge < 60:
                    priceMember = adute
                else:
                    priceMember = elderly
                memTake = MemberTakeService(member_ID=member['id'], service_ID=serviceID, price=priceMember)
                db.session.add(memTake)
                db.session.commit()
        else:
            countMem = int(len(members))
            for member in members:
                mem = Member.query.filter_by(id = member['id']).first()
                memAge = int((dt.datetime.now()).year) - int(mem.DoB)
                if memAge <= 12:
                    countMem = countMem-1

            priceM = int(price)/countMem
            for member in members:
                mem = Member.query.filter_by(id = member['id']).first()
                memAge = int((dt.datetime.now()).year) - int(mem.DoB)
                if memAge > 12:
                    memTake = MemberTakeService(member_ID=member['id'], service_ID=serviceID, price=priceM)
                    db.session.add(memTake)
                    db.session.commit()
                else:
                    memTake = MemberTakeService(member_ID=member['id'], service_ID=serviceID)
                    db.session.add(memTake)
                    db.session.commit()

        return jsonify(dict(success=True,code=200))

    except Exception as e:
        db.session.rollback()
        return jsonify(dict(success=False, message=str(e),code=400))

@bp.route('<service_id>/delete', methods=['DELETE'])
def delete_service(service_id):
    try:
        MemberTakeService.query.filter_by(service_ID=service_id).delete()
        Service.query.filter_by(service_ID=service_id).delete()
        return jsonify(dict(success=True, code=200))

    except Exception as e:
        db.session.rollback()
        return jsonify(dict(success=False, message=str(e),code=400))

@bp.route('<activity_id>/<service_id>',methods=['PUT'])
def update_service(service_id):
    try:
        name = request.json.get('name')
        calType = request.json.get('calType')#True is multiple, False is mod

        if calType:
            kid_price = request.json.get("kidPrice")
            adult = request.json.get("adultPrice")
            elderly = request.json.get("elderlyPrice")
            if not kid_price and not adult and not elderly:
                raise Exception("Plase set price")

        else:
            price = request.json.get("price")
            if not price:
                raise Exception("Plase set price")

        Service.query.filter_by(id=service_id)\
        .update({Service.name:name, Service.kidPrice:kid_price, Service.adultPrice:adult,\
        Service.elderlyPrice:elderly,Service.calType:calType,Service.sumPrice:price})
        db.session.commit()

        members = request.json.get("user")
        # jwttoken = request.json.get('jwttoken')
        # user = jwt_auth.get_user_from_token(jwttoken)
        if calType:
            for member in members:
                mem = Member.query.filter_by(id==member).first()
                memAge = (dt.date.now()).year - (mem.DoB).year
                if memAge <= 12:
                    priceMember = kid_price
                elif memAge < 60:
                    priceMember = adult
                else:
                    priceMember = elderly

                MemberTakeService.query.filter_by(MemberTakeService.member_ID == mem.id,\
                    MemberTakeService.service_ID == service_id)\
                    .update({price:priceMember})
                db.session.commit()

        else:
            countMem = len(members)
            priceM = price/countMem
            for member in members:
                MemberTakeService.query.filter_by(member_ID = mem.id,\
                    service_ID = service_id)\
                    .update({price:priceM})
                db.session.commit()

        return jsonify(dict(success=True,code=200))

    except Exception as e:
        db.session.rollback()
        return jsonify(dict(success=False, message=str(e),code=400))

@bp.route('<activity_id>',methods=['GET'])
def viewServiceInActivity(activity_id):
    try:
        returnServices = Service.query.filter_by(activity_id).all()
        servicenamelist = []
        servicecaltypelist = []
        servicekidlist = []
        serviceadultlist = []
        serviceelderylist = []
        servicesumpricelist = []
        serviceallpricelist = []
        for service in returnServices:
            servicenamelist.append(service.name)
            servicecaltypelist.append(service.calType)
            servicekidlist.append(service.kidPrice)
            serviceadultlist.append(service.adultPrice)
            serviceelderylist.append(service.elderlyPrice)
            servicesumpricelist.append(service.sumPrice)
            allprice = 0
            for price in service.takeServices:
                allprice += price.price
            serviceallpricelist.append(allprice)

        return jsonify(dict(servicename=servicenamelist, caltype=servicecaltypelist\
            , kid=servicekidlist, adult=serviceadultlist, elderly=serviceelderylist\
            , sumprice=servicesumpricelist, allprice=servicesumpricelist\
            , code = 200))


    except Exception as e:
        db.session.rollback()
        return jsonify(dict(success=False, message=str(e),code=400))

@bp.route('<activity_id>/service',methods=['GET'])
def viewMemberPrice(activity_id):
    try:
        activity = Activity.query.filter_by(id = activity_id).one()
        services = Service.query.filter_by(activity_ID = activity_id)
        servicedict = {}
        activity_total_price = 0
        activityname = activity.name
        for service in services:
            servicedict[service.id] = [service.id, service.name]
            memberdict = {}
            members = MemberTakeService.query.filter_by(service_ID = service.id)
            priceinservice = 0
            for member in members:
                memberdetail = Member.query.filter_by(id=member.member_ID).one()
                memberdict[memberdetail.id] = [memberdetail.id, memberdetail.firstname, memberdetail.lastname, memberdetail.DoB, member.price]
                if member.price:
                    priceinservice += member.price
                    activity_total_price += member.price
            servicedict[service.id].append(memberdict)
            servicedict[service.id].append(priceinservice)

        servicedict[999999] = int(activity_total_price)
        return jsonify(dict(data=servicedict, activityname = activityname, success=True, code=200))

    except Exception as e:
        return jsonify(dict(success=False, message=str(e), code=400))

        # service = Service.query.filter_by(id = service_ID)
        # if not service:
        #     raise 'service not found'

        # members = service.takeServices
        # memberlist = []
        # membergender = []
        # memberpricelist = []
        # for member in members:
        #     membername = Member.query.filter_by(id = member.member_ID).one()
        #     memberlist.append(membername.fristname)
        #     membergender.append(membername.gender)
        #     memberpricelist.append(member.price)



@bp.route('planner_id=<planner_id>/member',methods=['GET'])
def viewResult(planner_id):
    try:
        planner = Planner.query.filter_by(id=planner_id).one()
        memberdict = {}
        servicesdict = {}
        memberdict[0] = {
            'id' : planner.id,
            'planner_name' : planner.name,
            'desc' : planner.description
        }
        print('get planner id')
        membersid = joinMemberPlannerActivity.Jointask.query.filter_by(planner_ID=planner_id)
        print(membersid)
        i = 0
        allprice = 0
        for memberid in membersid:
            print('round: ' + str(i))
            print('member_id: '+str(memberid.member_ID))
            memberdetail = Member.query.filter_by(id=int(memberid.member_ID)).one()
            if memberdetail:
                memberdict[memberdetail.id] = [memberdetail.id, memberdetail.firstname, memberdetail.lastname, memberdetail.gender, memberdetail.is_owner]
                membertotalprice = 0
                activitys = Activity.query.filter_by(planner_ID=planner_id)
                for activity in activitys:
                    services = Service.query.filter_by(activity_ID=activity.id)
                    if services:
                        for service in services:
                            servicesdict[service.id] = [service.id, service.name]
                            price = MemberTakeService.query.filter(MemberTakeService.member_ID == memberid.member_ID,\
                                MemberTakeService.service_ID == service.id).first()
                            if price:
                                if price.price:
                                    membertotalprice = membertotalprice + int(price.price)
                                    allprice += int(price.price)

            print('get total price')
            print(membertotalprice)
            memberdict[memberdetail.id].append(membertotalprice)
            memberdict[memberdetail.id].append(servicesdict)
            print('finish append')
            i = i+1
        memberdict[0]['allprice'] = allprice
        return jsonify(dict(data=memberdict, success=True, code=200))

    except Exception as e:
        return jsonify(dict(success=False, message=str(e), code=400))









            # members = MemberTakeService.query.filter_by(service_ID = service.id)
            # priceinservice = 0
            # for member in members:
            #     memberdetail = Member.query.filter_by(id=member.member_ID)
            #     memberdict[memberdetail.id] = [memberdetail.id, memberdetail.fristname, memberdetail.lastname, memberdetail.DoB, member.price]
            #     priceinservice += member.price
            # servicedict[service.id].append(memberdict)
            # servicedict[service.id].append(priceinservice)
