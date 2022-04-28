from flask_login import UserMixin
from sqlalchemy.orm import backref
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    tasks = db.relationship('Task')
    taskgroups = db.relationship('Group_')

class Group_(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(100))
    tasks = db.relationship('Task', backref=backref("children", cascade="all,delete"))

class Task(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(100))
    expire_date = db.Column(db.String(8))
    taskgroup_id = db.Column(db.Integer, db.ForeignKey('group_.id'))


