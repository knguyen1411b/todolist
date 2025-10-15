from flask import Flask, request, redirect, url_for
import os
import logging
from flask_login import LoginManager, current_user
from dotenv import load_dotenv
from .api.note_route import views
from .api.user_route import user
from .db import db
from .utils.error_handlers import register_error_handlers

load_dotenv()

def create_app(config_name=None):
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('KEY', '')

    # Ensure instance folder exists for SQLite DB
    instance_path = os.path.join(os.getcwd(), 'instance')
    os.makedirs(instance_path, exist_ok=True)
    db_file = os.getenv('DB_NAME', os.path.join('instance', 'todolist.db'))
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_file}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Logging configuration
    if not app.debug:
        logging.basicConfig(level=logging.INFO)
        app.logger.setLevel(logging.INFO)
    
    # Initialize extensions
    db.init_app(app)
    
    # Create database tables
    with app.app_context():
        from .models import User, Note 
        db.create_all()
    
    # Register blueprints
    app.register_blueprint(user)
    app.register_blueprint(views)
    
    # Setup Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'user.signin'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from .services.user_service import UserService
        return UserService.get_user_by_id(int(user_id))
    
    @app.before_request
    def require_login():
        """Require login for most endpoints"""
        # Endpoints that don't require login
        public_endpoints = ['user.signin', 'user.signup', 'user.check_username', 'user.check_email']
        
        # Static files và error pages không cần login
        if (request.endpoint and 
            (request.endpoint in public_endpoints or 
             request.endpoint.startswith('static'))):
            return
            
        if not current_user.is_authenticated:
            return redirect(url_for('user.signin', next=request.url))
    
    # Register error handlers
    register_error_handlers(app)
    
    # Add some global template variables
    @app.context_processor
    def inject_global_vars():
        return {
            'app_name': 'TodoList App',
            'version': '2.0'
        }
    
    return app
