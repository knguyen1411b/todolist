from ..models import Note
from ..db import db
from ..utils.helpers import sanitize_input


class NoteService:
    @staticmethod
    def create_note(data, user_id):
        """Tạo note mới"""
        # Sanitize và validate input
        data = sanitize_input(data)
        
        if len(data) < 1:
            return {'success': False, 'error': 'Note content cannot be empty!'}
        
        if len(data) > 10000:
            return {'success': False, 'error': 'Note content is too long (max 10000 characters)!'}
        
        try:
            new_note = Note(data=data, user_id=user_id)
            db.session.add(new_note)
            db.session.commit()
            return {'success': True, 'note': new_note}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': f'Error creating note: {str(e)}'}
    
    @staticmethod
    def delete_note(note_id, user_id):
        """Xóa note (chỉ note của user hiện tại)"""
        note = Note.query.filter_by(id=note_id, user_id=user_id).first()
        if not note:
            return {'success': False, 'error': 'Note not found or access denied'}
        
        try:
            db.session.delete(note)
            db.session.commit()
            return {'success': True}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': f'Error deleting note: {str(e)}'}
    
    @staticmethod
    def toggle_complete(note_id, user_id):
        """Toggle trạng thái complete của note"""
        note = Note.query.filter_by(id=note_id, user_id=user_id).first()
        if not note:
            return {'success': False, 'error': 'Note not found or access denied'}
        
        try:
            note.complete = not note.complete
            db.session.commit()
            return {'success': True, 'note': note, 'is_complete': note.complete}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': f'Error updating note: {str(e)}'}
    
    @staticmethod
    def get_user_notes(user_id, completed=None):
        """Lấy notes của user với filter tùy chọn"""
        query = Note.query.filter_by(user_id=user_id)
        if completed is not None:
            query = query.filter_by(complete=completed)
        return query.order_by(Note.date.desc()).all()
    
    @staticmethod
    def get_note_by_id(note_id, user_id=None):
        """Lấy note theo ID, có thể filter theo user_id"""
        query = Note.query.filter_by(id=note_id)
        if user_id:
            query = query.filter_by(user_id=user_id)
        return query.first()
    
    @staticmethod
    def update_note(note_id, user_id, new_data):
        """Cập nhật nội dung note"""
        if len(new_data.strip()) < 1:
            return {'success': False, 'error': 'Note content is too short!'}
            
        note = Note.query.filter_by(id=note_id, user_id=user_id).first()
        if not note:
            return {'success': False, 'error': 'Note not found or access denied'}
        
        try:
            note.data = new_data.strip()
            db.session.commit()
            return {'success': True, 'note': note}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': f'Error updating note: {str(e)}'}
