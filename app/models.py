from flask_login import UserMixin
from . import db
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))

class Card(UserMixin, db.Model):
    card_id = db.Column(db.Integer, primary_key=True)
    text = db.Column((db.String(500))
    timestamp = db.Column(db.Datetime, index = True, default= datetime.utcnow)
    label = db.Column((db.String(40))


