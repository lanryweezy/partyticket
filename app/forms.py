from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateTimeField, FloatField, IntegerField, TextAreaField, SelectField, BooleanField, EmailField
from wtforms.validators import DataRequired, EqualTo, Length, NumberRange, Email

class RegistrationForm(FlaskForm):
    """User registration form."""
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=150)])
    email = EmailField('Email', validators=[DataRequired(), Email(), Length(max=150)])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', 
                                   validators=[DataRequired(), EqualTo('password')])
    is_student = BooleanField('I am a student')
    school = StringField('School (if student)', validators=[Length(max=150)])
    student_id = StringField('Student ID (if student)', validators=[Length(max=50)])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    """User login form."""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class EventForm(FlaskForm):
    """Event creation form."""
    name = StringField('Event Name', validators=[DataRequired(), Length(max=150)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=500)])
    date = DateTimeField('Date and Time', validators=[DataRequired()], format='%Y-%m-%dT%H:%M')
    location = StringField('Location', validators=[DataRequired(), Length(max=150)])
    price = FloatField('Ticket Price (₦)', validators=[DataRequired(), NumberRange(min=0)])
    invitation_fee = FloatField('Invitation Creation Fee (₦)', validators=[DataRequired(), NumberRange(min=0)], default=0.0)
    category = SelectField('Event Category', choices=[
        ('general', 'General Event'),
        ('formal', 'Formal Event (Wedding, Corporate, etc.)'),
        ('campus', 'Campus Party'),
        ('street', 'Street Party/Festival'),
        ('concert', 'Concert/Live Music'),
        ('festival', 'Cultural Festival')
    ], validators=[DataRequired()])
    submit = SubmitField('Create Event')

class TicketForm(FlaskForm):
    """Ticket purchase form."""
    quantity = IntegerField('Number of Tickets', validators=[DataRequired(), NumberRange(min=1, max=10)], default=1)
    submit = SubmitField('Purchase Tickets')

class InvitationForm(FlaskForm):
    """Invitation creation form."""
    event_id = IntegerField('Event ID', validators=[DataRequired()])
    max_attendees = IntegerField('Max Attendees', validators=[DataRequired(), NumberRange(min=1, max=100)])
    submit = SubmitField('Create Invitation')

class BlogPostForm(FlaskForm):
    """Blog post creation/editing form."""
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    excerpt = StringField('Excerpt', validators=[DataRequired(), Length(max=300)])
    content = TextAreaField('Content', validators=[DataRequired()])
    slug = StringField('URL Slug', validators=[DataRequired(), Length(max=200)])
    published = BooleanField('Publish Immediately')
    submit = SubmitField('Save Post')