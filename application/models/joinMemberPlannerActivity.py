# coding: utf-8
from datetime import datetime
from ._base import db


class Jointask(db.Model):
    __tablename__ = 'jointask'
    #ForeignKey
    member_ID = db.Column(db.Integer, db.ForeignKey('planner.id'), primary_key = True)
    planner_ID = db.Column(db.Integer, db.ForeignKey('member.id') ,primary_key = True)
    activity_ID =  db.Column(db.Integer, db.ForeignKey('activity.id') ,primary_key = True)

    # relationship
    db.UniqueConstraint('member_ID', 'planner_ID', 'activity_ID')
    db.relationship('Member', uselist=False, backref='tasks', lazy='dynamic')
    db.relationship('Planner', uselist=False, backref='tasks', lazy='dynamic')
    db.relationship('Activity', uselist=False, backref='tasks', lazy='dynamic')

    def __repr__(self):
        return '<JoinTask %s %s %s>' % self.member_ID, self.planner_ID, self_activity_ID
