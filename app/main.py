from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from . import db
from .models import User, Comment, Product
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
    return ""


@main.route('/newproduct', methods=["POST"])
@login_required
def newproduct_post():
    return ""


@main.route('/delete', methods=["POST"])
@login_required
def delete_post():
    return ""  