# coding: utf-8
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from ._base import db


class Planner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    first_date = db.Column(db.DateTime)
    email = db.Column(db.String(255), unique=True)
    firstname = db.Column(db.String(255), nullable=False)
    lastname =  db.Column(db.String(255), nullable=False)
    # avatar = db.Column(db.String(200), default='default.png')
    password = db.Column(db.String(255))
    # active = db.Column(db.Boolean)
    # confirm_at = db.Column(db.DateTime)
    is_admin = db.Column(db.Boolean, default=False)
    dob = db.Column(db.DateTime, nullable=False)
    # created_at = db.Column(db.DateTime, default=datetime.now)

    # relationship
    roles = db.relationship("Role", secondary="users_roles", backref='users')

    def __repr__(self):
        return '<User %s>' % self.name
