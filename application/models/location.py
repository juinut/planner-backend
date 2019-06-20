# coding: utf-8
from ._base import db


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float(precision=24), nullable=False)
    longtitude = db.Column(db.Float(precision=24), nullable=False)
    #ForeignKey
    # relationship
    start = db.relationship("Service", backref='start_loc', lazy='dynamic')
    stop = db.relationship("Service", backref='stop_loc', lazy='dynamic')
    end = db.relationship("Service", backref='in_loc', lazy='dynamic')
    def __repr__(self):
        return '<Location %s>' % self.name
