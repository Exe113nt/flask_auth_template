from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User, Topic, Comment
from flask_login import current_user, login_user, logout_user, login_required

topics = Blueprint('topics', __name__)


@topics.route('/home')
def home():
    pass


@topics.route('/addtopic')
def addtopic():
    return render_template('addtopic.html')

@topics.route('/addtopic', methods=["POST"])
@login_required
def addtopic_post():
    theme = request.form['topic_theme']
    text = request.form['topic_text']
    new_topic = Topic(owner_id=current_user.id, theme=theme, text=text)
    db.session.add(new_topic)
    db.session.commit()
    return redirect('/')

@topics.route('/mytopics')
def mytopics():
    pass

@topics.route('/viewtopic/<int:topic_id>')
def viewtopic(topic_id):
    topic = Topic.query.filter_by(id=topic_id).first()
    # comments = Comment.query.filter_by(topic_id=topic.id).all()
    comments = Comment.query.join(User, Comment.owner_id == User.id).join(Topic, Comment.topic_id == topic_id).add_columns(User.name).order_by(Comment.timestamp.desc()).all()
    print(comments)
    return render_template('viewtopic.html', topic=topic, current_user=current_user,comments=comments)


@topics.route('/addcomment', methods=["POST"])
@login_required
def addcomment():
    topic_id = request.form["topicId"]
    comment_text = request.form["commentText"]
    new_comment = Comment(owner_id=current_user.id, topic_id=topic_id, text=comment_text)

    db.session.add(new_comment)
    db.session.commit()

    return redirect(f"/viewtopic/{topic_id}")