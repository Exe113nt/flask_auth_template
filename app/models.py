from flask_login import UserMixin
from . import db
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    products = db.relationship("Product")

class Product(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    image = db.Column(db.String(100))
    header = db.Column(db.String(50))
    description = db.Column(db.String(500))
    comments = db.relationship("Comment")

class Comment(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    text = db.Column(db.String(500))
    timestamp = db.Column(db.Date(), default=datetime.utcnow)