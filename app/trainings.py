from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import Training, User, Group, Student
from flask_login import current_user, login_user, logout_user, login_required

trainings = Blueprint('trainings', __name__)


@trainings.route('/trainingslist/<int:group_id>')
@login_required
def trainingslist(group_id):
    if group_id == 0:
        trainings = Training.query.filter_by(couch_id=current_user.id).order_by(Training.date.desc()).all()
    else:
        trainings = Training.query.filter_by(couch_id=current_user.id, group_id=group_id).order_by(Training.date.desc()).all()

    grouplist = Group.query.all()  
    route = '/trainingslist'
    return render_template('trainings.html', trainings=trainings, grouplist=grouplist, route=route)



@trainings.route('/newtraining')
@login_required
def newtraining():
    grouplist = Group.query.all()  
    return render_template('newtraining.html', grouplist=grouplist)



@trainings.route('/newtraining', methods=["POST"])
@login_required
def newtraining_post():
    date = request.form['date']
    group = request.form['group']

    new_training = Training(date=date, group_id=Group.query.filter_by(text=group).first().id, couch_id=current_user.id)

    db.session.add(new_training)
    db.session.commit()

    return redirect('trainingslist/0')