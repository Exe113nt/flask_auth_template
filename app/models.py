from tokenize import group
from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    students = db.relationship('Student')
    trainings = db.relationship('Training')


class Student(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    couch_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))

class Group(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(100))
    trainings = db.relationship('Training')


class Training(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    couch_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    date = db.Column(db.String(8))