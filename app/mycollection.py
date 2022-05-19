@mycollection.route('/view/<int:card_id>')
def view(card_id):
    card = Card.query.filter_by(id=card_id).first()

    return render_template('view.html', card=card)


@mycollection.route('/newcard')
@login_required
def newcard():
    return render_template('new_one.html')


@mycollection.route('/newcard', methods =["POST"])
@login_required
def newcard_post():

    label = request.form['']
    name = request.form['name']
    sec_name = request.form['sec_name']
    contact_number = request.form['contact_number']
    mail = request.form['mail']
    adress = request.form['adress']
    birthday = request.form['birthday']
    social_madia = request.form['social_media']

    new_card = Collection(label = label, name = name, sec_name = sec_name, contact_number = contact_number, mail = mail, adress = adress, birthday = birthday, social_madia = social_madia)
    db.session(new_card)
    db.sessioncommit()

    return redirect('/')