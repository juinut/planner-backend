# coding: utf-8
from ._base import db


class MemberTakeService(db.Model):
    __tablename__ = 'memberTakeService'
    #ForeignKey
    member_ID = db.Column(db.Integer, db.ForeignKey('planner.id'), primary_key = True)
    service_ID = db.Column(db.Integer, db.ForeignKey('service.id') ,primary_key = True)
    price = db.Column(db.Float, nullable=True)
    # relationship
    db.UniqueConstraint('member_ID', 'service_ID')
    db.relationship('Member', uselist=False, backref='takeServices', lazy='dynamic')
    db.relationship('Service', uselist=False, backref='takeServices', lazy='dynamic')


    def __repr__(self):
        return "<MemberTakeService %s %s>" %self.member_ID, self.service_ID
