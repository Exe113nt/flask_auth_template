from flask import Blueprint, render_template, flash, redirect, request, url_for
from flask_login import login_required, current_user
from .models import Collection
from . import db
import uuid
import os
from hashlib import md5
from urllib.request import urlretrieve
import requests
import shutil

mycollection = Blueprint('mycollection', __name__)

@mycollection.route('/collection')
@login_required
def mycollection():
    cards = Collection.query.filter_by(owner_id=current_user.id).all()
    return render_template('mycollection.html', name = current_user.name, id=current_user.id, cards=cards)

@mycollection.route('/view/<int:card_id>')
def view(card_id):
    card = Collection.query.filter_by(id=card_id).first()

    return render_template('view.html', card=card)


@mycollection.route('/newcard')
@login_required
def newcard():
    return render_template('new_card.html')


@mycollection.route('/newcard', methods =["POST"])
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