from .db import db
from sqlalchemy.sql import func
from flask_login import UserMixin

# TODO: Cấu trúc lại models để tối ưu hơn

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    notes = db.relationship('Note', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, user_name, email, password):
        self.user_name = user_name
        self.email = email
        self.password = password
    
    def __repr__(self):
        return f'<User {self.user_name}>'
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'user_name': self.user_name,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def get_notes_count(self, completed=None):
        """Count notes, filter by completion status if provided"""
        query = Note.query.filter_by(user_id=self.id)
        if completed is not None:
            query = query.filter_by(complete=completed)
        return query.count()
    
    def get_completed_notes(self):
        """Get completed notes"""
        return Note.query.filter_by(user_id=self.id, complete=True).order_by(Note.date.desc()).all()
    
    def get_pending_notes(self):
        """Get pending notes"""
        return Note.query.filter_by(user_id=self.id, complete=False).order_by(Note.date.desc()).all()


class Note(db.Model):
    __tablename__ = 'note'
    
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    complete = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __init__(self, data, user_id):
        self.data = data
        self.user_id = user_id
    
    def __repr__(self):
        return f'<Note {self.id}: {self.data[:50]}>'
    
    def to_dict(self):
        """Convert note to dictionary"""
        return {
            'id': self.id,
            'data': self.data,
            'date': self.date.isoformat() if self.date else None,
            'complete': self.complete,
            'user_id': self.user_id
        }
    
    def format_date(self):
        """Format date for display"""
        if self.date:
            return self.date.strftime('%Y-%m-%d %H:%M')
        return ''
