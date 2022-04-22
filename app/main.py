from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import Topic

main = Blueprint('main', __name__)

@main.route('/')
def index():
    topics = Topic.query.order_by(Topic.timestamp.desc()).all()
    return render_template('index.html',topics=topics)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name = current_user.name) 