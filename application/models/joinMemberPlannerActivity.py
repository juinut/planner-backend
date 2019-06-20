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
    db.UniqueConstraint('user_id', 'team_id', 'role_id')
    db.relationship('User', uselist=False, backref='memberships', lazy='dynamic')
    db.relationship('Team', uselist=False, backref='memberships', lazy='dynamic')
    db.relationship('Role', uselist=False, backref='memberships', lazy='dynamic')

    def __repr__(self):
        return "<Jointask(%s)>"

