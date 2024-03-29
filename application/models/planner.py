# coding: utf-8
from datetime import datetime
from ._base import db


class Planner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    first_date = db.Column(db.Date, nullable=False)
    last_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=True)

    #foreignkey
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # relationship
    user = db.relationship("User", backref='planners', lazy=True)
    # jointrip = db.relationship('Jointask', secondary='jointask', backref=db.backref('planners', lazy='dynamic'))

    def __repr__(self):
        return '<Planner %s>' % self.name
