from flask import Blueprint, render_template, flash, redirect, request, url_for
from flask_login import login_required, current_user
from .models import Card
from . import db
import uuid
import os
from hashlib import md5
from urllib.request import urlretrieve
import requests
import shutil

cards = Blueprint('cards', __name__)

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

@cards.route('/mycards')
@login_required
def mycards():
    cards = Card.query.filter_by(owner_id=current_user.id).all()
    return render_template('mycards.html', name = current_user.name, id=current_user.id, cards=cards)

@cards.route('/newcard')
@login_required
def newcard():
    return render_template('newcard.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@cards.route('/addcard', methods=["POST"])
@login_required
def addcard():
    firstName = request.form['firstName']
    middleName = request.form['middleName']
    lastName = request.form['lastName']
    birthDate = request.form['birthDate']
    favColor = request.form['favColor']
    favFood = request.form['favFood']
    personalityType = request.form['personalityType']
    uid = uuid.uuid4().hex

    
    if request.files["image"].filename != '':
        f = request.files['image']
        f.save(os.path.dirname(__file__)+'/static/'+uid + '.jpg')
    else:
        get_avatar(uid)

    new_card = Card(owner_id=current_user.id,
                firstName=firstName,
                middleName=middleName, 
                lastName=lastName,
                birthDate=birthDate,
                favColor=favColor,
                favFood=favFood,
                personalityType=personalityType,
                image=uid
     )
    db.session.add(new_card)
    db.session.commit()


    return redirect('/mycards')


@cards.route('/showcard/<int:user_id>/<int:card_id>')
@login_required
def showcard(user_id, card_id):
    if current_user.id != user_id:
        return 505
    
    card = Card.query.filter_by(owner_id=current_user.id, id=card_id).first()

    print(card)
    return render_template('showcard.html', card=card, id=current_user.id)


@cards.route('/deletecard/<int:user_id>/<int:card_id>')
@login_required
def deletecard(user_id, card_id):
    if current_user.id != user_id:
        return 505
    image_uid = Card.query.filter_by(id=card_id).first().image
    Card.query.filter_by(id=card_id).delete()
    imamge_path =  os.path.dirname(__file__)+'/static/'+image_uid + '.jpg'
    if os.path.exists(imamge_path):
        os.remove(imamge_path)
    db.session.commit()
    return redirect('/mycards')


@cards.route('/changecard/<int:user_id>/<int:card_id>')
@login_required
def changecard(user_id, card_id):
    if current_user.id != user_id:
        return 505
    card = Card.query.filter_by(owner_id=current_user.id, id=card_id).first()
    return render_template('changecard.html', card=card, id=user_id)


@cards.route('/changecard/<int:user_id>/<int:card_id>', methods=["POST"])
@login_required
def changecard_post(user_id, card_id):
    if current_user.id != user_id:
        return 505

    firstName = request.form['firstName']
    middleName = request.form['middleName']
    lastName = request.form['lastName']
    birthDate = request.form['birthDate']
    favColor = request.form['favColor']
    favFood = request.form['favFood']
    personalityType = request.form['personalityType']
    


    Card.query.filter_by(id = card_id).update({'firstName': firstName,
                                                 'middleName':middleName,
                                                 'lastName':lastName,
                                                 'birthDate':birthDate,
                                                 'favColor':favColor,
                                                 'favFood':favFood,
                                                 'personalityType':personalityType
                                                 })
    if request.files["image"].filename != '':
        image = request.files['image']
        image_uid = Card.query.filter_by(id = card_id).first().image
        image.save(os.path.dirname(__file__)+'/static/'+image_uid + '.jpg')

    db.session.commit()

    return redirect(f'/showcard/{user_id}/{card_id}')



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
        with open(os.path.dirname(__file__)+'/static/'+filename,'wb') as f:
            shutil.copyfileobj(r.raw, f)
            