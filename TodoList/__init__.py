from flask import Flask, request, redirect, url_for
import os
from flask_login import LoginManager, current_user
from dotenv import load_dotenv
from .user import user
from .views import views
from .db import db 

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.getenv('DB_NAME')}"
    
    db.init_app(app)

    with app.app_context():
        from .models import User, Note 
        db.create_all()     
    app.register_blueprint(user)
    app.register_blueprint(views)
    
    login_manager = LoginManager()
    login_manager.login_view = 'user.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    @app.before_request
    # Check permission to access the page
    def require_login():
        router_pl = ['user.login', 'user.signup']
        if not current_user.is_authenticated and request.endpoint not in router_pl:
            return redirect(url_for('user.login'))
    return app
