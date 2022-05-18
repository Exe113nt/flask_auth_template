from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from . import db
from .models import User, Comment, Product
import uuid
import os
main = Blueprint('main', __name__)

@main.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@main.route('/view/<int:product_id>')
def view(product_id):
    product = Product.query.filter_by(id=product_id).first()
    comments = Comment.query.filter_by(product_id=product_id).order_by(Comment.timestamp.desc()).all()
    return render_template('view.html', product=product, comments=comments)

@main.route('/addcomment', methods=["POST"])
@login_required
def addcomment_post():
    productId = request.form.get('productId')
    commentText = request.form.get('commentText')
    new_comment = Comment(owner_id=current_user.id, product_id=productId, text=commentText)
    db.session.add(new_comment)
    db.session.commit()
    return redirect(f'/view/{productId}')


@main.route('/newproduct')
@login_required
def newproduct():
    return render_template('newproduct.html')


@main.route('/newproduct', methods=["POST"])
@login_required
def newproduct_post():
    title = request.form['title']
    description = request.form['description']
    uid = uuid.uuid4().hex

    
    if request.files["image"].filename != '':
        f = request.files['image']
        f.save(os.path.dirname(__file__)+'/static/'+uid + '.jpg')

    new_product = Product(owner_id=current_user.id, header=title, description=description, image=uid)
    db.session.add(new_product)
    db.session.commit()
    return redirect('/')

@main.route('/myproducts')
@login_required
def myproducts():
    products = Product.query.filter_by(owner_id=current_user.id)
    return render_template('myproducts.html', products=products)

@main.route('/delete/<int:pr_id>')
@login_required
def delete(pr_id):
    Product.query.filter_by(id=pr_id).delete()
    db.session.commit()
    return redirect('/myproducts') 