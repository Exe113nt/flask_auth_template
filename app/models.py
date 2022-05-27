from flask_login import UserMixin
from . import db
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    col = db.relationship("Collection")

class Collection(UserMixin, db.Model):
    card_id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.String(8), index = True, default= datetime.utcnow)
    label = db.Column(db.String(40))
    name = db.Column(db.String(50))
    sec_name = db.Column(db.String(50))
    contact_number = db.Column(db.String(20))
    mail = db.Column(db.String(30))
    adress = db.Column(db.String(30))
    birthday = db.Column(db.String(10))
    social_media = db.Column(db.String(20))



