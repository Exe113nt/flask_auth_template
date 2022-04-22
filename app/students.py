from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required

students = Blueprint('students', __name__)

@students.route('/showtrainings')
def showtrainings():
    return render_template('trainings.html')