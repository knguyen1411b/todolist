from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from .db import db
import re  

user = Blueprint('user', __name__)

@user.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        password = request.form.get('password')
        existing_user = User.query.filter_by(user_name=user_name).first()
        if existing_user:
            if check_password_hash(existing_user.password, password):
                login_user(existing_user, remember=True)
                flash('Logged in successfully!', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Username does not exist.', category='error')
    return render_template('login.html', user=current_user)

@user.route('/signup', methods=['GET', 'POST'])
def signup(): 
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    if request.method == 'POST':
        email = request.form.get('email')
        user_name = request.form.get('user_name')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        existing_user = User.query.filter_by(email=email).first()  
        if existing_user:
            flash('Email already exists', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters', category='error')
        elif len(user_name) < 2:
            flash('Username must be greater than 1 character', category='error')
        elif len(password) < 6:
            flash('Password must be at least 6 characters long', category='error')
        elif password != confirm_password:
            flash('Passwords do not match', category='error')
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash('Invalid email address', category='error')
        else:
            new_user = User(email=email, user_name=user_name, password=generate_password_hash(password))
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('Account created successfully', category='success')
                login_user(new_user, remember=True)
                return redirect(url_for('user.login'))  
            except Exception as e: 
                flash(f'Error creating account: {str(e)}', category='error')

    return render_template('signup.html', user=current_user)

@user.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', category='success')
    return redirect(url_for('user.login'))
