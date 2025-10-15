from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user
from ..models import User
from ..db import db
from ..utils.helpers import validate_email, validate_password_strength, sanitize_input


class UserService:
    @staticmethod
    def create_user(email, username, password, confirm_password=None):
        """Tạo user mới với validation"""
        validation_errors = UserService.validate_user_data(email, username, password, confirm_password)
        if validation_errors:
            return {'success': False, 'errors': validation_errors}
        
        if UserService.user_exists(email, username):
            return {'success': False, 'errors': ['Email or username already exists']}
        
        try:
            hashed_password = generate_password_hash(password)
            new_user = User(email=email, user_name=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return {'success': True, 'user': new_user}
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'errors': [f'Error creating account: {str(e)}']}
    
    @staticmethod
    def authenticate_user(username, password):
        """Xác thực người dùng"""
        if not username or not password:
            return {'success': False, 'error': 'Username and password are required'}
            
        user = User.query.filter_by(user_name=username).first()
        if user and check_password_hash(user.password, password):
            return {'success': True, 'user': user}
        return {'success': False, 'error': 'Invalid credentials'}
    
    @staticmethod
    def validate_user_data(email, username, password, confirm_password=None):
        """Validate dữ liệu user"""
        errors = []
        
        email = sanitize_input(email)
        username = sanitize_input(username)
        
        if len(email) < 4:
            errors.append('Email must be greater than 4 characters')
        if not validate_email(email):
            errors.append('Invalid email address format')
        
        if len(username) < 2:
            errors.append('Username must be greater than 1 character')
        if len(username) > 150:
            errors.append('Username is too long (max 150 characters)')
        
        if len(password) < 6:
            errors.append('Password must be at least 6 characters long')
        
        password_errors = validate_password_strength(password)
        errors.extend(password_errors)
        
        if confirm_password and password != confirm_password:
            errors.append('Passwords do not match')
            
        return errors
    
    @staticmethod
    def user_exists(email, username):
        """Kiểm tra user đã tồn tại chưa"""
        return User.query.filter((User.email == email) | (User.user_name == username)).first() is not None
    
    @staticmethod
    def get_user_by_id(user_id):
        """Lấy user theo ID"""
        return User.query.get(user_id)
