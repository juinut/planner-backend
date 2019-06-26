# coding: utf-8
from ._base import db


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    kidPrice = db.Column(db.Integer, nullable=True)
    adultPrice = db.Column(db.Integer, nullable=True)
    elderlyPrice = db.Column(db.Integer, nullable=True)
    sumPrice = db.Column(db.Integer, nullable=True)
    calType = db.Column(db.Boolean, nullable=False)
    serviceRef = db.Column(db.Integer,nullable=True)
    #ForeignKey
    activity_ID = db.Column(db.Integer, db.ForeignKey('activity.id'), nullable=False)
    serviceType_ID = db.Column(db.Integer, db.ForeignKey('servicetype.id'), nullable=False)
    location_ID = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=True)
    # location_ID_Start = db.Column(db.Integer, db.ForeignKey('servicetype.id'), nullable=True)
    # location_ID_Stop = db.Column(db.Integer, db.ForeignKey('servicetype.id'), nullable=True)
    # location_ID_In = db.Column(db.Integer, db.ForeignKey('servicetype.id'), nullable=True)
    # relationship
    activity = db.relationship("Activity", backref='services', lazy=True)
    serviceType = db.relationship("Servicetype", backref='services' ,lazy=True)
    location = db.relationship("Location", backref='services', lazy=True)
    # location_Start = db.relationship("Location", backref='services_start', lazy=True)
    # location_In = db.relationship("Location", backref='services_in', lazy=True)
    # location_Stop = db.relationship("Location", backref='services_stop', lazy=True)

    def __repr__(self):
        return '<Service %s>' % self.name
