# coding: utf-8
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from ._base import db


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    DoB = db.Column(db.datetime, nullable=False)
    user_ID = db.Column(db.Integer, ForeignKey('user.id'))
    User = db.relationship("User")
    # relationship
    roles = db.relationship("Role", secondary="users_roles", backref='users')

    def __repr__(self):
        return '<Member %s>' % self.firstname
