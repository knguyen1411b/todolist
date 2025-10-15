from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from ..services.user_service import UserService

user = Blueprint('user', __name__)


@user.route('/signin', methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        password = request.form.get('password')
        
        if not user_name or not password:
            flash('Username and password are required!', category='error')
            return render_template('signin.html', user=current_user)

        result = UserService.authenticate_user(user_name, password)
        
        if result['success']:
            login_user(result['user'], remember=True)
            flash('Logged in successfully!', category='success')
            
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('views.home'))
        else:
            flash('Invalid username or password!', category='error')
    
    return render_template('signin.html', user=current_user)


@user.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        user_name = request.form.get('user_name')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not all([email, user_name, password, confirm_password]):
            flash('All fields are required!', category='error')
            return render_template('signup.html', user=current_user)
        
        result = UserService.create_user(email, user_name, password, confirm_password)
        
        if result['success']:
            login_user(result['user'], remember=True)
            flash('Account created successfully! Welcome!', category='success')
            return redirect(url_for('views.home'))
        else:
            for error in result['errors']:
                flash(error, category='error')
    
    return render_template('signup.html', user=current_user)


@user.route('/logout')
@login_required
def logout():
    user_name = current_user.user_name
    logout_user()
    flash(f'Goodbye {user_name}! Logged out successfully!', category='success')
    return redirect(url_for('user.signin'))


@user.route('/profile')
@login_required
def profile():
    """Trang profile của user"""
    user_stats = {
        'total_notes': current_user.get_notes_count(),
        'completed_notes': current_user.get_notes_count(completed=True),
        'pending_notes': current_user.get_notes_count(completed=False),
        'completion_rate': 0
    }
    
    if user_stats['total_notes'] > 0:
        user_stats['completion_rate'] = round(
            (user_stats['completed_notes'] / user_stats['total_notes']) * 100, 1
        )
    
    return render_template('profile.html', user=current_user, stats=user_stats)


@user.route('/api/check-username', methods=['POST'])
def check_username():
    """API endpoint để kiểm tra username có tồn tại không"""
    username = request.json.get('username')
    if not username:
        return jsonify({'available': False, 'message': 'Username is required'}), 400
    
    exists = UserService.user_exists('', username)
    return jsonify({
        'available': not exists,
        'message': 'Username is available' if not exists else 'Username already taken'
    })


@user.route('/api/check-email', methods=['POST'])
def check_email():
    """API endpoint để kiểm tra email có tồn tại không"""
    email = request.json.get('email')
    if not email:
        return jsonify({'available': False, 'message': 'Email is required'}), 400
    
    exists = UserService.user_exists(email, '')
    return jsonify({
        'available': not exists,
        'message': 'Email is available' if not exists else 'Email already registered'
    })
