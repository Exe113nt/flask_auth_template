from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from .models import *

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # Выбрать все из Cards
    cards = Card.query.all()

    return render_template('index.html', cards=cards)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name = current_user.name)


@main.route('/view/<int:card_id>')
def view(card_id):
    card = Card.query.filter_by(id=card_id).first()

    return render_template('view.html', card=card)


@main.route('/newcard')
@login_required
def newcard():
    return render_template('new_card.html')


@main.route('/newcard', methods =["POST"])
@login_required
def newcard_post():

    label = request.form['']
    name = request.form['']
    sec_name = request.form['']
    contact_number = request.form['']
    mail = request.form['']
    adress = request.form['']
    birthday = request.form['']
    social_madia = request.form['']

    new_card = Card(label = label, name = name, sec_name = sec_name, contact_number = contact_number, mail = mail, adress = adress, birthday = birthday, social_madia = social_madia)
    db.session(new_card)
    db.sessioncommit()

    return redirect('/')