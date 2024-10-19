from flask import Blueprint, render_template, flash,request, redirect, url_for
from flask_login import  current_user
from .models import Note
from .db import db
from sqlalchemy.sql.functions import user
views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    return render_template('index.html', user=current_user)


@views.route('/delete-note/<int:note_id>', methods=['POST', 'GET'])
def delete_note(note_id):
    note = Note.query.get(note_id)
    if note:
        try:
            db.session.delete(note)
            db.session.commit()
            flash('Note deleted successfully!', category='success')
        except:
            flash('Error deleting note.', category='error')
    else:
        flash('Note not found.', category='error')
    return redirect(url_for('views.home'))

@views.route('/complete-note/<int:note_id>', methods=['GET','POST'])
def complete_note(note_id):
    note = Note.query.get(note_id)
    if note:
        note.complete = not note.complete 
        db.session.commit()
        if note.complete:
            flash('Note marked as complete!', category='success')
        else:
            flash('Note marked as incomplete!', category='success')
    else:
        flash('Note not found.', category='error')
    return redirect(url_for('views.home'))
