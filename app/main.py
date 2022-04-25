
from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return redirect('/login')



# @main.route('/studentslist')
# @login_required
# def profile():
#     return render_template('profile.html', name = current_user.name) 