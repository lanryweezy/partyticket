from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app import db, oauth
from app.models import User
from app.forms import RegistrationForm, LoginForm
import secrets

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


@auth.route('/login/google')
def login_google():
    """Redirect user to Google for authentication."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if not current_app.config.get('GOOGLE_CLIENT_ID') or not current_app.config.get('GOOGLE_CLIENT_SECRET'):
        flash('Google login is not configured.', 'warning')
        return redirect(url_for('auth.login'))
    
    redirect_uri = url_for('auth.google_callback', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@auth.route('/auth/google/callback')
def google_callback():
    """Handle Google OAuth callback."""
    try:
        token = oauth.google.authorize_access_token()
        user_info = oauth.google.parse_id_token(token)
        if not user_info:
            # Fallback if parse_id_token is not available
            resp = oauth.google.get('userinfo')
            user_info = resp.json()
        
        email = user_info.get('email')
        name = user_info.get('name') or email.split('@')[0]
        
        if not email:
            flash('Unable to get email from Google account.', 'danger')
            return redirect(url_for('auth.login'))
        
        user = User.query.filter_by(email=email).first()
        if not user:
            # Create a new user with a random password
            username = name.replace(' ', '').lower()
            # Ensure username uniqueness
            base_username = username
            counter = 1
            while User.query.filter_by(username=username).first():
                username = f"{base_username}{counter}"
                counter += 1
            
            user = User(
                username=username,
                email=email
            )
            user.set_password(secrets.token_hex(16))
            db.session.add(user)
            db.session.commit()
        
        login_user(user, remember=True)
        flash('Logged in with Google successfully.', 'success')
        next_page = request.args.get('next')
        if next_page and not next_page.startswith('/'):
            next_page = None
        return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
    except Exception as e:
        current_app.logger.error(f'Google login error: {str(e)}')
        flash('An error occurred during Google login. Please try again.', 'danger')
        return redirect(url_for('auth.login'))


@auth.route('/login/facebook')
def login_facebook():
    """Redirect user to Facebook for authentication."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    if not current_app.config.get('FACEBOOK_CLIENT_ID') or not current_app.config.get('FACEBOOK_CLIENT_SECRET'):
        flash('Facebook login is not configured.', 'warning')
        return redirect(url_for('auth.login'))
    
    redirect_uri = url_for('auth.facebook_callback', _external=True)
    return oauth.facebook.authorize_redirect(redirect_uri)


@auth.route('/auth/facebook/callback')
def facebook_callback():
    """Handle Facebook OAuth callback."""
    try:
        token = oauth.facebook.authorize_access_token()
        resp = oauth.facebook.get('me?fields=id,name,email')
        user_info = resp.json()
        
        email = user_info.get('email')
        name = user_info.get('name') or (email.split('@')[0] if email else None)
        
        if not email:
            flash('Unable to get email from Facebook account.', 'danger')
            return redirect(url_for('auth.login'))
        
        user = User.query.filter_by(email=email).first()
        if not user:
            username = name.replace(' ', '').lower()
            base_username = username
            counter = 1
            while User.query.filter_by(username=username).first():
                username = f"{base_username}{counter}"
                counter += 1
            
            user = User(
                username=username,
                email=email
            )
            user.set_password(secrets.token_hex(16))
            db.session.add(user)
            db.session.commit()
        
        login_user(user, remember=True)
        flash('Logged in with Facebook successfully.', 'success')
        next_page = request.args.get('next')
        if next_page and not next_page.startswith('/'):
            next_page = None
        return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
    except Exception as e:
        current_app.logger.error(f'Facebook login error: {str(e)}')
        flash('An error occurred during Facebook login. Please try again.', 'danger')
        return redirect(url_for('auth.login'))