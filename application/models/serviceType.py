# coding: utf-8
from ._base import db


class Servicetype(db.Model):
    __tablename__ = "servicetype"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)

    #ForeignKey
    # relationship

    def __repr__(self):
        return '<Service %s>' % self.description
