# coding: utf-8
from ._base import db


class Servicetype(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)

    #ForeignKey
    # relationship
    services = db.relationship("Service", backref='servicetype', lazy='dynamic')

    def __repr__(self):
        return '<Service %s>' % self.description
