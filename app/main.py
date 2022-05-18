from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from .models import *

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # Выбрать все из Cards
    cards = Collection.query.all()

    return render_template('index.html', cards=cards)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name = current_user.name)