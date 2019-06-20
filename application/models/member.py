# coding: utf-8
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from ._base import db


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    DoB = db.Column(db.DateTime, nullable=False)
    # foreignKey
    user_ID = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # relationship
    user = db.relationship("User", backref="members", lazy='dynamic')
    # jointrip = db.relationship('Jointask', secondary='jointask', backref=db.backref('members', lazy='dynamic'))

    def __repr__(self):
        return '<Member %s>' % self.firstname
