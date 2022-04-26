from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User, Group_, Student
from flask_login import current_user, login_user, logout_user, login_required

students = Blueprint('students', __name__)


@students.route('/studentslist/<int:group_id>')
@login_required
def studentslist(group_id):
    if group_id == 0:
        students = Student.query.filter_by(couch_id=current_user.id).order_by(Student.surname.asc()).all()
    else:
        students = Student.query.filter_by(couch_id=current_user.id, group_id=group_id).order_by(Student.surname.asc()).all()
    grouplist = Group_.query.all()  
    route = '/studentslist'
    return render_template('students.html', students=students, grouplist=grouplist, route=route)


@students.route('/viewstudent/<int:student_id>')
@login_required
def viewstudent(student_id):

    student = Student.query.filter_by(id=student_id).first()
    query = f"select group_.text from group_ join student on student.group_id=group_.id where student.id={student_id}"
    group = db.engine.execute(query).first()[0]
    route = '/studentslist'
    return render_template('viewstudent.html', student=student, route=route, group=group)


@students.route('/deletestudent', methods=["POST"])
@login_required
def viewstudent_post():
    student_id = request.form["student_id"]

    Student.query.filter_by(id=student_id).delete()
    db.session.commit()
    return redirect('/studentslist/0')



@students.route('/editstudent/<int:student_id>')
@login_required
def editstudent(student_id):

    student = Student.query.filter_by(id=student_id).first()
    groups = Group_.query.all()
    return render_template('editstudent.html', student=student, groups=groups)


@students.route('/editstudent', methods=["POST"])
@login_required
def editstudent_post():
    student_id = request.form['student_id']
    name = request.form['name']
    surname = request.form['surname']
    group = request.form['group']
    student = Student.query.filter_by(id=student_id).update({'name':name,
                                                            'surname':surname,
                                                            'group_id':Group_.query.filter_by(text=group).first().id})
    db.session.commit()
    return redirect(f'/viewstudent/{student_id}')


@students.route('/newstudent')
def newstudent():
    grouplist = Group_.query.all()  
    return render_template('newstudent.html', grouplist=grouplist)



@students.route('/newstudent', methods=["POST"])
@login_required
def newstudent_post():
    name = request.form['name']
    surname = request.form['surname']
    group = request.form['group']

    new_student = Student(name=name, surname=surname, group_id=Group_.query.filter_by(text=group).first().id, couch_id=current_user.id)

    db.session.add(new_student)
    db.session.commit()

    return redirect('studentslist/0')
