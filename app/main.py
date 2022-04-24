from math import prod
from re import search
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from numpy import product
from . import db
from .models import Product, Brand, Type

main = Blueprint('main', __name__)

@main.route('/')
def index():
    brands = db.engine.execute(db.select([Brand.name])).all()
    types = db.engine.execute(db.select([Type.name])).all()
    products = Product.query.all()
    return render_template('index.html', brands=brands, types=types, products=products)

@main.route('/search', methods=["GET"])
def search():
    search_query = f" (product.name LIKE '%{request.args.get('q')}%')" if request.args.get('q') else 'True'

    type_join_query = " JOIN type ON product.type_id = type.id" if request.args.get('type') else ""
    type_where_query = f"type.name='{request.args.get('type')}'" if request.args.get('type') else 'True'

    brand_join_query = " JOIN brand ON product.brand_id = brand.id" if request.args.get('brand') else ''
    brand_where_query = f" brand.name='{request.args.get('brand')}'" if request.args.get('brand') else 'True'

    minprice_where_query = f" product.price > {request.args.get('min_price')}" if request.args.get('min_price') else 'True'
    maxprice_where_query = f" product.price < {request.args.get('max_price')}" if request.args.get('max_price') else 'True'

    join_substr = type_join_query + brand_join_query
    where_substr = " WHERE " +  type_where_query + " AND " + brand_where_query + " AND " + minprice_where_query + " AND " + maxprice_where_query \
        + " AND " + search_query 

    query = "Select * from Product" + join_substr + where_substr

    brands = db.engine.execute(db.select([Brand.name])).all()
    types = db.engine.execute(db.select([Type.name])).all()
    products = db.engine.execute(query).all()
    print(query)
    print(products)
    return render_template('index.html', products=products, brands=brands, types=types)
    # print(search_query2)
    # print(search_query)
    # products = Product.query.filter(Product.name.contains(search_query2), ).all()
    # print(products)
    # return render_template('index.html', products=products)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name = current_user.name) 


@main.route('/viewproduct/<int:product_id>')
def viewproduct(product_id):

    product = Product.query.join(Brand, Brand.id==Product.brand_id).join(Type, Type.id==Product.type_id).add_columns(Brand.name, Type.name).filter(Product.id==product_id).first()
    print(product)


    return render_template('viewproduct.html', product=product)