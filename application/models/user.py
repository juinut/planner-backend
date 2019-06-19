# coding: utf-8
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from ._base import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    firstname = db.Column(db.String(255),nullable=False)
    lastname =  db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean, default=False)
    dob = db.Column(db.Date, nullable=False)
    

    # relationship
    planners = db.relationship("Planner", backref='owner', lazy=True)
    members = db.relationship("Member", backref="owner", lazy=True)

    def __repr__(self):
        return '<User %s>' % self.name
