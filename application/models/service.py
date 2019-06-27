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
    #ForeignKey
    activity_ID = db.Column(db.Integer, db.ForeignKey('activity.id'), nullable=False)
    location_ID = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=True)
    # relationship
    activity = db.relationship("Activity", backref='services', lazy=True)
   
    def __repr__(self):
        return '<Service %s>' % self.name
