from tokenize import group
from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from .models import User, Group_, Task
from . import db

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    return redirect('/0')


@main.route('/newgroup')
@login_required
def newgroup(): 
    groups = Group_.query.all()
    tasks = Task.query.filter_by(owner_id=current_user.id).order_by(Task.expire_date.asc()).all()
    return render_template('newgroup_index.html', tasks=tasks, grouplist=groups, group="All")


@main.route('/newtask/<int:group_id>')
@login_required
def newtask(group_id): 
    groups = Group_.query.all()
    tasks = Task.query.filter_by(owner_id=current_user.id, taskgroup_id=group_id).order_by(Task.expire_date.asc()).all()
    groupname = Task.query.filter_by(id=group_id).first().name
    return render_template('newtask_index.html', grouplist=groups, group_id=group_id, tasks=tasks, groupname=groupname)


@main.route('/newtask', methods=["POST"])
@login_required
def newtask_post(): 
    name = request.form['name']
    expire = request.form['expire_date']
    gr_id = request.form['gr_id']
    new_task = Task(owner_id=current_user.id, name=name, expire_date=expire, taskgroup_id=gr_id)
    db.session.add(new_task)
    db.session.commit()
    return redirect(f'/{gr_id}')


@main.route('/newgroup', methods=["POST"])
@login_required
def newgroup_post(): 
    name = request.form['name']
    new_group = Group_(owner_id=current_user.id, name=name)
    db.session.add(new_group)
    db.session.commit()

    return redirect('/')


@main.route('/deletegroup/<int:group_id>')
@login_required
def deletegroup(group_id):
    Group_.query.filter_by(id=group_id, owner_id=current_user.id).delete()
    Task.query.filter_by(taskgroup_id=group_id, owner_id=current_user.id).delete()
    db.session.commit()
    return redirect('/')


@main.route('/deletetask/<int:task_id>')
@login_required
def deletetask(task_id):
    Task.query.filter_by(id=task_id, owner_id=current_user.id).delete()
    db.session.commit()
    return redirect('/')


@main.route('/<int:group_id>')
@login_required
def indexgroup(group_id):
    if group_id == 0:
        tasks = Task.query.filter_by(owner_id=current_user.id).order_by(Task.expire_date.asc()).all()
    else:
        tasks = Task.query.filter_by(owner_id=current_user.id, taskgroup_id=group_id).order_by(Task.expire_date.asc()).all()
    groups = Group_.query.all()  
    group = Group_.query.filter_by(id=group_id).first() if group_id != 0 else 'All'
    print(group)
    # groupId = 0 if Group_.query.filter_by(id=group_id).first() == None else Group_.query.filter_by(id=group_id).first().id
    return render_template('index.html', tasks=tasks, grouplist=groups, group=group)