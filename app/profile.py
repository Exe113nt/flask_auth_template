from math import prod
from re import search
from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from html2text import re
from numpy import product
from . import db
from .models import Product, Brand, Type
import uuid
import os
import requests
import shutil


profile = Blueprint('profile', __name__)

@profile.route('/profile')
@login_required
def profile_view():
    return 1

@profile.route('/newproduct')
@login_required
def newproduct():
    brands = Brand.query.all()
    types = Type.query.all()
    return render_template('newproduct.html', brands=brands, types=types)


@profile.route('/newproduct', methods=["POST"])
@login_required
def newproduct_post():
    name = request.form['name']
    description = request.form['description']
    brand = request.form['brand']
    type = request.form['type']
    price = request.form['price']
    uid = uuid.uuid4().hex

    
    if request.files["image"].filename != '':
        f = request.files['image']
        f.save(os.path.dirname(__file__)+'/static/img/'+uid + '.jpg')
    else:
        get_avatar(uid)

    new_product = Product(name=name,
                    description=description,
                    owner_id = current_user.id,
                    brand_id = Brand.query.filter_by(name=brand).first().id,
                    type_id = Type.query.filter_by(name=type).first().id,
                    price = float(price),
                    image=uid
     )
    db.session.add(new_product)
    db.session.commit()


    return redirect('/')


@profile.route('/myproducts')
@login_required
def myproducts():
    products = Product.query.filter_by(owner_id=current_user.id)
    return render_template('myproducts.html', products=products)


@profile.route('/deleteproduct', methods=["POST"])
@login_required
def deleteproduct_post():
    prod_id = request.form['id']
    image_uid = Product.query.filter_by(id=prod_id).first().image
    Product.query.filter_by(id=prod_id).delete()
    imamge_path =  os.path.dirname(__file__)+'/static/img/'+image_uid + '.jpg'
    if os.path.exists(imamge_path):
        os.remove(imamge_path)
    db.session.commit()
    return redirect('/myproducts')



def get_avatar(uid):
    image_url = 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            uid, 250)
    filename = f"{uid}.jpg"

    # Open the url image, set stream to True, this will return the stream content.
    r = requests.get(image_url, stream = True)

    # Check if the image was retrieved successfully
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True
        
        # Open a local file with wb ( write binary ) permission.
        with open(os.path.dirname(__file__)+'/static/img/'+filename,'wb') as f:
            shutil.copyfileobj(r.raw, f)