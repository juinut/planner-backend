# coding: utf-8
from datetime import datetime
from ._base import db


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    start = db.Column(db.DateTime ,nullable=False)
    end = db.Column(db.DateTime ,nullable=False)
    description = db.Column(db.Text, nullable=True)
    #ForeignKey
    planner_ID = db.Column(db.Integer, db.ForeignKey('planner.id'))
    # relationship
    services = db.relationship("Service", backref='activity', lazy='dynamic')
    jointrip = db.relationship('Jointask', secondary='jointask', backref=db.backref('activitys', lazy='dynamic'))

    def __repr__(self):
        return '<Activity %s>' % self.firstname
