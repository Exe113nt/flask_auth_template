from flask import Blueprint, get_flashed_messages, render_template,request, flash, redirect, url_for,send_file
from flask_login import login_required, current_user
from .models import User, Document
from . import db
import os
from hurry.filesize import size

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():

    dirpath = os.path.dirname(__file__)+f'\\static\\{current_user.id}'
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    filter = request.args.get('filter')
    if filter:
        files = Document.query.filter_by(owner_id=current_user.id).filter(Document.fileName.contains(f'.{filter}')).all()
    else:
        files = Document.query.filter_by(owner_id=current_user.id).all()
    
    weight = get_size(dirpath)
    filterList = [ext[ext.find('.')+1:] for ext in os.listdir(dirpath)]
    header = filter if filter else 'все'
    
    return render_template('index.html', files=files, filters=set(filterList), header=header.capitalize(), weight=weight)


@main.route('/uploadfile', methods=["POST"])
@login_required
def uploadfile():  
    file = request.files["file"]
    
    dirpath = os.path.dirname(__file__)+f'\\static\\{current_user.id}'

    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    file.save(dirpath+'\\'+file.filename)

    if not Document.query.filter_by(owner_id=current_user.id, fileName=file.filename).first():
        new_doc = Document(owner_id=current_user.id, fileName=file.filename)
        db.session.add(new_doc)
        db.session.commit()
    # flash('Uploaded succesfully')
    return redirect(url_for('main.index'))


@main.route('/download/<int:file_id>')
@login_required
def download(file_id):  

    filename = Document.query.filter_by(id=file_id).first().fileName
    dirpath = os.path.dirname(__file__)+f'\\static\\{current_user.id}\\'
    return send_file(dirpath + filename, as_attachment=True)



@main.route('/delete/<int:file_id>')
@login_required
def delete(file_id):
    dirpath = os.path.dirname(__file__)+f'\\static\\{current_user.id}\\'
    filename = Document.query.filter_by(id=file_id).first().fileName
    os.remove(dirpath+filename)
    Document.query.filter_by(id=file_id).delete()
    
    db.session.commit()
    return redirect(f'/')


def get_size(path):
    filesSize = 0
    Folderpath = path
    for ele in os.scandir(Folderpath):
        filesSize+=os.stat(ele).st_size

    return size(filesSize)