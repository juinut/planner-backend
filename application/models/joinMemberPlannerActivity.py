# coding: utf-8
from datetime import datetime
from ._base import db


class Jointask(db.Model):
    #ForeignKey
    member_ID = db.Column(db.Integer, db.ForeignKey('planner.id'))
    planner_ID = db.Column(db.Integer, db.ForeignKey('member.id'))
    activity_ID =  db.Column(db.Integer, db.ForeignKey('activity.id'))
    # relationship
    
    def __repr__(self):
        return f"Jointask('{self.member_ID}','{self.activity_ID}','{self.planner_ID}')"
