from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    cards = db.relationship("Card")


class Card(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    firstName = db.Column(db.String(100))
    middleName = db.Column(db.String(100))
    lastName = db.Column(db.String(100))
    birthDate = db.Column(db.String(8))
    favColor = db.Column(db.String(100))
    favFood = db.Column(db.String(100))
    personalityType = db.Column(db.String(100))
    image = db.Column(db.String(32))