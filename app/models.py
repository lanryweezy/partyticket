from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    """User model for the application."""
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    is_student = db.Column(db.Boolean, default=False)
    is_verified_student = db.Column(db.Boolean, default=False)
    school = db.Column(db.String(150), nullable=True)
    student_id = db.Column(db.String(50), nullable=True)
    earnings = db.Column(db.Float, default=0.0)
    date_registered = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    events = db.relationship('Event', backref='organizer', lazy=True)
    tickets = db.relationship('Ticket', backref='user', lazy=True)
    invitations = db.relationship('Invitation', backref='inviter', lazy=True)
    blog_posts = db.relationship('BlogPost', backref='author', lazy=True)
    
    def set_password(self, password):
        """Hash and set user password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash."""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Event(db.Model):
    """Event model for storing event information."""
    __tablename__ = 'event'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Float, nullable=False, default=0.0)
    invitation_fee = db.Column(db.Float, default=0.0)
    category = db.Column(db.String(50), nullable=False, default='general')
    organizer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    tickets = db.relationship('Ticket', backref='event', lazy=True)
    invitations = db.relationship('Invitation', backref='event', lazy=True)
    
    def __repr__(self):
        return f'<Event {self.name}>'

class Ticket(db.Model):
    """Ticket model for storing ticket information."""
    __tablename__ = 'ticket'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_scanned = db.Column(db.Boolean, default=False)
    amount_paid = db.Column(db.Float, default=0.0)
    date_purchased = db.Column(db.DateTime, default=datetime.utcnow)
    qr_code = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<Ticket {self.id}>'

class Invitation(db.Model):
    """Invitation model for storing invitation information."""
    __tablename__ = 'invitation'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    max_attendees = db.Column(db.Integer, nullable=False)
    attendee_count = db.Column(db.Integer, default=0)
    amount_paid = db.Column(db.Float, default=0.0)
    qr_code = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Invitation {self.id}>'

class BlogPost(db.Model):
    """Blog post model for content marketing."""
    __tablename__ = 'blog_post'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    excerpt = db.Column(db.String(300), nullable=False)
    content = db.Column(db.Text, nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(50), nullable=True)
    published = db.Column(db.Boolean, default=False)
    views = db.Column(db.Integer, default=0)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<BlogPost {self.title}>'