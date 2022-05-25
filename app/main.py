from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import Card
main = Blueprint('main', __name__)

@main.route('/')
def index():
    teams = Card.query.all()
    return render_template('index.html', teams=teams)

@main.route('/team/<int:team_id>')

def team(team_id):
    team = Card.query.filter_by(id=team_id).first()
    return render_template('team.html', team=team) 