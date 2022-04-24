from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    products = db.relationship("Product")


class Product(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'))
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    description = db.Column(db.String(500))
    image = db.Column(db.String(100))


class Brand(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    products = db.relationship("Product")


class Type(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    products = db.relationship("Product")