from flask import Blueprint, render_template, flash, request, redirect, url_for, jsonify
from flask_login import current_user, login_required
from ..services.note_service import NoteService

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note_data = request.form.get('note')
        if not note_data:
            flash('Note content is required!', category='error')
        else:
            result = NoteService.create_note(note_data, current_user.id)
            if result['success']:
                flash('Note added successfully!', category='success')
            else:
                flash(result['error'], category='error')
        return redirect(url_for('views.home'))
    
    notes = NoteService.get_user_notes(current_user.id)
    stats = {
        'total': len(notes),
        'completed': sum(1 for note in notes if note.complete),
        'pending': sum(1 for note in notes if not note.complete)
    }
    
    return render_template('index.html', user=current_user, notes=notes, stats=stats)


@views.route('/delete-note/<int:note_id>', methods=['POST', 'DELETE'])
@login_required
def delete_note(note_id):
    result = NoteService.delete_note(note_id, current_user.id)
    
    if request.method == 'DELETE' or request.is_json:
        return jsonify(result), 200 if result['success'] else 404
    
    if result['success']:
        flash('Note deleted successfully!', category='success')
    else:
        flash(result['error'], category='error')
    
    return redirect(url_for('views.home'))


@views.route('/complete-note/<int:note_id>', methods=['POST', 'PATCH'])
@login_required
def complete_note(note_id):
    result = NoteService.toggle_complete(note_id, current_user.id)
    
    if request.method == 'PATCH' or request.is_json:
        return jsonify(result), 200 if result['success'] else 404
    
    if result['success']:
        status = 'complete' if result['is_complete'] else 'incomplete'
        flash(f'Note marked as {status}!', category='success')
    else:
        flash(result['error'], category='error')
    
    return redirect(url_for('views.home'))


@views.route('/edit-note/<int:note_id>', methods=['POST', 'PUT'])
@login_required
def edit_note(note_id):
    new_data = None

    if request.is_json:
        json_data = request.get_json(silent=True)
        if json_data:
            new_data = json_data.get('data')
    else:
        new_data = request.form.get('note_data')

    if not new_data:
        error_msg = 'Note content is required!'
        if request.is_json:
            return jsonify({'success': False, 'error': error_msg}), 400
        flash(error_msg, category='error')
        return redirect(url_for('views.home'))

    result = NoteService.update_note(note_id, current_user.id, new_data)

    if request.is_json:
        return jsonify(result), 200 if result['success'] else 400

    if result['success']:
        flash('Note updated successfully!', category='success')
    else:
        flash(result['error'], category='error')

    return redirect(url_for('views.home'))


@views.route('/api/notes', methods=['GET'])
@login_required
def api_get_notes():
    """API endpoint để lấy danh sách notes"""
    completed = request.args.get('completed')
    if completed is not None:
        completed = completed.lower() == 'true'
    
    notes = NoteService.get_user_notes(current_user.id, completed)
    return jsonify({
        'success': True,
        'notes': [note.to_dict() for note in notes]
    })


@views.route('/api/notes/<int:note_id>', methods=['GET'])
@login_required
def api_get_note(note_id):
    """API endpoint để lấy thông tin một note"""
    note = NoteService.get_note_by_id(note_id, current_user.id)
    if note:
        return jsonify({'success': True, 'note': note.to_dict()})
    return jsonify({'success': False, 'error': 'Note not found'}), 404
