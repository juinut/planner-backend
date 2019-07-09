# coding: utf-8
from datetime import datetime
from ._base import db


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    start = db.Column(db.DateTime ,nullable=False)
    end = db.Column(db.DateTime ,nullable=False)
    description = db.Column(db.Text, nullable=True)
    ref = db.Column(db.Integer, nullable=True)
    #ForeignKey
    planner_ID = db.Column(db.Integer, db.ForeignKey('planner.id'))
    location_ID = db.Column(db.Integer,db.ForeignKey('location.id'))
    serviceType_ID = db.Column(db.Integer, db.ForeignKey('servicetype.id'), nullable=False)
    # relationship
    planner = db.relationship("Planner",backref='activties',lazy=True)
    location = db.relationship("Location",backref='activities',lazy=True)
    serviceType = db.relationship("Servicetype", backref='services' ,lazy=True)
    # jointrip = db.relationship('Jointask', secondary='jointask', backref=db.backref('activitys', lazy='dynamic'))

    def __repr__(self):
        return '<Activity %s>' % self.name
