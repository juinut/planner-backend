# coding: utf-8
from ._base import db


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Text, nullable=False)
    longtitude = db.Column(db.Text, nullable=False)
    #ForeignKey
    # relationship
    def __repr__(self):
        return '<Location %s>' % self.name
