from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User
from app.forms import RegistrationForm, LoginForm

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route."""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            # Check if username or email already exists
            existing_user = User.query.filter(
                (User.username == form.username.data) | 
                (User.email == form.email.data)
            ).first()
            
            if existing_user:
                flash('Username or email already exists. Please choose different ones.', 'danger')
                return render_template('register.html', form=form)
            
            # Create new user
            user = User(
                username=form.username.data,
                email=form.email.data,
                phone=form.phone.data,
                is_student=form.is_student.data,
                school=form.school.data if form.is_student.data else None,
                student_id=form.student_id.data if form.is_student.data else None
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            
            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            from flask import current_app
            current_app.logger.error(f'Registration error: {str(e)}')
            flash('An error occurred during registration. Please try again.', 'danger')
    
    return render_template('register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """User login route."""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data if hasattr(form, 'remember_me') else False)
                next_page = request.args.get('next')
                # Security: validate next_page to prevent open redirects
                if next_page and not next_page.startswith('/'):
                    next_page = None
                return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
        except Exception as e:
            from flask import current_app
            current_app.logger.error(f'Login error: {str(e)}')
            flash('An error occurred during login. Please try again.', 'danger')
    
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    """User logout route."""
    logout_user()
    return redirect(url_for('main.home'))