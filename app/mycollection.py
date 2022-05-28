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

@mycollection.route('/mycollection')
@login_required
def coll():
    cards = Collection.query.filter_by(owner_id=current_user.id).all()
    return render_template('mycollection.html', name = current_user.name, id=current_user.id, cards=cards)


@mycollection.route('/newcard')
@login_required
def newcard():
    return render_template('new_one.html')


@mycollection.route('/newcard', methods =["POST"])
@login_required
def newcard_post():

    # label = request.form['']
    name = request.form['name']
    sec_name = request.form['sec_name']
    contact_number = request.form['contact_number']
    mail = request.form['mail']
    adress = request.form['adress']
    birthday = request.form['birthDate']
    social_media = request.form['social_media']

    new_card = Collection(owner_id = current_user.id, name = name, sec_name = sec_name, contact_number = contact_number, mail = mail, adress = adress, birthday = birthday, social_media = social_media)
    db.session.add(new_card)
    db.session.commit()

    return redirect('/profile')


@mycollection.route('/showcard/<int:user_id>/<int:card_id>')
@login_required
def showcard(user_id, card_id):
    if current_user.id != user.id:
        return 505
    
    card = Collection.query.filter_by(owner_id=current_user.id, id=card_id).first()

    return render_template('show.html', card=card, id=current_user.id)

@mycollection.route('/adding', methods=['POST'])
@login_required
def add_one():
    firstName = request.form['name']
    middleName = request.form['sec_name']
    contact_number = request.form['contact_number']
    email = request.form['email']
    adress = request.form['adress']
    birthDate = request.form['birthDate']
    social_media = request.form['social_media']

    uid = uuid.uuid4().hex